from datetime import datetime
from typing import Union
from fastapi import APIRouter, HTTPException, Query

from api.models.response import UFDictResponse
from api import config
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

    Retorna un diccionario `UFDictResponse` que contiene los valores de UF con su fecha respectiva.

    - Si la fecha solicitada es anterior al 1 de enero de 2013 o si los parámetros son inválidos, se devuelve un error 422.
    - Si ocurre un error al obtener los valores de UF, se devuelve un error 500.
    - Si el día no es válido para el mes (por ejemplo, 30 de febrero), se omite y se detiene el proceso para ese mes.
    """
    try:
        selected_date = datetime(year, month, 1)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f'Los parámetros de fecha no son válidos. {e}') from e
    
    try:
        if selected_date >= config.date_init.min_date:
            url: str = f'https://www.sii.cl/valores_y_fechas/uf/uf{year}.htm'
            uf_values: UFDictResponse = {}
            total_sum = 0.0
            count = 0

            for day in range(1, 32):
                # Verificamos si el día es válido para el mes
                try:
                    datetime(year, month, day)
                    uf_value: Union[str, float] = get_uf(url, day, month) # Obtenemos el valor de UF para el día y mes
                    if not uf_value:
                        break
                    uf_float_value = float(uf_value.replace('.', '').replace(',', '.')) # Convertimos el valor de UF a float para conseguir un formato numérico más universal
                    uf_float_str = f"{uf_float_value:.2f}" # Convertimos el valor de UF a string con 2 decimales para mantener el tipo de dato original
                    uf_values[f'{day:02d}/{month:02d}/{year}'] = uf_float_str
                    total_sum += uf_float_value
                    count += 1
                except ValueError:
                    # Día no válido para el mes
                    break

            if uf_values:
                if count > 0:
                    uf_average = round(total_sum / count, 2) # Redondeamos el promedio a 2 decimales
                    uf_average_str = f"{uf_average:.2f}"
                    return UFDictResponse(uf_values=uf_values, uf_average=uf_average_str)
                return UFDictResponse(uf_values=uf_values) # Devolvemos una instancia del modelo UFDictResponse como respuesta
            raise HTTPException(status_code=404, detail='no se encontraron valores de UF para el mes y año especificados.')
        
        raise HTTPException(status_code=400, detail='La fecha debe ser posterior al 1 de enero de 2013.')
    
    except Exception as e:
        raise e
