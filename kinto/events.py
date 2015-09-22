# This is where objects are constructed in order to pass to the Broker.


class Bucket(object):
    def __init__(self, bucket_id, when, request):
        self.msg = '%s %s on the %s bucket' % (when,
                                               request.method,
                                               bucket_id)


class Collection(object):
    def __init__(self, parent_id, collection_id, when, request):
        self.msg = '%s %s on the %s/%s collection' % (when,
                                                      request.method,
                                                      parent_id,
                                                      collection_id)


class Group(object):
    def __init__(self, parent_id, group_id, when, request):
        self.msg = '%s %s on the %s/%s group' % (when,
                                                 request.method,
                                                 parent_id,
                                                 group_id)


class Record(object):
    def __init__(self, parent_id, record_id, when, request):
        self.msg = '%s %s on the %s/%s record' % (when,
                                                  request.method,
                                                  parent_id,
                                                  record_id)
