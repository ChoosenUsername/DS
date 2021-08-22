import hazelcast
import time

from hazelcast.util import validate_serializer


def optimistic_blocking():
    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map").blocking()

    key = 1
    for i in range(100):
        print('i: ', i)
        
        while True:
            old_value = map.get(key)
            new_value = old_value
            time.sleep(1.5)
            new_value += 1
            if map.replace_if_same(key, old_value, new_value):
                break

    print('total', client.get_map("my-distributed-map").get(key).result())

if __name__ == "__main__":
    optimistic_blocking()
