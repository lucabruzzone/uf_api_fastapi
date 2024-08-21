# API de Valores UF

Esta API proporciona información sobre el valor de la Unidad de Fomento (UF) en Chile. Permite consultar el valor de la UF para un día específico o para todos los días de un mes en particular.

## Implementación

### Dependencias

Asegúrate de tener las siguientes dependencias instaladas:

- `fastapi[standard]`
- `beautifulsoup4`
- `uvicorn`

### Instalación

Para instalar las dependencias necesarias, ejecuta:

```bash
pip install -r requirements.txt
```

### Estructura de carpetas

```text
.
├── api
│   ├── __init__.py
│   ├── main.py
│   ├── config.py               # Configuración global de la API
│   ├── endpoints
│   │   ├── __init__.py
│   │   ├── monthly_uf.py
│   │   └── single_uf.py
│   ├── models
│   │   ├── __init__.py
│   │   └── response.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── constants.py        # Define las constantes globales
│   │   └── get_uf.py           # Función que realiza el scraping
├── env
├── test
│   ├── __init__.py
│   ├── test_main.py           # Pruebas para main.py
│   ├── test_get_uf.py         # Pruebas para get_uf.py
│   ├── test_monthly_uf.py     # Pruebas para monthly_uf.py
│   └── test_single_uf.py      # Pruebas para single_uf.py
├── .gitignore
├── README.md
├── requirements.txt


```

### Ejecutar el Servidor

```bash
uvicorn api.main:app --reload
```

Sirviendo en: http://127.0.0.1:8000

Puedes probar la api desde la `documentación` interactiva: http://127.0.0.1:8000/docs

## Pruebas unitarias

### Pruebas unitarias

Este proyecto incluye un conjunto completo de pruebas unitarias para validar el funcionamiento de los endpoints de la API. Las pruebas están dentro de la carpeta `test`, donde encontrarás por separado las pruebas correspondientes a cada endpoint.

Estas pruebas utilizan `pytest` y `fastapi.testclient` para verificar distintos aspectos de la API.

### Ejecutar las pruebas

```bash
pytest
```

## Uso

### URL BASE

```bash
https://uf-api-fastapi.onrender.com
```

#### Respuesta

```json
{ "Hello": "Health check baby" }
```

### Endpoints Disponibles

- **Obtener el valor UF para un día específico**: Permite consultar el valor de la UF para una fecha específica (día, mes y año).
- **Obtener los valores UF para un mes específico**: Permite consultar los valores de la UF para todos los días de un mes y año específicos.

Para más detalles sobre cómo utilizar estos endpoints y los parámetros requeridos, por favor consulta la `documentación interactiva` en el siguient enlace: https://uf-api-fastapi.onrender.com/docs

### 1. Obtener el valor de la UF para una fecha específica

- **RUTA**: `/get_single_uf/`
- **Método**: `GET`
- **Descripción**: Obtiene el valor de la UF para una fecha específica.

#### Parámetros de Consulta

- `day` (int): Día del mes (1-31).
- `month` (int): Mes (1-12).
- `year` (int): Año (YYYY).

#### Ejemplo de Solicitud

```h
https://uf-api-fastapi.onrender.com/get_single_uf/?day=19&month=8&year=2024
```

#### Respuestas

- 200 OK:

```json
{
  "uf_value": "22.837,06",
  "date": "19/08/2024"
}
```

- 400 Bad Request:

```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["query", "month"],
      "msg": "Input should be greater than or equal to 1",
      "input": "0",
      "ctx": {
        "ge": 1
      }
    }
  ]
}
```

- 500 Internal Server Error:

```json
{
  "detail": "Error durante la solicitud a https://www.sii.cl/valores_y_fechas/uf/uf3000.htm: Client error '404 Not Found' for url 'https://www.sii.cl/valores_y_fechas/uf/uf3000.htm'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404"
}
```

### 2. Obtener todos los valores de la UF para un mes y año específicos

- **RUTA**: `/get_monthly_uf/`
- **Método**: `GET`
- **Descripción**: Obtiene todos los valores de la UF para un mes y año específicos.

#### Parámetros de Consulta

- `month` (int): Mes (1-12).
- `year` (int): Año (YYYY).

#### Ejemplo de Solicitud

```h
https://uf-api-fastapi.onrender.com/get_monthly_uf/?month=8&year=2024
```

#### Respuestas

- 200 OK:

```json
[
  {"date": "01/08/2024", "uf_value": "22.837,06"},
  {"date": "02/08/2024", "uf_value": "22.847,12"},
  ...
  {"date": "31/08/2024", "uf_value": "22.890,34"}
]

```

- 400 Bad Request:

```json
{
  "detail": [
    {
      "type": "greater_than_equal",
      "loc": ["query", "month"],
      "msg": "Input should be greater than or equal to 1",
      "input": "0",
      "ctx": {
        "ge": 1
      }
    }
  ]
}
```

- 500 Internal Server Error:

```json
{
  "detail": "Error durante la solicitud a https://www.sii.cl/valores_y_fechas/uf/uf3000.htm: Client error '404 Not Found' for url 'https://www.sii.cl/valores_y_fechas/uf/uf3000.htm'\nFor more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404"
}
```
