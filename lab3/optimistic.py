import hazelcast
import time

from hazelcast.util import validate_serializer


def optimistic_blocking():
    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map")
    key = 1
    map.put(key,0)
    for i in range(15):
        print('i: ', i)
        
        while True:
            old_value = map.get(key)
            new_value = old_value
            time.sleep(10)
            new_value += 1
            if map.replace_if_same(key, old_value, new_value):
                break
        
    print('total', client.get_map("my-distributed-map").get(key).result())

if __name__ == "__main__":
    optimistic_blocking()
