import hazelcast
import time


client = hazelcast.HazelcastClient()
queue = client.get_queue("my-distributed-queue").blocking()

for i in range(15):
    queue.put( i )
    time.sleep(5)
queue.put( -1 )

