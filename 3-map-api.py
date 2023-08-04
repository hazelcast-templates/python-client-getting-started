import hazelcast
import os

from config import client_config

####################################

# Connect to your Hazelcast Cluster
client = hazelcast.HazelcastClient(client_config)

# Create a map on the cluster
cities_map = client.get_map('cities').blocking()

# Clear the map
cities_map.clear()

# Add some data
cities_map.put(1, "London")
cities_map.put(2, "New York")
cities_map.put(3, "Tokyo")

# Output the data
entries = cities_map.entry_set()

for key, value in entries:
    print(f"{key} -> {value}")

# Shutdown the client connection
client.shutdown()