from uuid import uuid1
import re
import boto
from boto.s3.key import Key

AWSAccessKeyId='AKIAJSQ5UF3IOBMZTRLA'
AWSSecretKey='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'
bucket_name = 'idc-cloud-ex2-bucket'


connection = boto.connect_s3(AWSAccessKeyId, AWSSecretKey)
bucket = connection.get_bucket(bucket_name)


def upload_file(file):
#    url = 'http://default-url.net/' + str(uuid1()) + '/' + str(file)
 #   print 'uploading file ' + str(file) + ' to ' + url
  #  print ' ... ... ... Done!'
   # return url
    k = Key(bucket)
    k.key = str(uuid1()) + '.' + str(file)
    k.set_contents_from_file(file)
    return k.generate_url(expires_in=1*60*60*24)


def delete_file(url):
#    print 'deleting file at ' + url
 #   print ' ... ... ... Done!'
    k = Key(bucket)
    key_name = deduce_key_name(url)
    k.key = key_name
    k.delete()

regex = u's3.amazonaws.com/(.+)\?'
def deduce_key_name(url):
    match = re.search(regex, url)
    key_name = match.groups(1)
    return key_name
