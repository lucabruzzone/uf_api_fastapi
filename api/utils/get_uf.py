from functools import lru_cache
from typing import Union
import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException

from api.utils import constants

# LRU Cache para la función de obtener UF
@lru_cache(constants.MAX_CACHE_SIZE)
def get_uf(url: str, day: int, month: int) -> Union[str, None]:
    
    custom_header: dict[str, str] = {'user-Agent': constants.USER_AGENT}
    with httpx.Client() as client:
        # Agregar un tiempo de espera constants.GET_UF_TIMEOUT en segundos
        try:
            res = client.get(url, headers=custom_header, timeout=constants.GET_UF_TIMEOUT)
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
            table = soup.find('table', id=constants.TABLE_ID)
            if table is None:
                raise ValueError(f"No se encontró la tabla con el id {constants.TABLE_ID}.")
            table_body = table.find(constants.TABLE_BODY_LABEL)
            if table_body is None:
                raise ValueError(f"No se encontró el cuerpo de la tabla con la etiqueta {constants.TABLE_BODY_LABEL}.")
            rows = table_body.find_all(constants.ROWS_LABEL)
            if not rows:
                raise ValueError(f"No se encontraron filas con la etiqueta {constants.ROWS_LABEL}.")
            current_row = rows[day - 1]
            months = current_row.find_all(constants.ROW_ELEMENTS_LABEL)
            if not months:
                raise ValueError(f"No se encontraron elementos con la etiqueta {constants.ROW_ELEMENTS_LABEL}.")
            current_month = months[month - 1]
            value = current_month.text.strip()
            if value:
                return value
            return ''
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
