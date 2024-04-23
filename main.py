from fastapi import FastAPI, HTTPException, Form
import pymysql
import pymysql.cursors
from fastapi.templating import Jinja2Templates
from fastapi import Request
import Turmas
import Usuarios 
import Professores
from datetime import date

# Configuração do FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="C:\\Users\\FALCAO.GABRIEL\\Desktop\\Gabriel\\SENAI\\SimuladoSAEP")


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
        usuarioExiste = await Usuarios.VerificarUsuario(email, senha, conn)
        if usuarioExiste == True:
                nome_usuario, professorID = await Professores.IdentificarProfessor(email, conn)
                turmas = await Turmas.ExibirTurmas(professorID, conn)
                return templates.TemplateResponse("Turmas.html", {"request": request, "nome_usuario": nome_usuario, "professorID": professorID, "turmas": turmas})
        else:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.post("/api/visualizar")
async def visualizar():
    return "message: Tela renderizada som sucesso"

@app.post("/api/NovaTurma")
async def nova_turma(request: Request):
    return templates.TemplateResponse("CriarTurma.html", {"request": request})

@app.post("/api/CriarTurma")
async def nova_turma(request: Request, nome: str = Form(...), data: date = Form(...), professorID: int = Form(...)):
    await Turmas.CriarTurmas(nome, data, professorID, conn)
    nome_usuario, professorID = await Professores.IdentificarProfessorID(professorID, conn)
    turmas = await Turmas.ExibirTurmas(professorID, conn)
    return templates.TemplateResponse("Turmas.html", {"request": request, "nome_usuario": nome_usuario, "professorID": professorID, "turmas": turmas})

@app.post("/api/DeletarTurma/")
async def nova_turma(request: Request, turma_id: str = Form(...)):
    turmaDeletada = await Turmas.ConfirmacaoDeletarTurma(turma_id, conn)
    turma_nome = turmaDeletada['Nome']
    return templates.TemplateResponse("DeletarTurma.html", {"request": request, "turma_id": turma_id, "turma_nome": turma_nome})
    #criar função assíncrona para ler a turma 
    #chamar tela de confirmação '
    #criar função 
    #criar função assíncrona para deletar a turma, chamando a url app.delete(/api/DeletarTurma/id)
    
@app.delete("/api/DeletarTurma/{id}")
async def delete_item(item_id: int):
    query = "DELETE FROM items WHERE id = %s"
    cursor = conn.cursor()
    values = (item_id,)
    cursor.execute(query, values)
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": "Item deletado com sucesso"}

