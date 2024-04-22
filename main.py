from fastapi import FastAPI, HTTPException, Form
import pymysql
import pymysql.cursors
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Configuração do FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="C:\\Users\\gabri\\OneDrive\\Área de Trabalho\\SAEP\\SimuladoSAEP")


# Conexão com o banco de dados
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="SAEP_novo",
    cursorclass=pymysql.cursors.DictCursor 
)

# Rota para autenticação
@app.post("/api/login")
async def login(request: Request, email: str = Form(...), senha: str = Form(...)):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Usuarios WHERE email = %s AND senha = %s", (email, senha))
        user = cursor.fetchone()

        if user:
            cursor.execute("SELECT Professores.Nome, Professores.ID FROM Professores LEFT JOIN Usuarios ON Professores.Usuario_ID = Usuarios.ID WHERE Usuarios.email = %s", (email,))
            row = cursor.fetchone()
            if row:
                nome_usuario = row["Nome"] 
                professorID = row["ID"]
                cursor.execute("select Professores.Nome, turmas.nome, turmas.Data_Criacao, Professores.Usuario_ID "+
                                    "FROM Turmas " +
                                    "LEFT JOIN Professores ON Turmas.Professor_ID = Professores.ID " +
                                    "Where Turmas.Professor_ID = %s", (professorID))
                turmas = cursor.fetchall()


                return templates.TemplateResponse("Turmas.html", {"request": request, "nome_usuario": nome_usuario, "professorID": professorID, "turmas": turmas})


        else:
            # Autenticação falhou
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
