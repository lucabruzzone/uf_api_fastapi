"""
Este módulo define las constantes utilizadas en la aplicación.
"""

from datetime import datetime

# Tiempo de espera para la conexión y lectura de solicitudes
GET_UF_TIMEOUT: float = 15.0
GET_UF_CONNECT_TIMEOUT: float = 5.0
GET_UF_READ_TIMEOUT: float = 10.0

# Tamaño máximo para el caché
MAX_CACHE_SIZE: int = 100

# Rango de años y meses válidos
MIN_YEAR: int = 2013
MIN_MONTH: int = 1
MAX_MONTH: int = 12
MIN_DAY: int = 1
MAX_DAY: int = 31

# Fechas mínimas
MIN_DATE = datetime(2013, 1, 1)

# Etiquetas HTML
TABLE_ID = 'table_export'
TABLE_BODY_LABEL = 'tbody'
ROWS_LABEL = 'tr'
ROW_ELEMENTS_LABEL = 'td'

# Agente de usuario para solicitudes HTTP
USER_AGENT: dict[str, str] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
