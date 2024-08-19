"""
Este archivo configura y lanza la aplicación FastAPI para la API de valores UF.

La aplicación incluye los siguientes enrutadores:
- `single_uf_router`: Rutas para obtener el valor de la UF para una fecha específica.
- `monthly_uf_router`: Rutas para obtener los valores de la UF para un mes específico.

La aplicación expone dos conjuntos de rutas bajo los siguientes prefijos:
- `/uf`: Para acceder a los endpoints relacionados con valores UF individuales.
- `/monthly-uf`: Para acceder a los endpoints relacionados con valores UF mensuales.

La raíz de la API (`/`) proporciona un mensaje de bienvenida que confirma que la API está en funcionamiento.
"""

from fastapi import FastAPI
from .endpoints.single_uf import router as single_uf_router
from .endpoints.monthly_uf import router as monthly_uf_router


app = FastAPI()

@app.get("/")
def read_root():
    """
    Esta función maneja una solicitud GET a la ruta raíz ("/") de la API.
    Devuelve un mensaje de confirmación para verificar que la API está 
    en funcionamiento y respondiendo correctamente.
    """
    return {"message": "Health check baby"}

# Incluye las rutas para obtener el valor de UF para una fecha específica
app.include_router(single_uf_router)

# Incluye las rutas para obtener los valores de UF para un mes específico
app.include_router(monthly_uf_router)
