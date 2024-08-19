# API de Valores UF

Esta API proporciona información sobre el valor de la Unidad de Fomento (UF) en Chile. Permite consultar el valor de la UF para un día específico o para todos los días de un mes en particular.

## Endpoints Disponibles

- **Obtener el valor UF para un día específico**: Permite consultar el valor de la UF para una fecha específica (día, mes y año).
- **Obtener los valores UF para un mes específico**: Permite consultar los valores de la UF para todos los días de un mes y año específicos.

Para más detalles sobre cómo utilizar estos endpoints y los parámetros requeridos, por favor consulta la documentación completa.

### Instalación

Para instalar las dependencias necesarias, ejecuta:

```bash
pip install -r requirements.txt
```

### Ejecutar el Servidor

```bash
uvicorn api.main:app --reload
```

## Documentación

La `documentación` interactiva de la API está disponible en:

[https://uf-api-fastapi.onrender.com/docs](https://uf-api-fastapi.onrender.com/docs)

## Estructura de carpetas

```text
.
├── endpoints/
│   ├── monthly_uf.py
│   ├── single_uf.py
│   ├── README.md
├── schemas/
│   ├── response.py
├── utils/
│   ├── constants.py
│   ├── get_uf.py
├── .gitignore
├── main.py
├── README.md
├── requirements.txt

```
