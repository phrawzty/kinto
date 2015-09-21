class PreBucket(object):
    def __init__(self, bucket_id, request):
        self.bucket_id = bucket_id
        self.request = request


class PostBucket(object):
    def __init__(self, bucket_id, request):
        self.bucket_id = bucket_id
        self.request = request


class Bucket(object):
    def __init__(self, bucket_id, when, request):
        self.bucket_id = bucket_id
        self.when = when
        self.request = request
