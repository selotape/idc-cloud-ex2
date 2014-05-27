import boto
from boto.s3.key import Key

import sys
import mimetypes
import email
import time
import types
from datetime import datetime, timedelta
from uuid import uuid1
import re
import secrets

connection = boto.connect_s3(secrets.AWSAccessKeyId, secrets.AWSSecretKey)
bucket = connection.get_bucket(secrets.bucket_name)


def upload_file(file):
    key = Key(bucket)
    key.key = str(uuid1()) + '.' + str(file)

    # set cache headers
    aggressive_headers = get_aggressive_cache_headers()
    key.metadata.update(aggressive_headers)
    key.set_contents_from_file(file)

    # key.copy(bucket_name, key, metadata=aggressive_headers, preserve_acl=True)

    return key.generate_url(expires_in=1*60*60*24)


def delete_file(url):
    key = Key(bucket)
    key_name = deduce_key_name(url)
    key.key = key_name
    key.delete()


#--- Helpers ----------------------------------------------
regex = u's3.amazonaws.com/(.+)\?'
def deduce_key_name(url):
    match = re.search(regex, url)
    key_name = match.groups(1)
    return key_name

def get_aggressive_cache_headers():
    cache_metadata = {}

    # HTTP/1.0 (5 years)
    cache_metadata['Expires'] = '%s GMT' %\
        (email.Utils.formatdate(
            time.mktime((datetime.now() +
            timedelta(days=365*5)).timetuple())))

    # HTTP/1.1 (5 years)
    cache_metadata['Cache-Control'] = 'max-age=%d, public' % (3600 * 24 * 360 * 5)

    return cache_metadata

