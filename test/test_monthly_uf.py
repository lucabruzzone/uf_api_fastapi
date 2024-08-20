"""
Pruebas para la ruta `/get_monthly_uf` de la API.

1. **test_success**: Verifica que la ruta responda correctamente con un mes y año válidos.
2. **test_invalid_month**: Verifica que la ruta devuelva un error 422 si el mes es inválido (fuera del rango 1-12).
3. **test_invalid_year**: Verifica que la ruta devuelva un error 422 si el año es inválido (anterior a 2013).
4. **test_invalid_datetime**: Verifica que la ruta devuelva un error 400 si el año es anterior al mínimo permitido (1 de enero de 2013).
5. **test_not_found**: Verifica que la ruta devuelva un error 404 si no se encuentran valores UF para el mes y año especificados.
6. **test_server_error**: Verifica que la ruta devuelva un error 500 si ocurre algún error inesperado al obtener los valores de UF del mes especificado.

Para ejecutar las pruebas, asegúrate de tener `pytest` instalado y ejecuta el comando `pytest` en el directorio del proyecto.

Se utiliza `TestClient` de FastAPI para realizar solicitudes a la API y verificar las respuestas.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# @pytest.mark.skip
def test_success():
    """
    Verifica que la ruta `/get_monthly_uf` responda con éxito para un mes y año válidos.

    - **Entrada**: mes=8, año=2024
    - **Salida esperada**: Estado HTTP 200 y un diccionario con valores de UF válidos.
    """
    response = client.get("/get_monthly_uf", params={"month": 8, "year": 2023})
    assert response.status_code == 200
    data = response.json().get('uf_values')
    assert isinstance(data, dict)
    assert all(isinstance(k, str) and isinstance(v, (str, float)) for k, v in data.items())

# @pytest.mark.skip
def test_invalid_month():
    """
    Verifica que la ruta `/get_monthly_uf` devuelve un error 422 si el mes es inválido.

    - **Entrada_1**: mes=13, año=2024
    - **Entrada_2**: mes=0, año=2024
    - **Salida esperada**: Estado HTTP 422 (Unprocessable Entity).
    """
    response_1 = client.get("/get_monthly_uf", params={"month": 13, "year": 2024})
    response_2 = client.get("/get_monthly_uf", params={"month": 0, "year": 2024})
    assert response_1.status_code == 422
    assert response_2.status_code == 422

    # Verificar el contenido exacto de la respuesta de error
    error_details_1 = response_1.json()
    error_details_2 = response_2.json()
    
    expected_error_1 = [
        {
            "type": "less_than_equal",
            "loc": [
                "query",
                "month"
            ],
            "msg": "Input should be less than or equal to 12",
            "input": "13",
            "ctx": {
                "le": 12
            }
        }
    ]
    
    expected_error_2 = [
        {
            "type": "greater_than_equal",
            "loc": [
                "query",
                "month"
            ],
            "msg": "Input should be greater than or equal to 1",
            "input": "0",
            "ctx": {
                "ge": 1
            }
        }
    ]
    
    assert error_details_1 == {"detail": expected_error_1}
    assert error_details_2 == {"detail": expected_error_2}

# @pytest.mark.skip
def test_invalid_year():
    """
    Verifica que la ruta `/get_monthly_uf` devuelve un error 422 si la fecha es anterior al 1 de enero de 2013.

    - **Entrada**: mes=9, año=2012
    - **Salida esperada**: Estado HTTP 422 (Unprocessable Entity).
    """
    response = client.get("/get_monthly_uf", params={"month": 9, "year": 2012})
    assert response.status_code == 422

    # Verificar el contenido exacto de la respuesta de error
    error_details = response.json()
    
    expected_error = [
        {
            "type": "greater_than_equal",
            "loc": [
                "query",
                "year"
            ],
            "msg": "Input should be greater than or equal to 2013",
            "input": "2012",
            "ctx": {
                "ge": 2013
            }
        }
    ]
    
    assert error_details == {"detail": expected_error}

# @pytest.mark.skip
def test_invalid_datetime():
    """
    Prueba que la ruta `/get_monthly_uf` devuelve un error 400 
#     cuando ocurre un error al intentar crear un datetime inválido.
    """
    response = client.get("/get_monthly_uf", params={"month": 8, "year": 30000})
    assert response.status_code == 400

    # Verificar el contenido exacto de la respuesta de error
    error_details = response.json()
    
    expected_error = "Los parámetros de fecha no son válidos."
    
    # Comprobar si `expected_error` está contenido en `detail`
    expected_error = "Los parámetros de fecha no son válidos."
    assert expected_error in error_details["detail"]

# @pytest.mark.skip
def test_not_found():
    """
    Prueba que la ruta `/get_monthly_uf` devuelve un error 404 
#     cuando no se encuentran los valores de UF para el mes especificado.
    """
    response = client.get("/get_monthly_uf", params={"month": 10, "year": 2024})
    assert response.status_code == 404

    # Verificar el contenido exacto de la respuesta de error
    error_details = response.json()
    
    expected_error = "no se encontraron valores de UF para el mes y año especificados."
    
    assert error_details == {"detail": expected_error}

# @pytest.mark.skip
def test_not_found_2():
    """
    Prueba que la ruta `/get_monthly_uf` devuelve un error 404 
#     cuando no se encuentra la página o los datos.
    """
    response = client.get("/get_monthly_uf", params={"month": 8, "year": 2027})
    assert response.status_code == 404

