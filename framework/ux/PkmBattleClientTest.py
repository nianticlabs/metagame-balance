
import time

from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey='VGC AI'.encode('utf-8'))
conn.send(('init', []))
conn.send('close')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()

time.sleep(1)

address = ('localhost', 6000)
conn = Client(address, authkey='VGC AI'.encode('utf-8'))
conn.send(('switch', []))
time.sleep(1)
conn.send(('switch', []))
time.sleep(1)
conn.send(('attack', []))
conn.send('close')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()
