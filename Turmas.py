import Professores

async def ExibirTurmas(professorID, conn): 
    cursor = conn.cursor()
    cursor.execute("select Turmas.ID, Professores.Nome, turmas.nome, turmas.Data_Criacao, Professores.Usuario_ID "+
                                    "FROM Turmas " +
                                    "LEFT JOIN Professores ON Turmas.Professor_ID = Professores.ID " +
                                    "Where Turmas.Professor_ID = %s", (professorID,))
    turmas = cursor.fetchall()
    cursor.close()
    return turmas


async def CriarTurmas(nome, data, professorID, conn): 
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Turmas(nome, Data_Criacao, Professor_ID) VALUES  (%s, %s, %s)", (nome, data, professorID))
    conn.commit()  
    return {"message": "Turma inserida com sucesso"}

async def ConfirmacaoDeletarTurma(turma_id, conn):
    cursor = conn.cursor()
    cursor.execute("select ID, Nome FROM Turmas WHERE ID = %s", (turma_id))
    turmaDeletada = cursor.fetchone()
    cursor.close()
    return turmaDeletada

async def DeletarTurmaDefinitivo(turma_id, conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Turmas WHERE ID = %s", (turma_id))
    conn.commit() 
    return True 

