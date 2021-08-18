import hazelcast
import time


   
client = hazelcast.HazelcastClient()
queue = client.get_queue("my-distributed-queue").blocking()
while True:
    item = queue.take()
    print(item)
    if item == -1 :
        queue.put( -1 );
        break
    time.sleep(5)
        
print("finished")