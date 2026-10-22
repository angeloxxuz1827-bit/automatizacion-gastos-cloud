import os

# `.env` solo existe en desarrollo local. En Lambda no hay `.env` y el paquete
# `python-dotenv` no está instalado, así que el import es opcional.
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv()

# Telegram. La constante y la variable se llaman distinto a propósito:
# `ingestion/telegram/client.py` importa `TELEGRAM_TOKEN`.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = os.getenv("TELEGRAM_API_URL")

# Groq.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")

# S3 (Lambda de ingestion).
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Supabase (Lambda de store). El dashboard nuevo entrega `SUPABASE_SECRET_KEY`;
# el nombre legacy es `SUPABASE_SERVICE_ROLE_KEY`. Se acepta cualquiera de los dos.
# La secret key es sensible: vive solo en variables de entorno o en `.env`.
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY")
SUPABASE_SECRET_KEY = (
    os.getenv("SUPABASE_SECRET_KEY")
    or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)
SUPABASE_JWKS_URL = os.getenv("SUPABASE_JWKS_URL")

# MySQL/RDS legado. El store ya no usa estas variables; se conservan mientras
# exista `python/aws/rds/` como referencia de la migración.
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
USER_NAME = os.getenv("USER_NAME")
