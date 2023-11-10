import time

from dotenv import load_dotenv
from os import getenv
from azure.storage.blob import BlobServiceClient, ContentSettings

load_dotenv()

connect_str = getenv("AZURE_STORAGE_CONNECTION_STRING")
base_url = getenv("BLOB_BASE_URL")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


container_client = blob_service_client.get_container_client("file")

# east asia is hk
# southeast asia ia sg

def upload(name: str , file: bytes) -> str: # type of file could be various
    headers = ContentSettings(content_disposition=f"inline; filename={name}") # when file is inline, the filename will not be parsed
    name = f"{hex(int(time.time()))[2:]}-{name}" 
    blob_client = container_client.get_blob_client(name)
    #blob_client = blob_service_client.get_blob_client(container="file", blob=name)
    #it seem that azure will set content-type to application/octet-stream and content-md5
    # we will ignore that as azure will set the same content-type and we do not need md5
    blob_client.upload_blob(file)
    blob_client.set_http_headers(headers)
    return f"{base_url}/file/{name}"

def delete(name: str) -> None:
    blob_client = blob_service_client.get_blob_client(container="file", blob=name)
    blob_client.delete_blob()

#blob_client = blob_service_client.get_blob_client(container="file", blob="hello.txt")