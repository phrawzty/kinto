class KintoBroker(object):
    def bucket(self, event):
        bucket = event.bucket_id
        method = event.request.method
        when = event.when

        if when == 'pre':
            print('TRY'),
        elif when == 'post':
            print('SUCCESS'),
        else:
            print('WTF'),

        print 'Bucket:', bucket, 'with method:', method
