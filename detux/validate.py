#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ========
#    Python library to interact with the Detux.org API and an accompanying CLI application
#    using the library for more straight forward user access.
#
#    Copyright (C) 2017  Adam M. Swanda (adam@zeroharbor.com)
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

import re

from .utils.Utils import is_file_valid


class Validate(object):
    """ Verifies arguments passed to functions are correct """
    @staticmethod
    def check_type(arg_name, correct_type, message):
        if not isinstance(arg_name, correct_type):
            raise TypeError(message)

    @staticmethod
    def sha256(data):
        sha256_re = r"\b([a-f0-9]{64}|[A-F0-9]{64})\b"
        m = re.match(sha256_re, data, re.IGNORECASE)
        if type(m.group()) is None:
            raise TypeError('"sha256" argument is not a valid SHA256 hash')


    @staticmethod
    def s3_info(s3_bucket, aws_key, aws_secret):
        if not s3_bucket:
            raise TypeError('"s3_bucket" argument must be defined when using save="s3"')
        if not aws_key:
            raise TypeError('"aws_key" argument must be defined when using save="s3"')
        if not aws_secret:
            raise TypeError('"aws_secret" argument must be defined when using save="s3"')


    @staticmethod
    def file_path(file_path):
        if not is_file_valid(file_path):
            raise TypeError('provided file either does not exist or has a zero file size')


    def submit(self, file_path, comments=None, file_name=None, _threaded=False):
        if not is_file_valid(file_path):
            raise TypeError('provided "file_path" either does not exist or has a zero file size')

        if comments is not None:
            Validate.check_type(comments, str, 'comments must be a string')

        if file_name is not None:
            Validate.check_type(file_name, str, 'file_name must be a string')


    def search(self, content=None, start=None):
        if content is not None:
            Validate.check_type(content, str, '"content" must be a string')

        if start is not None:
            Validate.check_type(start, int, '"start" argument must be an integer')


    def report(self, sha256=None, save=None, output=None, s3_bucket=None, aws_key=None, aws_secret=None, aws_region=None, _threaded=False):
        Validate.check_type(sha256, str, 'sha256 must be a string')

        sha256_re = r"\b([a-f0-9]{64}|[A-F0-9]{64})\b"
        m = re.match(sha256_re, sha256, re.IGNORECASE)
        if type(m.group()) is None:
            raise TypeError('"sha256" argument is not a valid SHA256 hash')

        if (save is not None) and (save not in ['s3', 'json']):
            raise TypeError('save must be a string of either "s3" or "json"')

        if save and output is None:
            raise TypeError('"output" argument must be specified when using "save" argument')

        if save:
            Validate.check_type(output, str, '"output" argument must be a string when using "save" argument')

            if save == 's3':
                if any([s3_bucket, aws_key, aws_secret, aws_region]) is None:
                    raise TypeError('all of the following arguments must be set when using save="json": s3_bucket, aws_key, aws_secret, aws_region')

        Validate.check_type(_threaded, bool, '"threaded" argument must be a boolean')
