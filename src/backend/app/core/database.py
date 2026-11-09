from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import get_settings

settings = get_settings()

# Un pool acotado evita abrir una conexion nueva por peticion (menos CPU y
# memoria en PostgreSQL) y `pool_recycle` descarta conexiones que el servidor
# ya cerro por inactividad.
_POOL_OPCIONES = {
    "pool_pre_ping": True,
    "pool_size": 10,
    "max_overflow": 20,
    "pool_timeout": 30,
    "pool_recycle": 1800,
}

def get_database_url(test: bool = False) -> str:
    db_name = settings.DB_NAME_TEST if test else settings.DB_NAME
    return f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{db_name}"

engine = create_engine(get_database_url(), **_POOL_OPCIONES)
TestingEngine = create_engine(get_database_url(test=True), **_POOL_OPCIONES)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestingEngine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# `create_all` no agrega indices a tablas que ya existen. Estas sentencias son
# idempotentes y dejan una base creada antes de esta optimizacion con el mismo
# esquema que una base nueva.
_INDICES = (
    "CREATE INDEX IF NOT EXISTS ix_usuarios_id_rol ON usuarios (id_rol)",
    "CREATE INDEX IF NOT EXISTS ix_puntos_entrega_operador_fecha "
    "ON puntos_entrega (id_operador, fecha_registro)",
    "CREATE INDEX IF NOT EXISTS ix_rutas_id_vehiculo ON rutas (id_vehiculo)",
    "CREATE INDEX IF NOT EXISTS ix_rutas_operador_fecha "
    "ON rutas (id_operador, fecha_generacion)",
    "CREATE INDEX IF NOT EXISTS ix_rutas_estado ON rutas (estado)",
    "CREATE INDEX IF NOT EXISTS ix_ruta_puntos_punto ON ruta_puntos (id_punto)",
)

def init_db(test: bool = False):
    motor = TestingEngine if test else engine
    Base.metadata.create_all(bind=motor)
    with motor.begin() as conexion:
        for sentencia in _INDICES:
            conexion.execute(text(sentencia))