import pymssql

def get_connection():
    return pymssql.connect(
        server='localhost',
        user='sa',
        password='YourStrong@Passw0rd',
        database='huella'
    )
