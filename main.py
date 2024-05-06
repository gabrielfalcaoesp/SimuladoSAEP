from fastapi import FastAPI, HTTPException, Form
import pymysql
import pymysql.cursors
from fastapi.templating import Jinja2Templates
from fastapi import Request
import Turmas
import Usuarios 
import Professores
import Atividades
from datetime import date
from fastapi.responses import RedirectResponse
from typing import List
import starlette.status as status
from urllib.parse import urlencode

# Configuração do FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")
emailUsuario = ""

# Conexão com o banco de dados
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="SAEP_novo",
    cursorclass=pymysql.cursors.DictCursor 
)

@app.get("/")
async def redirect_to_home(request: Request):
    return templates.TemplateResponse("Index.html", {"request": request})




@app.post("/api/Index")
async def index(request: Request):
    global emailUsuario

    emailUsuario = ""
    return templates.TemplateResponse("Index.html", {"request": request})



@app.post("/api/login")
async def login(request: Request, email: str = Form(...), senha: str = Form(...)):
    global emailUsuario

    with conn.cursor() as cursor:
        usuarioExiste = await Usuarios.VerificarUsuario(email, senha, conn)
        if usuarioExiste:
            emailUsuario = email


            redirect_url = f"/Turmas"

            return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
        else:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")  
        
        

        
        
    






@app.post("/api/atividades")
async def visualizar(request: Request, turma_id: str = Form(...)):
    atividades = await Atividades.ExibirAtividades(conn, turma_id)
    return templates.TemplateResponse("Atividades.html", 
                                      {"request": request,
                                       "turma_id": turma_id,
                                       "atividades": atividades})
    
  
  
@app.post("/api/NovaAtividade")
async def nova_atividade(request: Request, turma_id: str = Form(...)):
    return templates.TemplateResponse("CriarAtividade.html", {"request": request, "turma_id": turma_id})  

@app.post("/api/CriarAtividade")
async def criar_Atividade(request: Request, nome: str = Form(...), data_criacao: date = Form(...), data_entrega: date = Form(...), turma_id: str = Form(...)):
    await Atividades.CriarAtividades(nome, data_criacao, data_entrega, turma_id, conn)
    return RedirectResponse(url="/api/atividades")

@app.post("/api/DeletarAtividade/")
async def deletar_Atividade(request: Request, atividade_id: str = Form(...)):
    atividadeDeletada = await Atividades.ConfirmacaoDeletarAtividade(atividade_id, conn)
    atividade_nome = atividadeDeletada['Nome']
    return templates.TemplateResponse("DeletarAtividade.html", {"request": request, "atividade_id": atividade_id, "atividade_nome": atividade_nome})
    
@app.post("/api/DeletarAtividade/{item_id}")
async def delete_Atividade(request: Request, item_id: int):
    deleteCompleto = await Atividades.DeletarAtividadeDefinitivo(item_id, conn)
    if deleteCompleto == True:
        redirect_url = f"/Turmas"
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
    else:
        return "message: Houve um erro"










@app.post("/Turmas")
async def turmas(request: Request):
    redirect_url = f"/Turmas"
    return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)

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
@app.post("/api/NovaTurma")
async def nova_turma(request: Request):
    return templates.TemplateResponse("CriarTurma.html", {"request": request})

@app.post("/api/CriarTurma")
async def criar_turma(request: Request, nome: str = Form(...), data: date = Form(...), professorID: int = Form(...)):
    await Turmas.CriarTurmas(nome, data, professorID, conn)
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
    
