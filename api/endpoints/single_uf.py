from datetime import datetime
from typing import Union
from fastapi import APIRouter, HTTPException, Query

from api.models.response import UFResponse
from api import config
from api.utils.get_uf import get_uf

router = APIRouter()

@router.get("/get_single_uf", response_model=UFResponse)
def get_single_uf(
    day: int = Query(..., ge=1, le=31),
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2013)  # Mayor o igual a 2013
) -> UFResponse:
    """
    Obtiene el valor de UF para un día, mes y año específicos.

    - **day**: Día del mes (1-31).
    - **month**: Mes del año (1-12).
    - **year**: Año (mayor a 2012).

    Retorna un objeto `UFResponse` que contiene el valor de UF y la fecha para el día especificado.
    """
    try:
        selected_date = datetime(year, month, day)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f'Los parámetros de fecha no son válidos. {e}') from e
    
    try:
        if selected_date >= config.date_init.min_date:
            url: str = f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm'
            uf_value: Union[str, float] = get_uf(url, day, month)
            if uf_value:
                uf_float_value = float(uf_value.replace('.', '').replace(',', '.')) # Convertimos el valor de UF a float para conseguir un formato numérico más universal
                uf_float_str = f"{uf_float_value:.2f}" # Convertimos el valor de UF a string con 2 decimales para mantener el tipo de dato original
                return UFResponse(uf_value=uf_float_str, date=selected_date.strftime('%d/%m/%Y'))
            raise HTTPException(status_code=404, detail="No se encontró un valor UF para la fecha especificada.")
        raise HTTPException(status_code=400, detail='La fecha debe ser posterior al 1 de enero de 2013.')
    
    except Exception as e:
        raise e
