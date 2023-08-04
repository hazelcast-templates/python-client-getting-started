import hazelcast
import os

from config import client_config

def entry_added(event):
    print(f"Entry added with key: {event.key}, value: {event.value}")

def entry_removed(event):
    print(f"Entry removed with key: {event.key}")

def entry_updated(event):
    print(f"Entry updated with key: {event.key}, old value: {event.old_value}, new value: {event.value}")

####################################

# Connect to your Hazelcast Cluster
client = hazelcast.HazelcastClient(client_config)

# Create a map on the cluster
cities_map = client.get_map('cities').blocking()

# Add listeners
cities_map.add_entry_listener(
    include_value=True, added_func=entry_added, removed_func=entry_removed, updated_func=entry_updated
)

# Clear the map
cities_map.clear()

# Add some data
cities_map.set(1, "London")
cities_map.set(2, "New York")
cities_map.set(3, "Tokyo")

cities_map.remove(1)
cities_map.replace(2, "Paris")

# Output the data
entries = cities_map.entry_set()

for key, value in entries:
    print(f"{key} -> {value}")

# Shutdown the client connection
client.shutdown()