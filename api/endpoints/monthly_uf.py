from datetime import datetime
from typing import Union
from fastapi import APIRouter, HTTPException, Query

from api.models.response import UFDictResponse
from api.utils.constants import MINIMUM_DATE
from api.utils.get_uf import get_uf

router = APIRouter()

@router.get("/get_monthly_uf", response_model=UFDictResponse)
def get_monthly_uf(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2013)  # Mayor o igual a 2013
) -> UFDictResponse:
    """
    Obtiene los valores de UF para un mes y año específicos.

    - **month**: Mes del año (1-12).
    - **year**: Año (mayor o igual a 2013).

    Retorna una lista de objetos `UFResponse` que contienen el valor de UF y la fecha para cada día del mes especificado.

    - Si la fecha solicitada es anterior al 1 de enero de 2013 o si los parámetros son inválidos, se devuelve un error 422.
    - Si ocurre un error al obtener los valores de UF, se devuelve un error 500.
    - Si el día no es válido para el mes (por ejemplo, 30 de febrero), se omite y se detiene el proceso para ese mes.
    """
    try:
        selected_date = datetime(year, month, 1)

        if selected_date < MINIMUM_DATE:
            raise HTTPException(status_code=422, detail='La fecha debe ser posterior al 1 de enero de 2013.')

        url: str = f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm'

        try:
            uf_values: UFDictResponse = {}
            for day in range(1, 32):
                try:
                    datetime(year, month, day)
                    uf_value: Union[str, float] = get_uf(url, day, month)
                    if not uf_value:
                        break
                    uf_values[f'{day:02d}/{month:02d}/{year}'] = uf_value
                except ValueError:
                    # Día no válido para el mes
                    break
            if not uf_values:
                raise HTTPException(status_code=404, detail='no se encontraron valores de UF para el mes y año especificados.')
            return UFDictResponse(uf_values=uf_values) # Devolvemos una instancia del modelo UFDictResponse como respuesta
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail='Los parámetros de fecha no son válidos.') from e
