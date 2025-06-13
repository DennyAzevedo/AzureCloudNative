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

product_name = st.text_input("Nome do Produto")
product_description = st.text_area("Descrição do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

if st.button("Cadastrar Produto"):
	return_message = "Produto cadastrado com sucesso!"

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
	return_message = "Lista de produtos carregada com sucesso!"