from uuid import uuid1


def upload_file(file):
    url = 'http://default-url.net/' + str(uuid1()) + '/' + str(file)
    print 'uploading file ' + str(file) + ' to ' + url
    print ' ... ... ... Done!'
    return url

def delete_file(url):
    print 'deleting file at ' + url
    print ' ... ... ... Done!'
    return True
