import hazelcast
import time

from hazelcast.util import validate_serializer


def pessimistic_blocking():
    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map").blocking()

    for i in range(100):
        print('i: ', i)
        map.lock(i)
        
        value = map.get(i)
        time.sleep(0.5)
        value += 1
        map.put(i, value)
        map.unlock(i)
    print('total', client.get_map("my-distributed-map").get(i).result())

if __name__ == "__main__":
    pessimistic_blocking()
        