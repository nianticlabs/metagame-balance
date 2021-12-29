
import time

from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey='VGC AI'.encode('utf-8'))
conn.send(('init', [1, 4, 1, 250, 150, 100, 100, 150, 2, 2, 2, 300]))
conn.send('close')
conn.close()

time.sleep(1)

address = ('localhost', 6000)
conn = Client(address, authkey='VGC AI'.encode('utf-8'))
conn.send(('switch', [0, 1, 0, 150, 150, 150, 150]))
conn.send(('switch', [1, 1, 0]))
conn.send(('attack', [0, 3, False]))
conn.send(('attack', [1, 3, True]))
conn.send(('event', ['hp', 0, 100]))
conn.send(('event', ['slp', 0, 2]))
conn.send('close')
conn.close()
