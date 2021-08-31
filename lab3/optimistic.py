import hazelcast
import time

from hazelcast.util import validate_serializer

def ris(my_map, key, old_value, new_value):
    if my_map.contains_key(key) and my_map.get(key) == old_value:
        my_map.put(key, new_value)
        return True
    else:
        return False

def optimistic_blocking():
    client = hazelcast.HazelcastClient()
    map = client.get_map("my-distributed-map").blocking()

    key = 1
    map.put_if_absent(key,0)
    for i in range(100):
        print('i: ', i)
        
        while True:
            old_value = map.get(key)
            new_value = old_value
            time.sleep(1.5)
            new_value += 1
            if ris(map, key, old_value, new_value):
                break

    print('total', client.get_map("my-distributed-map").get(key).result())

if __name__ == "__main__":
    optimistic_blocking()
