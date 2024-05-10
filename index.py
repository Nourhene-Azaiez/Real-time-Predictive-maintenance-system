from elasticsearch import Elasticsearch

# Create an Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Define the index name
index_name = "indus"

# Check if the Elasticsearch index exists
if es.indices.exists(index=index_name):
    # Delete the index
    es.indices.delete(index=index_name)
    print(f"Index '{index_name}' has been deleted.")
else:
    print(f"Index '{index_name}' does not exist.")


# Define the mapping for Elasticsearch index
mapping = {
    "mappings": {
        "properties": {
         "UDI": { "type": "integer" },
         "Product ID":{"type": "keyword"},
         "Type":{"type":"keyword"},
         "Air temperature [K]":{"type":"float"},
         "Process temperature [K]":{"type":"float"},
         "Rotational speed [rpm]":{"type":"float"},
         "Torque [Nm]":{"type":"float"},
         "Tool wear [min]":{"type":"integer"},
         "Target":{"type":"integer"},
        #  "Prediction":{"type": "keyword"},
         }
    }
}
# Create the Elasticsearch index with the specified mapping of my data
es.indices.create(index=index_name, body=mapping)
