import requests

from config.settings import SUPABASE_SECRET_KEY, SUPABASE_URL


class SupabaseClient:
    """
    Cliente REST para persistir gastos en Supabase.

    La Lambda no abre una conexión Postgres directa. Llama a la función RPC
    `public.registrar_gasto`, que inserta o actualiza cliente, mensaje y gasto
    dentro de una sola transacción en Postgres.
    """

    def __init__(self):
        """
        Inicializa la configuración del cliente REST.
        """

        # URL base del proyecto Supabase, sin la barra final.
        self.base_url = (SUPABASE_URL or "").rstrip("/")

        # Clave secreta (`SUPABASE_SECRET_KEY` o la legacy
        # `SUPABASE_SERVICE_ROLE_KEY`). Nunca se registra en logs.
        self.api_key = SUPABASE_SECRET_KEY

        # Cabeceras requeridas por PostgREST y Supabase.
        self.headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    def registrar_gasto(self, payload: dict) -> dict:
        """
        Ejecuta la función RPC que guarda un gasto completo.

        Args:
            payload: Parámetros de la función `registrar_gasto`.

        Returns:
            Diccionario con los identificadores generados o actualizados.
        """

        # Validar la configuración antes de hacer la petición HTTP.
        if not self.base_url or not self.api_key:
            raise RuntimeError(
                "Faltan SUPABASE_URL o SUPABASE_SECRET_KEY "
                "(o SUPABASE_SERVICE_ROLE_KEY) en el entorno."
            )

        # Endpoint RPC expuesto por PostgREST.
        url = f"{self.base_url}/rest/v1/rpc/registrar_gasto"

        # Ejecutar la transacción del lado de Postgres.
        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=30
        )

        # Incluir el detalle de Postgres en el error para diagnosticar.
        if response.status_code >= 400:
            raise RuntimeError(
                "Supabase RPC registrar_gasto falló "
                f"({response.status_code}): {response.text}"
            )

        # Devolver el JSON generado por la función.
        return response.json()
