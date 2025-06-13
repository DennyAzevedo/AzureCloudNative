import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()
BlobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
BlobContainerName = os.getenv("BLOB_CONTAINER_NAME")
BlobAccountName = os.getenv("BLOB_ACCOUNT_NAME")

SQLServer = os.getenv("SQL_SERVER")
SQLDatabase = os.getenv("SQL_DATABASE")
SQLUser = os.getenv("SQL_USER")
SQLPassword = os.getenv("SQL_PASSWORD")

st.title("Cadastro de Produtos")
# Formulário de Cadastro de Produto
product_name = st.text_input("Nome do Produto")
product_description = st.text_area("Descrição do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

#Save image on blob storage
def upload_blob(file):
	blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
	container_client = blob_service_client.get_container_client(BlobContainerName)
	blob_name = str(uuid.uuid4()) + file.name  # Generate a unique blob name
	blob_client = container_client.get_blob_client(blob_name)
	blob_client.upload_blob(file.read(), overwrite=True)
	image_url = f"https://{BlobAccountName}.blob.core.windows.net/{BlobContainerName}/{blob_name}"
	return image_url

if st.button("Cadastrar Produto"):
	if product_image is not None:
		image_url = upload_blob(product_image)
		return_message = f"Produto cadastrado com sucesso! Imagem disponível em: {image_url}"
	else:
		return_message = "Produto cadastrado com sucesso! (sem imagem)"

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
	return_message = "Lista de produtos carregada com sucesso!"