from functools import lru_cache
from typing import Union
import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException

from api import config

# LRU Cache para la función de obtener UF
@lru_cache(config.cache_init.max_cache_size)
def get_uf(url: str, day: int, month: int) -> Union[str, None]:
    
    custom_header: dict[str, str] = {'user-Agent': config.header_http_init.user_agent}
    with httpx.Client() as client:
        # Agregar un tiempo de espera en segundos
        try:
            res = client.get(url, headers=custom_header, timeout=config.timeout_init.get_uf_timeout)
            res.raise_for_status()  # Lanza un error si la solicitud falla
        except httpx.HTTPStatusError as e:
            # Manejo específico del error 404
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="No se encontró la página o los datos solicitados.") from e
            raise HTTPException(status_code=500, detail="Error al obtener los datos.") from e
        except httpx.TimeoutException as e:
            raise HTTPException(status_code=504, detail="La solicitud ha superado el tiempo de espera.") from e
        except HTTPException as e:
            raise HTTPException(status_code=500, detail="Error en la solicitud.") from e

        try:
            soup = BeautifulSoup(res.text, 'html.parser')
            table = soup.find('table', id=config.scraping_init.table_id)
            if table is None:
                raise ValueError(f"No se encontró la tabla con el id {config.scraping_init.table_id}.")
            table_body = table.find(config.scraping_init.table_body_label)
            if table_body is None:
                raise ValueError(f"No se encontró el cuerpo de la tabla con la etiqueta {config.scraping_init.table_body_label}.")
            rows = table_body.find_all(config.scraping_init.rows_label)
            if not rows:
                raise ValueError(f"No se encontraron filas con la etiqueta {config.scraping_init.rows_label}.")
            current_row = rows[day - 1]
            months = current_row.find_all(config.scraping_init.row_elements_label)
            if not months:
                raise ValueError(f"No se encontraron elementos con la etiqueta {config.scraping_init.row_elements_label}.")
            current_month = months[month - 1]
            value = current_month.text.strip()
            if value:
                return value
            return ''
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
