from datetime import datetime
from typing import List, Union
from fastapi import APIRouter, HTTPException, Query
from api.schemas.response import UFResponse

from api.utils.constants import MINIMUM_DATE
from api.utils.get_uf import get_uf

router = APIRouter()

@router.get("/get_monthly_uf", response_model=List[UFResponse])
def get_monthly_uf(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2013)  # Mayor o igual a 2013
) -> List[UFResponse]:
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
            uf_values: List[UFResponse] = []
            for day in range(1, 32):
                try:
                    datetime(year, month, day)
                    uf_value: Union[str, float] = get_uf(url, day, month)
                    uf_values.append(UFResponse(date=f'{day:02d}/{month:02d}/{year}', uf_value=uf_value))
                except ValueError:
                    # Día no válido para el mes
                    break
            return uf_values
        except RuntimeError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    except (ValueError, TypeError) as e:
        raise HTTPException(status_code=422, detail='Los parámetros de fecha no son válidos.') from e
