

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


