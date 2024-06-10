import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Retrieve the file from the request
        file = req.files['file']
        file_content = file.stream.read()
        file_name = file.filename

        # Set up Azure Blob Storage connection
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

        # Upload the file to Blob Storage
        blob_client.upload_blob(file_content, overwrite=True)

        return func.HttpResponse(f"File {file_name} uploaded successfully.", status_code=200)

    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        return func.HttpResponse("Failed to upload file.", status_code=500)
