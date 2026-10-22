# Expense Tracker Bot

Bot de Telegram que convierte mensajes en lenguaje natural (español) en gastos
estructurados. El procesamiento usa Groq y el pipeline corre sobre AWS Lambda,
API Gateway y S3; la persistencia objetivo es Supabase (Postgres).

> **Estado de esta revisión**
>
> Este commit consolida `python/` como código compartido de la Lambda Layer y
> actualiza ingestion y processor. El store versionado todavía usa RDS en este
> commit; su migración a Supabase se incorpora en el commit siguiente. Las
> secciones marcadas como objetivo describen el estado final de esa migración.

## Arquitectura

```text
Telegram
   │  POST update
   ▼
API Gateway HTTP API
   │  ANY /default/webhook-telegram-bot
   ▼
webhook-telegram-bot (ingestion)
   │  guarda raw/...json
   ▼
Amazon S3
   │  ObjectCreated: raw/*.json
   ▼
expense-processor
   │  Groq: extrae el gasto
   │  guarda processed/...json
   │  responde por Telegram
   ▼
Amazon S3
   │  ObjectCreated: processed/*.json
   ▼
expense-store
   │  lee processed/ y el raw/ original
   │  ejecuta la RPC registrar_gasto
   ▼
Supabase (Postgres)
   ├── clientes
   ├── mensajes
   └── gastos
```

En el estado final, cada Lambda contiene únicamente su entrypoint y, cuando
aplica, su `core/` propio. El código compartido (`aws/`, `config/`, `database/`,
`ingestion/`, `llm/`) vive una sola vez en `python/`, que es la raíz de la Lambda
Layer. En este commit, ingestion y processor ya usan la capa; el store todavía
conserva sus copias locales y se migra en el commit siguiente.

## Estructura del repositorio

```text
bot-telegram/
├── python/                         # Contenido de la Lambda Layer
│   ├── aws/
│   │   ├── s3/                     # Cliente, eventos y keys de S3
│   │   └── rds/                    # Implementación legado de RDS/MySQL
│   ├── config/
│   │   └── settings.py             # Variables de entorno
│   ├── database/                   # Cliente REST/RPC de Supabase
│   ├── ingestion/telegram/         # Cliente y servicio de Telegram
│   └── llm/                        # Cliente Groq y prompts
├── expense-ingestion-lambda/
│   └── lambda_function.py          # API Gateway -> S3 raw/
├── expense-procces-lambda/
│   ├── lambda_function.py          # S3 raw/ -> Groq -> S3 processed/
│   └── core/application.py
├── expense-store-lambda/
│   ├── lambda_function.py          # S3 processed/ -> Supabase
│   └── core/application.py
├── requirements-layer.txt          # Dependencias de la capa
├── supabase/schema.sql             # DDL, RLS y RPC (migración del store)
└── .env.example
```

El directorio `expense-procces-lambda` conserva esa grafía histórica.

No hay `infrastructure/`, `scripts/`, `tests/` ni CI en el repositorio. El
despliegue es manual desde la consola de AWS o con AWS CLI.

## Flujo

1. Telegram envía el update al webhook de API Gateway.
2. `webhook-telegram-bot` guarda el update crudo en `raw/`.
3. El evento de S3 invoca `expense-processor`.
4. `expense-processor` envía el mensaje a Groq, sobrescribe `ChatId`,
   `MessageId` y `Fecha` con los datos reales de Telegram y guarda la respuesta
   en `processed/`. Después envía la confirmación por Telegram.
5. El evento de S3 invoca `expense-store`.
6. `expense-store` lee el JSON procesado y el update original de `raw/`, y
   ejecuta la RPC transaccional `public.registrar_gasto` en Supabase.
7. La RPC es idempotente por `(chat_id, message_id)` y por `message_id`.

## Variables de entorno

`python/config/settings.py` es el único cargador de configuración. En local lee
`.env` si `python-dotenv` está instalado; en Lambda usa las variables del
entorno.

| Variable | Uso |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token del bot; el código lo expone como `TELEGRAM_TOKEN` |
| `TELEGRAM_API_URL` | `https://api.telegram.org` |
| `GROQ_API_KEY` | Clave de Groq |
| `GROQ_API_URL` | Endpoint de chat completions de Groq |
| `BUCKET_NAME` | Bucket de ingestion |
| `SUPABASE_URL` | URL del proyecto Supabase |
| `SUPABASE_PUBLISHABLE_KEY` | Clave publicable; no la usa el store |
| `SUPABASE_SECRET_KEY` | Clave secreta usada por el store |
| `SUPABASE_JWKS_URL` | URL de JWKS; no la usa el store |
| `DB_*`, `USER_NAME` | Legado de RDS; el store nuevo no los usa |

