"""
Este módulo contiene pruebas para verificar el comportamiento de la api 
cuando los elementos html de la web a la cual se le está haciendo scraping
no se encuentran disponibles.
"""

import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.config import scraping_init

client = TestClient(app)

# @pytest.mark.skip
def test_atributes_not_found():
    """
    Verificar que la ruta `/get_single_uf` devuelve un error 404 si no se encuentran los items del scraping.
    """

    scraping_updates = {
        "table_id": 'dnsjakndaks',
        "table_body_label": 'tbodydsad',
        "rows_label": 'trdsad',
        "row_elements_label": 'tddsads'
    }

    for key, value in scraping_updates.items():
        # Actualizar la configuración de scraping
        scraping_init.update(**{key: value})

        # Realizar la solicitud y verificar el error 404
        response = client.get("/get_single_uf", params={"day": 3, "month": 8, "year": 2023})
        assert response.status_code == 404
        scraping_init.reset() # Resetear la configuración de scraping


# PRUEBAS ESPECÍFICAS POR CADA ATRIBUTO DEL SCRAPING:

def test_table_id_not_found():
    """
    Verificar que la ruta `/get_single_uf` devuelve un error 404 si no se encuentra el `table_id`.
    """

    scraping_init.update(**{"table_id": 'dnsjakndaks'})

    # Realizar la solicitud y verificar el error 404
    response = client.get("/get_single_uf", params={"day": 3, "month": 8, "year": 2023})
    assert response.status_code == 404
    scraping_init.reset() # Resetear la configuración de scraping

def test_table_body_label_not_found():
    """
    Verificar que la ruta `/get_single_uf` devuelve un error 404 si no se encuentra el `table_body_label`.
    """

    scraping_init.update(**{"table_body_label": 'dnsjakndaks'})

    # Realizar la solicitud y verificar el error 404
    response = client.get("/get_single_uf", params={"day": 3, "month": 8, "year": 2023})
    assert response.status_code == 404
    scraping_init.reset() # Resetear la configuración de scraping

def test_rows_label_not_found():
    """
    Verificar que la ruta `/get_single_uf` devuelve un error 404 si no se encuentra el `rows_label`.
    """

    scraping_init.update(**{"rows_label": 'dnsjakndaks'})

    # Realizar la solicitud y verificar el error 404
    response = client.get("/get_single_uf", params={"day": 3, "month": 8, "year": 2023})
    assert response.status_code == 404
    scraping_init.reset() # Resetear la configuración de scraping

def test_row_elements_label_not_found():
    """
    Verificar que la ruta `/get_single_uf` devuelve un error 404 si no se encuentra el `row_elements_label`.
    """

    scraping_init.update(**{"row_elements_label": 'dnsjakndaks'})

    # Realizar la solicitud y verificar el error 404
    response = client.get("/get_single_uf", params={"day": 3, "month": 8, "year": 2023})
    assert response.status_code == 404
    scraping_init.reset() # Resetear la configuración de scraping

