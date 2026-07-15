# from pymilvus import connections, utility

# # Connect to Milvus
# connections.connect(
#     alias="default",
#     host="localhost",
#     port="19530"
# )

# print("✅ Connected to Milvus")

# # Get server version
# print("Server Version:", utility.get_server_version())

# # List all collections
# collections = utility.list_collections()

# # print("Collections:", collections)

from pymilvus import MilvusClient

client = MilvusClient("http://localhost:19530")

print(client.list_collections())