`SUPABASE_SECRET_KEY` es sensible. No debe quedar en el repositorio, en logs ni
en capturas. El código también acepta el nombre legacy
`SUPABASE_SERVICE_ROLE_KEY`.

Cada Lambda debe definir solo las variables que usa:

- ingestion: `BUCKET_NAME`
- processor: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_API_URL`, `GROQ_API_KEY`,
  `GROQ_API_URL`
- store: `SUPABASE_URL`, `SUPABASE_SECRET_KEY`

## Ejecución local

No hay un entrypoint local para el pipeline completo. Para validar imports y
sintaxis:

```powershell
$env:PYTHONPATH = (Resolve-Path python).Path
venv\Scripts\python.exe -m compileall -q python expense-store-lambda expense-procces-lambda
```

`boto3` lo provee el runtime de Lambda y no está en el entorno local. No hay
tests, linter ni typechecker configurados.

## Empaquetado y despliegue

La capa se construye en `build/layer`:

```text
build/layer/
└── python/            # copia de python/ + dependencias de requirements-layer.txt
```

El ZIP de la capa debe contener `python/` en la raíz. Los ZIP de las funciones
contienen:

- `expense-ingestion-lambda`: `lambda_function.py`
- `expense-procces-lambda`: `lambda_function.py` y `core/`
- `expense-store-lambda`: `lambda_function.py` y `core/`

`boto3` no se empaqueta. Las tres funciones usan la capa compartida y se
despliegan manualmente. El store no necesita VPC ni conexión directa a
Postgres.

## Webhook de Telegram

El webhook se registra una vez por bot:

```text
https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<API_ID>.execute-api.<REGION>.amazonaws.com/default/webhook-telegram-bot
```

Si el stage de API Gateway es `default`, la URL debe incluir `/default`. Se
recomienda `allowed_updates=["message"]` para que ingestion reciba únicamente
mensajes. Después de cambiar de bot o de token, verifica con `getWebhookInfo`
que `url` sea la correcta, `pending_update_count` sea 0 y
`last_error_message` esté vacío.

## Contrato del LLM

`expense-processor` guarda la respuesta cruda de Groq y `expense-store` parsea:

```text
response["choices"][0]["message"]["content"]
```

Claves esperadas: `ChatId`, `MessageId`, `Fecha`, `Categoria`, `Subcategoria`,
`Producto`, `Cantidad`, `Unidad`, `Lugar`, `MetodoPago`, `Valor`, `Moneda`,
`Estado`.

`Cantidad` y `Valor` son numéricos; `Unidad` va separada. El modelo configurado
es `openai/gpt-oss-120b` (`python/llm/models.py`).

## Persistencia objetivo (Supabase)

La migración del store usa REST + RPC, no una conexión Postgres directa:

- `public.registrar_gasto(...)` inserta o actualiza cliente, mensaje y gasto en
  una sola transacción.
- Las tablas `clientes`, `mensajes` y `gastos` tienen RLS activo y sin policies
  para escritura pública.
- La RPC es `security definer`; solo `service_role` debe ejecutarla.
- `supabase/schema.sql` queda como DDL de referencia de la migración.

La tabla `mensajes` conserva la columna histórica `s3_key_proccessed` con esa
grafía.

## Seguridad

- Los tokens y claves viven en variables de entorno o `.env`; nunca en Git.
- `.env` está ignorado.
- El cliente de Telegram convierte los errores de `requests` en
  `TelegramAPIError` sin incluir la URL ni el token, para no filtrarlos a
  CloudWatch.
- `SUPABASE_SECRET_KEY` solo se usa en el store y no se registra en logs.
- El bucket S3 y las bases de datos deben restringirse a las funciones que los
  usan.

## Limitaciones actuales

- Despliegue manual; no hay infraestructura como código.
- Sin tests automatizados, CI, linter ni typechecker.
- El código del store y `supabase/schema.sql` se incorporan en el commit de
  migración a Supabase.
- La documentación local del agente (`AGENTS.md`, `especificaciones.md`,
  `memory.md`, `plan-desarrollo.md`) está ignorada por Git.
