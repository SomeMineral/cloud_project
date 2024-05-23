from flask import *
import boto3, json, os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Git
GIST_ID = "a9d6acbaf78e4d82a4dcf858ba3652ea"
GITHUB_TOKEN = os.environ.get("GIST_TOKEN")

# AWS 자격 증명 및 S3 클라이언트 생성
session2 = boto3.Session()
s3_client = session2.client('s3')
S3_BUCKET = 'ssgpang-bucket2'

# Azure Blob Storage 연결 설정
CONNECTION_STRING = os.environ.get("AZURE_CONNECTION_STRING")
# CONNECTION_STRING = ""
CONTAINER_NAME = "ssgpangcontainer"

# Blob 서비스 클라이언트 생성
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# AWS S3 Image URL
def get_public_url(bucket_name, key) :
    # S3 객체에 대한 공개적인 URL 생성
    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': key},
        ExpiresIn=3600  # URL의 유효기간 설정 (초 단위)
    )
    return url

# Azure Blob Storage Image URL
def get_public_url_azure(container_name, blob_name):
    blob_client = BlobClient.from_connection_string(
        CONNECTION_STRING, container_name, blob_name
    )
    url = blob_client.url
    return url


# JSON 파일 읽기
def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data