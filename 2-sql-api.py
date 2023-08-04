import hazelcast
from hazelcast import HazelcastClient
from hazelcast.serialization.api import CompactReader, CompactSerializer, CompactWriter
import os
import typing

from config import client_config

class City:
    def __init__(self, country: str, city: str, population: int) -> None:
        self.country = country
        self.city = city
        self.population = population

class CitySerializer(CompactSerializer[City]):
    def read(self, reader: CompactReader) -> City:
        city = reader.read_string("city")
        country = reader.read_string("country")
        population = reader.read_int32("population")
        return City(country, city, population)

    def write(self, writer: CompactWriter, obj: City) -> None:
        writer.write_string("country", obj.country)
        writer.write_string("city", obj.city)
        writer.write_int32("population", obj.population)

    def get_type_name(self) -> str:
        return "city"

    def get_class(self) -> typing.Type[City]:
        return City

def create_mapping(client: HazelcastClient) -> None:
    print("Creating the mapping...", end="")
    # See: https://docs.hazelcast.com/hazelcast/latest/sql/mapping-to-maps
    mapping_query = """
        CREATE OR REPLACE MAPPING
            cities (
                __key INT,
                country VARCHAR,
                city VARCHAR,
                population INT) TYPE IMAP
            OPTIONS (
                'keyFormat' = 'int',
                'valueFormat' = 'compact',
                'valueCompactTypeName' = 'city')
    """
    client.sql.execute(mapping_query).result()
    print("OK.")

def populate_cities(client: HazelcastClient) -> None:
    print("Inserting data...", end="")

    insert_query = """
        INSERT INTO cities
        (__key, city, country, population) VALUES
        (1, 'London', 'United Kingdom', 9540576),
        (2, 'Manchester', 'United Kingdom', 2770434),
        (3, 'New York', 'United States', 19223191),
        (4, 'Los Angeles', 'United States', 3985520),
        (5, 'Istanbul', 'Türkiye', 15636243),
        (6, 'Ankara', 'Türkiye', 5309690),
        (7, 'Sao Paulo ', 'Brazil', 22429800)
    """

    try:
        client.sql.execute('DELETE from cities').result()
        client.sql.execute(insert_query).result()
        print("OK.")
    except Exception as e:
        print(f"FAILED: {e!s}.")

def fetch_cities(client: HazelcastClient) -> None:
    print("Fetching cities...", end="")
    result = client.sql.execute("SELECT __key, this FROM cities").result()
    print("OK.")

    print("--Results of 'SELECT __key, this FROM cities'")
    print(f"| {'id':>4} | {'country':<20} | {'city':<20} | {'population':<15} |")

    for row in result:
        city = row["this"]
        print(
            f"| {row['__key']:>4} | {city.country:<20} | {city.city:<20} | {city.population:<15} |"
        )

####################################

# Register Compact serializer of City class
client_config.compact_serializers = [CitySerializer()]
# Connect to your Hazelcast Cluster
client = hazelcast.HazelcastClient(client_config)

# Create a map on the cluster
create_mapping(client)

# Add some data
populate_cities(client)

# Output the data
fetch_cities(client)

# Shutdown the client connection
client.shutdown()