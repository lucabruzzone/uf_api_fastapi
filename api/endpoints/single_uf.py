from datetime import datetime
from typing import Union
from fastapi import APIRouter, HTTPException, Query
from api.schemas.response import UFResponse

from api.utils.constants import MINIMUM_DATE
from api.utils.get_uf import get_uf

router = APIRouter()

@router.get("/get_single_uf", response_model=UFResponse)
def get_single_uf(
    day: int = Query(..., ge=1, le=31),
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., gt=2012)  # Mayor o igual a 2013
) -> UFResponse:
    """
    Obtiene el valor de UF para un día, mes y año específicos.

    - **day**: Día del mes (1-31).
    - **month**: Mes del año (1-12).
    - **year**: Año (mayor a 2012).

    Retorna un objeto `UFResponse` que contiene el valor de UF y la fecha para el día especificado.

    - Si la fecha solicitada es anterior al 1 de enero de 2013, se devuelve un error 400.
    - Si ocurre un error al obtener el valor de UF, se devuelve un error 500.
    - Si los parámetros de fecha son inválidos, se devuelve un error 400.
    """
    try:
        selected_date = datetime(year, month, day)

        if selected_date >= MINIMUM_DATE:
            url: str = f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm'
            try:
                uf_value: Union[str, float] = get_uf(url, day, month)
                return UFResponse(uf_value=uf_value, date=selected_date.strftime('%d/%m/%Y'))
            except RuntimeError as e:
                raise HTTPException(status_code=500, detail=str(e)) from e
        else:
            raise HTTPException(status_code=400, detail='La fecha debe ser posterior al 1 de enero de 2013.')

    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail='Los parámetros de fecha no son válidos.') from e
