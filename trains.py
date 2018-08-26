import stomp
import gzip
from io import StringIO
import json


def get_credentials():
    with open('creds.json') as f:
        creds = json.load(f)
    return creds


class MyListener(object):

        def on_error(self, headers, message):
                print('received an error %s' % message)

        def on_message(self, headers, message):
                fp = gzip.GzipFile(fileobj=StringIO.StringIO(message))
                text = fp.readlines()
                fp.close()
                print('%s\n' % text)


if __name__ == '__main__':
    conn = stomp.Connection([('datafeeds.nationalrail.co.uk', 61613)])

    conn.set_listener('', MyListener())
    conn.start()
    conn.connect(username='d3user', passcode='d3password', wait=False)
    creds = get_credentials()
    print(creds)

    conn.subscribe(destination='/queue/{0}'.format(creds['queue_id']),
                   id=1, ack='auto')

    # mydata = raw_input('Prompt :')

    conn.disconnect()
