#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ========
#    Python library to interact with the Detux.org API and an accompanying CLI application
#    using the library for more straight forward user access.
#
#    Copyright (C) 2016  Adam M. Swanda (adam@zeroharbor.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ========

import os
import re
import logging
import logging.handlers
import requests
import threading
import Queue

# local libraries
from .utils import Utils
from .store import Store


__version__ = '0.0.1'
__author__ = 'Adam M. Swanda'

# ignore requests and urllib3 warnings
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Detux(object):
    def __init__(self, api_key, verbose=False):
        self.api_key = api_key
        self.urls = {
            'search': 'https://detux.org/api/search.php',
            'submit': 'https://detux.org/api/submit.php',
            'report': 'https://detux.org/api/report.php' }
        self.sha256_re = r"\b([a-f0-9]{64}|[A-F0-9]{64})\b"
        self.verbose = verbose

        # setup stream logging handler
        self._handler = logging.StreamHandler()
        self._handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(module)s: %(message)s'))
        self._handler.setLevel(logging.DEBUG)

        # create our logger for when verbose is used
        self._logger = logging.getLogger('detux-api')
        self._logger = self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(self._handler)


    def msg(self, data):
        """ Send a message to stdout if verbose is set when Detux was instantiated"""
        if self.verbose:
            self._logger.debug(data)


    def send_request(self, endpoint, data):
        """ Send API POST request and return full response if successful or error message if failed """
        self.msg('sending POST to %s' % endpoint)

        try:
            req = requests.post(endpoint, data=data)

            if req.status_code == 200:

                if req.json()['status'] == 1:
                    self.msg('msg="API request successful; returning JSON results" endpoint="%s"' % endpoint)
                    return req.json()

                self.msg('msg="API request failed; returning error message" endpoint="%s"' % endpoint)
                return req.json()['message']

            self.msg('msg="POST request returned non-200 HTTP status code" endpoint="%s"' % endpoint)
            result = {
                'status': req.status_code,
                'endpoint': endpoint,
                'error': 'POST request returned non-200 HTTP status code'}
            return result

        except Exception as err:
            raise err


    def search(self, content, start=None):
        """ Search Detux by hash, IP address, etc. and get the JSON results

            Each search request limits to 20 results. To page through more results,
            simply call this function again with the 'start' argument set to 1 number
            higher than your last returned result. For example; search('foo') returns the
            first page of 20 results and then search('foo', 21) would return results 21 to 40
            and so on. The JSON results does not tell you how many total pages there are.
        """
        if not isinstance(content, str):
            raise TypeError('content argument must be a string')

        endpoint = self.urls['search']
        data = {'api_key': self.api_key, 'search': content}

        if start is not None:
            if not start.isdigit():
                raise TypeError('start argument must be a digit')

            self.msg('msg="search request starting from offset %d' % int(start))
            data['from'] = int(start)

        return self.send_request(endpoint, data)


    def report(self, sha256, save=None, output_file=None, s3_bucket=None, aws_key=None, aws_secret=None, aws_region=None, _threaded=False):
        """ Search Detux for an existing report by a files SHA256 hash and get the JSON results """
        endpoint = self.urls['report']

        if not isinstance(sha256, str):
            raise TypeError('sha256 must be a string')

        if save is not None:
            if not isinstance(save, str):
                raise TypeError('save must be a string of either "s3" or "json"')
            if output_file is None:
                raise TypeError('"output" argument must be specified when using "save" argument')

        m = re.match(self.sha256_re, sha256, re.IGNORECASE)
        if type(m.group()) is None:
            raise TypeError('sha256 argument is not a valid hash')

        data = {'api_key': self.api_key, 'sha256': sha256}
        report = self.send_request(endpoint, data)

        if save == 'json':
            self.msg('msg="attempting to store JSON report to disk" file="%s"' % output_file)
            Store().to_disk(report, output_file)
        elif save == 's3':
            self.msg('msg="attempting to store JSON report to S3" bucket="%s" key="%s"' % (s3_bucket, output_file))
            Store(aws_access_id=aws_key, aws_secret_key=aws_secret, aws_region=aws_region).to_s3(report, s3_bucket, output_file)

        if save is None:
            return report


    def submit_file(self, file_path, comments=None, file_name=None, _threaded=False):
        """ Submit an individual file to Detux for analysis """
        endpoint = self.urls['submit']

        if not Utils.is_file_valid(file_path):
            raise TypeError('provided file either does not exist or has a zero file size')

        encoded_file = self.encode_file(file_path)
        if encoded_file is None:
            raise TypeError('Base64 encoding of file %s failed: unable to upload' % file_path)

        data = {'api_key': self.api_key, 'file': encoded_file}

        if comments is not None:
            if not isinstance(comments, str):
                raise TypeError('comments argument must be a string')
            data['comments'] = comments

        if file_name is not None:
            if not isinstance(file_name, str):
                raise TypeError('file_name argument must be a string')
            data['file_name'] = file_name

        if _threaded:
            report = self.send_request(endpoint, data)
            self.result_queue.put(report)
            return

        return self.send_request(endpoint, data)


    def submit_directory(self, dir_path, use_filenames=False, threads=None):
        if not os.path.isdir(dir_path):
            raise TypeError('dir_path argument is not a directory')

        results_list = []
        files = Utils.list_directory(dir_path)

        self.msg('msg="attempting to submit contents of directory" path="%s"' % dir_path)

        if threads is not None:
            if (0 < threads > 25) or (0 < threads > len(files)):
                raise TypeError('threads argument cannt be larger than 25 or the amount of files in dir_path argument')

            running_threads = []
            file_queue = Queue.Queue()
            self.msg('msg="using %d threads for submissions" path="%s"' % (threads, dir_path))

            for f in files:
                file_queue.put(f)

            for i in range(threads):
                thread = threading.Thread(target=self.submit_worker, args=(file_queue, use_filenames))
                thread.setName('thread-%d' % i)
                thread.setDaemon(False)
                running_threads.append(thread)

            for t in running_threads:
                self.msg('msg="starting thread %s" path="%s"' % (t.name, dir_path))
                t.start()

            for t in running_threads:
                self.msg('msg="joining thread %s" path="%s"' % (t.name, dir_path))
                t.join()

            results_list = [report for report in file_queue.queue]

        for f in files:
            self.msg('msg="attempting to submit file" file="%s" path="%s"' % (f, dir_path))
            report = self.submit_file(file_path=f, file_name=use_filenames)
            results_list.append(report)

        return results_list


    def submit_worker(self, file_queue, use_filenames):
        while file_queue.empty() is False:
            next_file = file_queue.get()
            if use_filenames:
                self.submit_file(next_file, file_name=os.path.basename(next_file))
            else:
                self.submit_file(next_file)
            file_queue.task_done()
