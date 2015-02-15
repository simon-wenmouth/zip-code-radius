#
#   Copyright 2015 Simon Wenmouth
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

import csv
import os
import requests
from collections import namedtuple
from zip_code_radius import settings

ZipCode = namedtuple('ZipCode', ['zip_code', 'lon', 'lat'])

def download():
    """Downloads the reference set of US postal codes from the
    data file hosted by GitHub.
    """
    r = requests.get(settings.DB_URL, stream=True)
    with open(settings.DB, 'w') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

def read():
    """Reads the reference set of US postal codes into the namedtuple
    'ZipCode'

    Returns:
        list (ZipCode): the reference set of US postal codes

    """
    values = []
    with open(settings.DB, 'r') as f:
        reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for record in reader:
            value = ZipCode(
                zip_code=record[0],
                lat=float(record[2]),
                lon=float(record[1]))
            values.append(value)
    return values

def exists():
    """Check for the existence of the reference file of US postal codes
    on the local file system.

    Returns:
        bool: True if the reference set of US postal codes are present
              on the local file system, otherwise False.

    """
    return os.path.isfile(settings.DB)

def remove():
    """Remove the reference set of US postal codes from the local file
    system.
    """
    if exists():
        os.remove(settings.DB)

def update():
    "Remove then Download the reference set of US postal codes."
    remove()
    download()

def load():
    """Ensure we have a copy of the reference US postal codes on the
    local file system then parse and return an array of those postal
    codes.

    Returns:
        list (ZipCode): the reference us postal codes

    """
    if not exists():
        download()
    return read()

