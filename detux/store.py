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
import json
import boto3

from datetime import datetime

from StringIO import StringIO


jsondate = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None


class Store(object):
    def __init__(self, aws_access_id=None, aws_secret_key=None, aws_region=None):
        self.aws_key = aws_access_id
        self.aws_private = aws_secret_key
        self.aws_region = aws_region
        self.reports = []


    def _connect_s3(self):
        _s3 = boto3.resource('s3', region_name=self.aws_region, aws_access_key_id=self.aws_key, aws_secret_access_key=self.aws_private)
        return _s3


    def _verify_bucket(self, bucket_name):
        s3 = self._connect_s3()
        try:
            s3.meta.client.head_bucket(Bucket=bucket_name)
            return True
        except:
            raise TypeError('S3 Bucket %s does not exist' % bucket_name)


    def _mkdir(self, dir_path):
        """ Make a directory for storage of reports or downloaded samples """
        if os.path.isdir(dir_path):
            return True
        try:
            os.mkdir(dir_path)
            return True
        except Exception as err:
            raise err


    def to_disk(self, data, file_name):
        """ Dump JSON output to a formatted file on disk """
        if os.path.exists(file_name):
            raise OSError('output file %s already exists on disk' % file_name)

        with open(file_name, 'wb') as fp:
            json.dump(data, fp, indent=4, default=jsondate)

        if os.path.exists(file_name):
            return True

        return False


    def to_s3(self, data, bucket_name, key_name):
        """ Write JSON report to AWS S3 Bucket and key location

            @note: No attempt is made to see if the key already exists before writing to it. If it does, its data will be overwritten.
        """
        if self._verify_bucket(bucket_name):
            temp_fp = StringIO(buf=json.dumps(data, indent=4, default=jsondate))
            s3 = self._connect_s3()
            bucket = s3.Bucket(bucket_name)
            bucket.upload_fileobj(temp_fp, key_name)
            temp_fp.close()
            return True
