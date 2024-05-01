

async def ExibirAtividades(conn, ID): 
    cursor = conn.cursor()
    cursor.execute("select * FROM Atividades WHERE Turma_ID = %s", (ID,))
    atividades = cursor.fetchall()
    cursor.close()
    return atividades

async def CriarAtividades(nome, data_criacao, data_entrega, turma_id, conn): 
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Atividades(nome, Data_Criacao, Data_Entrega, Turma_ID) VALUES  (%s, %s, %s, %s)", (nome, data_criacao, data_entrega, turma_id))
    conn.commit()  
    return {"message": "Turma inserida com sucesso"}

async def ConfirmacaoDeletarAtividade(atividade_id, conn):
    cursor = conn.cursor()
    cursor.execute("select ID, Nome FROM atividades WHERE ID = %s", (atividade_id))
    atividadeDeletada = cursor.fetchone()
    cursor.close()
    return atividadeDeletada

async def DeletarAtividadeDefinitivo(atividade_id, conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Atividades WHERE ID = %s", (atividade_id))
    conn.commit() 
    return True 