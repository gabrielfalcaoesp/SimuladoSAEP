from fastapi import FastAPI, HTTPException, Form
import pymysql
import pymysql.cursors

# Configuração do FastAPI
app = FastAPI()

# Conexão com o banco de dados
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="SAEP",
    cursorclass=pymysql.cursors.DictCursor  # Isso garante que os resultados sejam retornados como dicionários
)

# Rota para autenticação
@app.post("/api/login")
async def login(email: str = Form(...), senha: str = Form(...)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Usuarios WHERE email = %s AND senha = %s", (email, senha))
        user = cursor.fetchone()

        if user:
            cursor.execute("SELECT Professores.Nome FROM Professores LEFT JOIN Usuarios ON Professores.Usuario_ID = Usuarios.ID WHERE Usuarios.email = %s", (email,))
            row = cursor.fetchone()
            if row:
                nome_usuario = row["Nome"]  # Obtendo o nome do usuário
                return {"mensagem": f"Bem-vindo, {nome_usuario}!"}
            else:
                return {"mensagem": "Bem-vindo!"}  # Se não houver correspondência na tabela Professores
        else:
            # Autenticação falhou
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
