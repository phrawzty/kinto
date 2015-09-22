class KintoBroker(object):
    def trigger(self, event):
        print '###', event.msg
