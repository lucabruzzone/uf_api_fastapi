"""
Este módulo define las configuraciones para diferentes aspectos de la aplicación, 
proporcionando una estructura base para manejar y actualizar las propiedades de configuración.

Las configuraciones están divididas en clases específicas para organizar diferentes tipos de parámetros:
- `ScrapingConfig`: Configuración relacionada con los elementos de scraping en HTML.
- `TimeoutConfig`: Configuración para los tiempos de espera en las solicitudes.
- `CacheConfig`: Configuración para el tamaño máximo del caché.
- `DateConfig`: Configuración para los rangos y fechas mínimas.
- `HeaderHTTPConfig`: Configuración para el header de solicitudes HTTP.

Cada clase hereda de `BaseConfig`, que proporciona métodos comunes para mostrar y actualizar las propiedades.

PARA ACTUALIZAR LAS PROPIEDADES DE FORMA PERMANENTE, PUEDES IR AL ARCHIVO `/UTILS/CONSTANTS.PY` Y MODIFICAR LOS VALORES DIRECTAMENTE.
"""
from datetime import datetime

from .utils import constants

class BaseConfig:
    """Clase base para configurar métodos comunes."""

    def display(self) -> str:
        """Método para mostrar todas las propiedades de una instancia."""
        properties = []
        for attribute, value in self.__dict__.items():
            properties.append(f"{attribute}: {value}")
        return ", ".join(properties)

    def update(self, **kwargs):
        """Método para actualizar las propiedades de una instancia."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    def reset(self):
        """Método para resetear los atributos a sus valores por defecto."""
        default_instance = self.__class__()  # Crear una nueva instancia con valores por defecto
        for attribute, value in default_instance.__dict__.items():
            setattr(self, attribute, value)

class Scraping(BaseConfig):
    """Configuración relacionada con los items a los cuales se les hará scraping."""

    def __init__(
            self,
            table_id: str = constants.TABLE_ID,
            table_body_label: str = constants.TABLE_BODY_LABEL,
            rows_label: str = constants.ROWS_LABEL,
            row_elements_label: str = constants.ROW_ELEMENTS_LABEL
            ):
        self.table_id = table_id
        self.table_body_label = table_body_label
        self.rows_label = rows_label
        self.row_elements_label = row_elements_label

class Timeout(BaseConfig):
    """Configuración relacionada con los tiempos de espera de conexión y lectura."""

    def __init__(
            self,
            get_uf_timeout: float = constants.GET_UF_TIMEOUT,
            get_uf_connect_timeout: float = constants.GET_UF_CONNECT_TIMEOUT,
            get_uf_read_timeout: float = constants.GET_UF_READ_TIMEOUT
            ):
        self.get_uf_timeout = get_uf_timeout
        self.get_uf_connect_timeout = get_uf_connect_timeout
        self.get_uf_read_timeout = get_uf_read_timeout

class Cache(BaseConfig):
    """Configuración relacionada con el tamaño máximo del caché."""

    def __init__(
            self,
            max_cache_size: int = constants.MAX_CACHE_SIZE):
        self.max_cache_size = max_cache_size

class Date(BaseConfig):
    """Configuración relacionada con las fechas mínimas y límites."""

    def __init__(
            self,
            min_year: int = constants.MIN_YEAR,
            min_month: int = constants.MIN_MONTH,
            max_month: int = constants.MAX_MONTH,
            min_day: int = constants.MIN_DAY,
            max_day: int = constants.MAX_DAY,
            min_date: datetime = constants.MIN_DATE
            ):
        self.min_year = min_year
        self.min_month = min_month
        self.max_month = max_month
        self.min_day = min_day
        self.max_day = max_day
        self.min_date = min_date

class HeaderHTTP(BaseConfig):
    """Configuración relacionada con el header de solicitudes HTTP."""

    def __init__(
            self,
            user_agent: str = constants.USER_AGENT
            ):
        self.user_agent = user_agent

# Instancias por defecto
scraping_init = Scraping()
timeout_init = Timeout()
cache_init = Cache()
date_init = Date()
header_http_init = HeaderHTTP()
