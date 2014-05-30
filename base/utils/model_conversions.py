from pickle import loads

def db_to_model(db_object):
    return None

def cache_to_model(cache_object):
    return loads(cache_object)
