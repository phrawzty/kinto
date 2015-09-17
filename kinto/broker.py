class KintoBroker(object):
    def __init__(self):
        pass

    def on_bucket_created(self, event):
        bucket = event.bucket_id

        print 'You created a bucket called:', bucket
