from http.client import HTTPException
import json
import boto3
from botocore.exceptions import ClientError
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
log = logging.getLogger(__name__)

def getSecretManagerDB():
    secret_name = "rds!cluster-9b4b7cd8-22ee-48ff-bbc4-d1f43ddf3bc8"
    region_name = "us-east-1"   
    
    try:
        client = boto3.client("secretsmanager", region_name=region_name)
        response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response["SecretString"])
        return secret
    except ClientError as e:
        log.error(f"Error{e}")
        return None
    

# db_credentials = getSecretManagerDB()
# DB_HOST = "cluster-gamer-vault-instance-1.c6r6ws4k4vwo.us-east-1.rds.amazonaws.com"
# DB_USER = db_credentials["username"]
# DB_PASS = db_credentials["password"]
# DB_NAME = 'gamervaultlts'

DB_HOST = "localhost:8400"
DB_USER = "admin"
DB_PASS = ">fc-liyYi[v4Dlh6Pc0m_FwZ>pE#"
DB_NAME = 'gamervaultlts'

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
Base = declarative_base()

    
def get_db():
    try:
        log.info("Obteniendo sesion de Base de Datos")
        yield db
    except Exception as e:
        log.error(str(e))
        db.close()
        raise HTTPException(status_code=500, detail='ERROR - DATABASE FAIL')
    finally:
        db.close()

def verify_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            log.info("Conexion exitosa")
        return True
    except Exception as e:
        log.critical(f"No se pudo conectar a la base de datos: {str(e)}")
        return False
    
    
verify_db_connection()