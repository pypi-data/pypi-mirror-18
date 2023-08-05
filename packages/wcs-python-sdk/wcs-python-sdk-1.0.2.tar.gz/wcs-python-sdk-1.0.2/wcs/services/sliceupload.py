
import copy
import binascii
import base64 
import json
import os
import time
import requests
import multiprocessing
from multiprocessing.dummy import Pool as TheadPool

from wcs.commons.config import PUT_URL
from wcs.commons.config import _BLOCK_SIZE
from wcs.commons.config import _BPUT_SIZE
from wcs.commons.config import connection_timeout
from wcs.commons.config import connection_retries
from wcs.commons.config import mkblk_retries
from wcs.commons.config import bput_retries
from wcs.commons.config import mkfile_retries
from wcs.commons.config import logging_folder

from wcs.commons.http import _post
from wcs.commons.util import get_logger
from wcs.commons.util import readfile
from wcs.commons.util import file_to_stream
from wcs.commons.util import GetUuid
from .uploadprogressrecorder import UploadProgressRecorder

record_lock = multiprocessing.Lock()



class SliceUpload(object):
    
    def __init__(self, uploadtoken, filepath, key, params, upload_progress_recorder, modify_time):
        
        self.uploadtoken = uploadtoken
        self.filepath = filepath
        self.upload_progress_recorder = upload_progress_recorder
        self.modify_time = modify_time
        self.key = key
        self.size = os.path.getsize(self.filepath)
        self.params = params
        self.num = self.size/_BLOCK_SIZE + 1
        self.status = []
        self.offsetlist = [i *  _BLOCK_SIZE for i in range(0, self.num)]
        self.logger = get_logger(logging_folder, 'sliceupload')
        self.uploadBatch = ''
        self.progress = 0

    def need_retry(self,code):
        if code == -1:
            return True
        if (code // 100 == 5 and code != 579):
            return True
        return False

    def record_upload_progress(self, result, uploadBatch):
        record_data = dict(zip(['offset', 'code', 'ctx'], result))
        record_data['uploadBatch'] = uploadBatch
        if self.modify_time:
            record_data['modify_time'] = self.modify_time
        self.upload_progress_recorder.set_upload_record(self.key, record_data)
        if record_data['code'] == 200:
            blockid = record_data['offset']/_BLOCK_SIZE
            if blockid < self.num - 1:
                blocksize = _BLOCK_SIZE
            else:
                blocksize = self.size - (blockid * _BLOCK_SIZE)
            self.progress += float(blocksize)/float(self.size)
            print 'current size: {0:d}, total upload progress: {1:.2f}%'.format(blocksize, self.progress * 100)
    
    def recovery_from_record(self):
        record = self.upload_progress_recorder.get_upload_record(self.key)
        if not record:
            return 'Null'
        return record
    
    def records_parse(self, record):
        offsets = copy.copy(self.offsetlist)
        if record == 'Null':
            return offsets, 'Null'
        for rec in record:
            if rec['code'] == 200:
                offsets.remove(rec['offset'])
            uploadBatch = rec['uploadBatch']
        return offsets, uploadBatch

    def iscomplet(self, results):
        if len(results) != self.num:
            return 0   
        for offset in self.offsetlist:
            for result in results:
                if offset == result['offset'] and result['code'] != 200:
                    return 0
        return 1

    def blockStatus(self, results):
        blockstatus = []
        for offset in self.offsetlist:
            for result in results:
                if offset == result['offset']:
                    blockstatus.append(result['ctx'])
        return blockstatus

    def recovery_to_list(self, records):
        return [[rec['offset'], rec['code'], rec['ctx']] for rec in records]
    
    def slice_upload(self):
        self.logger.info('File %s slice upload start!', self.filepath)
        records = self.recovery_from_record()
        offsets, uploadBatch = self.records_parse(records)
        self.logger.info('Recovery from upload record:offset %s, upload %s', offsets, uploadBatch)
        if len(offsets) != 0:
            self.logger.info('Thare are %d offsets need to upload', len(offsets))
            if uploadBatch == 'Null':
                uploadBatch = GetUuid()
            self.uploadBatch = uploadBatch
            self.progress = float(self.size - len(offsets) * _BLOCK_SIZE)/float(self.size)
            
            self.logger.info('Now start upload file blocks')
            pool = TheadPool()
            pool.map(self.make_block, offsets)
            pool.close()
            pool.join()
         
        else:
            self.logger.info('Do not need to upload, all file blocks have been uplaod')
        results = self.recovery_from_record()
        if self.iscomplet(results):
            self.logger.info('Now all blocks have upload suc.')
            return self.make_file(PUT_URL, self.blockStatus(results), uploadBatch)
        else:
            return -1, "slice upload uncomplet" 

    def make_bput_post(self, ctx, bputnum, uploadBatch, bput_next):
        url = self.bput_url(ctx, bputnum*_BPUT_SIZE)
        headers = self.bput_headers(uploadBatch)
        return _post(url=url, headers=headers, data=bput_next)
        
    def bput_url(self, ctx, offset):
        return 'http://{0}/bput/{1}/{2}'.format(PUT_URL, ctx, offset)
    
    def bput_headers(self, uploadBatch):
        headers = {'Authorization':self.uploadtoken }
        headers['Content-Type'] = "application/octet-stream"
        headers['uploadBatch'] = uploadBatch
        return headers

    def mlkblock_url(self, offset):
        blockid = offset/_BLOCK_SIZE
        if blockid < self.num - 1:
            url = self.block_url(_BLOCK_SIZE, blockid)
        else:
            url = self.block_url(self.size - (blockid * _BLOCK_SIZE), blockid)
        return url

    def make_block(self, offset):
        openfile = file_to_stream(self.filepath)
        bput = readfile(openfile, offset, _BPUT_SIZE)
        url = self.mlkblock_url(offset)
        headers = self.block_headers(self.uploadBatch)
        blkretry = mkblk_retries
        blkcode, blktext = _post(url=url, headers=headers, data=bput)
        while blkretry and self.need_retry(blkcode):
            blkcode, blktext = _post(url=url, headers=headers, data=bput)
            blkretry = blkretry - 1
        if self.need_retry(blkcode) or blkcode != 200:
            openfile.close()
            result = [offse, blkcode, blktext['message']]
        else:
            result = self.make_bput(openfile, blktext['ctx'], self.uploadBatch, offset)
        with record_lock:
            self.record_upload_progress(result, self.uploadBatch)
        

    def make_bput(self, inputfile, ctx, uploadBatch, offset):
        bputnum = 1
        offset_next = offset + _BPUT_SIZE
        bput_next = readfile(inputfile, offset_next, _BPUT_SIZE)
        bputretry = bput_retries
        while bput_next is not None and bputnum < _BLOCK_SIZE/_BPUT_SIZE:
            bputcode, bputtext = self.make_bput_post(ctx, bputnum, uploadBatch, bput_next)
            while bputretry and self.need_retry(bputcode):
                bputcode,bputtext = self.make_bput_post(ctx, bputnum, uploadBatch, bput_next)
                bputretry = bputretry - 1
            if self.need_retry(bputcode) or bputcode != 200:
                return offset, bputcode, bputtext['message']
            ctx = bputtext['ctx']
            offset_next = offset + bputtext['offset']
            bput_next = readfile(inputfile, offset_next, _BPUT_SIZE)
            bputnum += 1
        inputfile.close()
        return offset, bputcode, bputtext['ctx']
      
    def block_url(self, size, blocknum):
        return 'http://{0}/mkblk/{1}/{2}'.format(PUT_URL, size, blocknum)

    def block_headers(self,uploadBatch):
        headers = {'Authorization':self.uploadtoken}
        headers['Content-Type'] = "application/octet-stream"
        headers['uploadBatch'] = uploadBatch
        return headers

    def file_url(self, host):
        url = ['http://{0}/mkfile/{1}'.format(host, self.size)]
        if self.params:
            for k, v in self.params.items():
                url.append('x:{0}/{1}'.format(k, base64.b64encode(v)))
        url = '/'.join(url)
        return url

    def file_headers(self,uploadBatch):
        headers = {'Authorization':self.uploadtoken}
        headers['Content-Type'] = "text/plain"
        headers['uploadBatch'] = uploadBatch
        return headers

    def make_file(self, host, blockstatus, uploadBatch):
        url = self.file_url(host)
        self.status = blockstatus
        body = ','.join(blockstatus)
        self.logger.info('The ctx is %s, then start to make_file', body)
        headers = self.file_headers(uploadBatch)
        retry = mkfile_retries
        code,text = _post(url=url, headers=headers, data=body)
        while retry and self.need_retry(code):
            self.logger.warning('Make_file fail, now start %dth retry', mkfile_retries - retry)
            code,text = _post(url=url, headers=headers, data=body)
            retry -= 1
        if self.need_retry(code):
           self.logger.error('Sorry, the make_file error, code is %d, the reason is %s', code, text)
           self.blockStatus = []
           self.upload_progress_recorder.delete_upload_record(self.key)
        else:
           self.logger.info('Make_file suc! sliceupload complet!')
        return code,text
