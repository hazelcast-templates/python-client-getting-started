import hazelcast

from config import client_config

####################################

# Connect to your Hazelcast Cluster
client = hazelcast.HazelcastClient(client_config)

# take actions
print("Welcome to your Hazelcast Viridian Cluster!")

# Shutdown the client connection
client.shutdown()