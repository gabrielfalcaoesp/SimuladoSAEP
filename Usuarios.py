async def VerificarUsuario(email, senha, conn): 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE email = %s AND senha = %s", (email, senha))
    usuarioExiste = cursor.fetchone()
    cursor.close()
    if usuarioExiste is not None:
        return True
    else:
        return False
