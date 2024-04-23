async def IdentificarProfessor(email, conn): 
    cursor = conn.cursor()
    cursor.execute("SELECT Professores.Nome, Professores.ID FROM Professores LEFT JOIN Usuarios ON Professores.Usuario_ID = Usuarios.ID WHERE Usuarios.email = %s", (email,))
    row = cursor.fetchone()
    nome_usuario = row["Nome"] 
    professorID = row["ID"]
    return nome_usuario, professorID

async def IdentificarProfessorID(id, conn): 
    cursor = conn.cursor()
    cursor.execute("SELECT Professores.Nome, Professores.ID FROM Professores WHERE Professores.ID = %s", (id,))
    row = cursor.fetchone()
    nome_usuario = row["Nome"] 
    professorID = row["ID"]
    return nome_usuario, professorID