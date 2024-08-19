from typing import Union, Dict
from pydantic import BaseModel

class UFResponse(BaseModel):
    """
    Modelo de respuesta para los valores de UF.
    
    - **uf_value**: Valor de la UF en formato cadena o flotante.
    - **date**: Fecha en formato `dd/mm/yyyy`.
    """
    uf_value: Union[str, float]
    date: str

class UFDictResponse(BaseModel):
    """
    Modelo de respuesta para los valores de UF.
    
    - **uf_values**: Diccionario con los valores de UF para cada día del mes.
    """
    uf_values: Dict[str, Union[str, float]]