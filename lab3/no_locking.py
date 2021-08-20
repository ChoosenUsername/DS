import hazelcast
import time

from hazelcast.util import validate_serializer

def no_blocking():
    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map").blocking()

    for i in range(100):
        print('i: ', i)
        value = map.get(i)
        time.sleep(0.5)
        value += 1
        map.put(i, value)
    print('total', client.get_map("my-distributed-map").get(i).result())

if __name__ == "__main__":
    no_blocking()
