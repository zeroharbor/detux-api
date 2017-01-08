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

import os
import base64
import hashlib

from StringIO import StringIO


class Utils(object):
    @staticmethod
    def encode_file(file_path):
        """ base64 encode the contents of a file for HTTP POST upload """
        encoded = None
        temp_fp = StringIO()

        try:
            base64.encode(open(file_path, 'rb'), temp_fp)
            encoded = temp_fp.getvalue()
            temp_fp.close()
        except Exception as err:
            raise err

        temp_fp.close()
        return encoded


    @staticmethod
    def mkdir(path):
        """ attempt to make a directory and set permissions"""
        if os.path.isdir(path):
            return True

        try:
            os.mkdir(path)
            return True
        except Exception as err:
            raise err


    @staticmethod
    def is_file_valid(file_path):
        """ verify that file exists, is not a directory and has a greater than 0 size """
        if os.path.exists(file_path) and os.path.isfile(file_path) \
                and os.path.getsize(file_path) > 0:
            return True
        return False


    @staticmethod
    def get_sha256(file_name):
        """ Get the SHA256 hash of a file """
        if Utils.is_file_valid(file_name):
            s = hashlib.sha256()
            while True:
                with open(file_name, 'rb') as fp:
                    data = fp.read(16384)
                    if not data:
                        break
                    s.update(data)

            _sha256 = s.hexdigest()
            return _sha256

        return None


    @staticmethod
    def list_directory(dir_path):
        """ Walk a directory and return all valid full file paths as a list"""
        files = []

        for root, dirs, files in os.walk(dir_path, topdown=True):
            files = [f for f in files if not f[0] == '.']
            for f in files:
                path = os.path.join(root, f)
                if Utils.is_file_valid(path):
                    files.append(path)

        return files
