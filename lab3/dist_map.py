import hazelcast

# Start the Hazelcast Client and connect to an already running Hazelcast Cluster on 127.0.0.1
client = hazelcast.HazelcastClient()
# Get the Distributed Map from Cluster.
my_map = client.get_map("my-distributed-map").blocking()

for i in range(100):
    my_map.put(i,i)
    
print("finished")
client.shutdown()
