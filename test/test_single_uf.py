"""
Pruebas para la ruta `/get_single_uf` de la API.

1. **test_success**: Verifica que la ruta `/get_single_uf` devuelve una respuesta exitosa (código de estado 200) cuando se proporciona una fecha válida. 
2. **test_invalid_day**: Verifica que la ruta `/get_single_uf` devuelve un error 422 cuando se proporciona un día inválido (fuera del rango 1-31).
3. **test_invalid_month**: Verifica que la ruta `/get_single_uf` devuelve un error 422 cuando se proporciona un mes inválido (fuera del rango 1-12).
4. **test_invalid_year**: Verifica que la ruta `/get_single_uf` devuelve un error 422 cuando se proporciona un año anterior a 2013.
5. **test_invalid_datetime**: Verifica que la ruta `/get_single_uf` devuelve un error 400 cuando ocurre un error al intentar crear un datetime inválido.
6. **test_not_found**: Verifica que la ruta `/get_single_uf` devuelve un error 404 cuando no se encuentran los valores de UF para la fecha especificada.
7. **test_server_error**: Verifica que la ruta `/get_single_uf` devuelve un error 500 cuando ocurre un error inesperado al obtener los valores de UF.
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.models.response import UFResponse

client = TestClient(app)

# @pytest.mark.skip
@pytest.mark.parametrize("day, month, year", [
    (1, 1, 2013), (15, 3, 2014), (28, 9, 2015), (5, 6, 2016),
    (15, 2, 2017), (10, 4, 2018), (25, 7, 2019), (8, 8, 2020),
    (12, 1, 2021), (23, 9, 2022), (7, 3, 2023), (19, 5, 2024),
    (4, 2, 2014), (16, 8, 2015), (1, 1, 2016), (10, 9, 2017),
    (15, 4, 2018), (22, 7, 2019), (5, 6, 2020), (20, 8, 2021),
    (3, 5, 2022), (28, 9, 2023), (12, 7, 2024), (14, 1, 2013)
])
def test_success(day, month, year):
    """
    Prueba que la ruta `/get_single_uf` devuelve una respuesta exitosa 
    (código de estado 200) cuando se proporciona una fecha válida.
    
    Verifica que la respuesta contenga los campos `uf_value` y `date`.
    """
    response = client.get("/get_single_uf", params={"day": day, "month": month, "year": year})
    assert response.status_code == 200
    response_json = response.json()

    # Verifica que la respuesta contenga los campos esperados
    assert "uf_value" in response.json()
    assert "date" in response.json()

    # Verifica que la respuesta cumpla con el esquema del modelo UFResponse
    try:
        UFResponse(**response_json)
    except ValueError as e:
        pytest.fail(f"La respuesta no cumple con el modelo UFResponse: {e}")

# @pytest.mark.skip
def test_invalid_day():
    """
    Prueba que la ruta `/get_single_uf` devuelve un error 422
    cuando se proporciona un día inválido (fuera del rango 1-31).
    
    Verifica que el mensaje de error sea adecuado para parámetros de fecha no válidos.
    """
    response_1 = client.get("/get_single_uf", params={"day": 32, "month": 8, "year": 2023})
    response_2 = client.get("/get_single_uf", params={"day": 0, "month": 8, "year": 2023})
    assert response_1.status_code == 422
    assert response_2.status_code == 422

    # Verificar el contenido exacto de la respuesta de error
    error_details_1 = response_1.json()
    error_details_2 = response_2.json()
    
    expected_error_1 = [
        {
            "type": "less_than_equal",
            "loc": ["query", "day"],
            "msg": "Input should be less than or equal to 31",
            "input": "32",
            "ctx": {"le": 31}
        }
    ]
    
    expected_error_2 = [
        {
            "type": "greater_than_equal",
            "loc": ["query", "day"],
            "msg": "Input should be greater than or equal to 1",
            "input": "0",
            "ctx": {"ge": 1}
        }
    ]
    
    assert error_details_1 == {"detail": expected_error_1}
    assert error_details_2 == {"detail": expected_error_2}

# @pytest.mark.skip
def test_invalid_month():
    """
    Prueba que la ruta `/get_single_uf` devuelve un error 422 
    cuando se proporciona un mes inválido (fuera del rango 1-12).
    
    Verifica que el mensaje de error sea adecuado para parámetros de fecha no válidos.
    """
    response_1 = client.get("/get_single_uf", params={"day": 15, "month": 13, "year": 2023})
    response_2 = client.get("/get_single_uf", params={"day": 15, "month": 0, "year": 2023})
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
    Prueba que la ruta `/get_single_uf` devuelve un error 400 
    cuando se proporciona un año anterior a 2013.
    
    Verifica que el mensaje de error indique que la fecha debe ser posterior al 1 de enero de 2013.
    """
    response = client.get("/get_single_uf", params={"day": 15, "month": 8, "year": 2012})
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
    Prueba que la ruta `/get_single_uf` devuelve un error 400 
#     cuando ocurre un error al intentar crear un datetime inválido.
    """
    response = client.get("/get_single_uf", params={"day": 15, "month": 8, "year": 30000})
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
    Prueba que la ruta `/get_single_uf` devuelve un error 404 
#     cuando no se encuentran los valores de UF para la fecha especificada.
    """
    response = client.get("/get_single_uf", params={"day": 15, "month": 10, "year": 2024})
    assert response.status_code == 404

    # Verificar el contenido exacto de la respuesta de error
    error_details = response.json()
    
    expected_error = "No se encontró un valor UF para la fecha especificada."
    
    assert error_details == {"detail": expected_error}
