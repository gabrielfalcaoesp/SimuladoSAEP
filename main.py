from fastapi import FastAPI, HTTPException, Form
import pymysql
import pymysql.cursors
from fastapi.templating import Jinja2Templates
from fastapi import Request
import Turmas
import Usuarios 
import Professores
from datetime import date
from fastapi.responses import RedirectResponse
from typing import List
import starlette.status as status
from urllib.parse import urlencode

# Configuração do FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="C:\\Users\\Aluno 25\\Desktop\\SimuladoSAEP")

emailUsuario = ""
senhaUsuario = ""


# Conexão com o banco de dados
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="SAEP_novo",
    cursorclass=pymysql.cursors.DictCursor 
)

@app.post("/api/login")
async def login(request: Request, email: str = Form(...), senha: str = Form(...)):
    global emailUsuario, senhaUsuario

    with conn.cursor() as cursor:
        usuarioExiste = await Usuarios.VerificarUsuario(email, senha, conn)
        if usuarioExiste:
            emailUsuario = email
            senhaUsuario = senha

            redirect_url = f"/Turmas"

            return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
        else:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")  

@app.get("/Turmas")
async def visualizar_turmas(request: Request):
    global emailUsuario
    nome_usuario, professorID = await Professores.IdentificarProfessor(emailUsuario, conn)
    if nome_usuario is None or professorID is None:
        raise HTTPException(status_code=400, detail="Parâmetros ausentes na URL")

    # Obtenha as turmas usando o professorID
    turmas = await Turmas.ExibirTurmas(professorID, conn)

    # Renderize o template com os dados recebidos
    return templates.TemplateResponse("Turmas.html", 
                                      {"request": request,
                                       "nome_usuario": nome_usuario,
                                       "professorID": professorID,
                                       "turmas": turmas})
    
@app.post("/api/visualizar")
async def visualizar():
    return "message: Tela renderizada som sucesso"

@app.post("/api/NovaTurma")
async def nova_turma(request: Request):
    return templates.TemplateResponse("CriarTurma.html", {"request": request})

@app.post("/api/CriarTurma")
async def criar_turma(request: Request, nome: str = Form(...), data: date = Form(...), professorID: int = Form(...)):
    await Turmas.CriarTurmas(nome, data, professorID, conn)
    nome_usuario, professorID = await Professores.IdentificarProfessorID(professorID, conn)
    turmas = await Turmas.ExibirTurmas(professorID, conn)
    redirect_url = f"/Turmas"
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

@app.post("/api/DeletarTurma/")
async def deletar_turma(request: Request, turma_id: str = Form(...)):
    turmaDeletada = await Turmas.ConfirmacaoDeletarTurma(turma_id, conn)
    turma_nome = turmaDeletada['Nome']
    return templates.TemplateResponse("DeletarTurma.html", {"request": request, "turma_id": turma_id, "turma_nome": turma_nome})
    
@app.post("/api/DeletarTurma/{item_id}")
async def delete_item(request: Request, item_id: int):
    deleteCompleto = await Turmas.DeletarTurmaDefinitivo(item_id, conn)
    if deleteCompleto == True:
        redirect_url = f"/Turmas"
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
    else:
        return "message: Houve um erro"