#!/usr/bin/env python
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

import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    e_group = parser.add_argument_group('Detux Endpoints')
    d_group = parser.add_argument_group('Data Sources')
    s_group = parser.add_argument_group('Storage Options')
    a_group = parser.add_argument_group('Additional Options')

    s_group.add_argument('-d', '--dir',
        help='directory of files to submit, search for, or obtain reports on',
        action='store',
        type='string',
        required=False)

    s_group.add_argument('-f', '--file',
        help='file to submit, search for, or obtain report on',
        action='store',
        type='string',
        required=False)

    s_group.add_argument('-l', '--list',
        help='text file list of hashes to submit, search for, or obtain reports on',
        action='store',
        type='string',
        required=False)

    s_group.add_argument('-H', '--hash',
        help='SHA256 hash to search for or obtain report on',
        action='store',
        type='string',
        required=False)

    e_group.add_argument('-k', '--key',
        help='API key (can be obtained by creating an account on Detux.org)',
        action='store',
        type='string',
        required=True)

    e_group.add_argument('-r', '--report',
        help='obtain Detux report on submitted file',
        action='store_true',
        type=bool,
        required=False)

    e_group.add_argument('-q', '--query',
        help='search Detux for file(s)',
        action='store_true',
        required=False)

    e_group.add_argument('-s', '--submit',
        help='submit file(s) to Detux for analysis',
        action='store_true',
        required=False)

    a_group.add_argument('-t', '--threads',
        help='thread count to use (only applies if performed actions on more than 10 files)',
        action='store',
        type=int,
        required=False)

    a_group.add_argument('-v', '--verbose',
        help='print verbose status output',
        action='store_true',
        type=bool,
        default=False,
        required=False)

    args = parser.parse_args()

    print 'Nothing happens here yet.'
