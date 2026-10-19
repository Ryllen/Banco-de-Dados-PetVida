import pyodbc
from contextlib import contextmanager
def montar_connection_string():
    return (
        r"DRIVER={ODBC Driver 18 for SQL Server};"
        r"SERVER=localhost\SQLEXPRESS;"
        r"DATABASE=PetVida;"
        r"Trusted_Connection=yes;"
        r"TrustServerCertificate=yes;"       
    )

def conectar():
    return pyodbc.connect(
        montar_connection_string(),
        autocommit=False
    )

def testar_conexao():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT @@SERVERNAME AS servidor, DB_NAME() AS banco, @@VERSION AS versao")
        return cursor.fetchone()
    finally:
        conn.close()

@contextmanager
def transacao():
    conn = conectar()
    cursor = conn.cursor()
    try:
        # entrega o cursor para quem chamou a função
        yield cursor
        conn.commit()
    except:
        # se aconteceu erro, desfaz
        conn.rollback()
        #raise iforma o erro 
        raise
    finally:
        cursor.close()
        conn.close()