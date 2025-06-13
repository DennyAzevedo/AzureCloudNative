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

def insert_product(product_name, product_description, product_price, product_image):
	try:
		image_url = upload_blob(product_image)
		conn = pymssql.connect(server=SQLServer, user=SQLUser, password=SQLPassword, database=SQLDatabase)
		cursor = conn.cursor()
		insert_query = """INSERT INTO produtos (nome, descricao, preco, imagem_url) VALUES (%s, %s, %s, %s)"""
		cursor.execute(insert_query, (product_name, product_description, product_price, image_url))
		conn.commit()
		conn.close()

		return True
	except Exception as e:
		st.error(f"Erro ao cadastrar produto: {e}")
		return False

def lista_produtos():
	try:
		conn = pymssql.connect(server=SQLServer, user=SQLUser, password=SQLPassword, database=SQLDatabase)
		cursor = conn.cursor()
		select_query = "SELECT nome, descricao, preco, imagem_url FROM produtos"
		cursor.execute(select_query)
		products = cursor.fetchall()
		conn.close()
		return products
	except Exception as e:
		st.error(f"Erro ao listar produtos: {e}")
		return []

def lista_produtos_tela():
	products = lista_produtos()
	if products:
		st.write("Lista de Produtos:")
		for product in products:
			st.write(f"**Nome:** {product[0]}")
			st.write(f"**Descrição:** {product[1]}")
			st.write(f"**Preço:** R$ {product[2]:.2f}")
			if product[3]:
				st.image(product[3])
			st.write("---")
	else:
		st.write("Nenhum produto cadastrado.")

if st.button("Cadastrar Produto"):
	if product_image is not None:
		insert_product(product_name, product_description, product_price, product_image)
		return_message = "Produto cadastrado com sucesso! Imagem disponível."
	else:
		return_message = "Produto cadastrado com sucesso! (sem imagem)"

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
	lista_produtos_tela()
	return_message = "Lista de produtos carregada com sucesso!"
