from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

# Configuração do FastAPI
app = FastAPI()

# Conexão com o banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="SAEP"
)

# Modelo para receber os dados do login
class Login(BaseModel):
    ID: int
    Email: str
    Senha: str

# Rota para autenticação
@app.post("/login")
async def login(login_data: Login):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuarios WHERE email = %s AND senha = %s", (login_data.email, login_data.senha))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # Autenticação bem-sucedida
        return {"mensagem": "Autenticação bem-sucedida"}
    else:
        # Autenticação falhou
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
