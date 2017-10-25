import stomp, gzip, StringIO, xml


class MyListener(object):
        #
        # def __init__ (self, conn):
        #       self._conn = conn

        def on_error(self, headers, message):
                print('received an error %s' % message)

        def on_message(self, headers, message):
                fp = gzip.GzipFile(fileobj=StringIO.StringIO(message))
                text = fp.readlines()
                fp.close()
                print text


if __name__ == '__main__':
    conn = stomp.Connection([('datafeeds.nationalrail.co.uk', 61613)]
                            )

    conn.set_listener('', MyListener())
    conn.start()
    conn.connect(username='d3user',
                 passcode='d3password',
                 wait=False)

    conn.subscribe(destination='/queue/D3907cbe2b-2a58-4c75-add3-850d1bdaa60b',
                   id=1, ack='auto')

    conn.disconnect()
