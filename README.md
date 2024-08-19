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

### Ejecutar el Servidor

```bash
uvicorn api.main:app --reload
```

Sirviendo en: http://127.0.0.1:8000
Documentación de la API: http://127.0.0.1:8000/docs

## Uso

### Endpoints Disponibles

- **Obtener el valor UF para un día específico**: Permite consultar el valor de la UF para una fecha específica (día, mes y año).
- **Obtener los valores UF para un mes específico**: Permite consultar los valores de la UF para todos los días de un mes y año específicos.

Para más detalles sobre cómo utilizar estos endpoints y los parámetros requeridos, por favor consulta la `documentación` completa en el siguient enlace: https://uf-api-fastapi.onrender.com/docs
