from functools import lru_cache
from typing import Union
import httpx
from bs4 import BeautifulSoup

# LRU Cache para la función de obtener UF
@lru_cache(maxsize=100)
def get_uf(url: str, day: int, month: int) -> Union[str, None]:
    custom_header: dict[str, str] = {'user-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    try:
        with httpx.Client() as client:
            # Agregar un tiempo de espera de 10 segundos
            res = client.get(url, headers=custom_header, timeout=10.0)
            res.raise_for_status()  # Lanza un error si la solicitud falla
            soup = BeautifulSoup(res.text, 'html.parser')
            table = soup.find('table', id='table_export')
            table_body = table.find('tbody')
            rows = table_body.find_all('tr')
            current_row = rows[day - 1]
            months = current_row.find_all('td')
            correct_month = months[month - 1]
            return correct_month.text.strip()

    # Manejo de otros errores de solicitudes
    except httpx.HTTPStatusError as e:
        # Re-lanzar la excepción original con información adicional
        raise RuntimeError(f"Error durante la solicitud a {url}: {e}") from e
    
    except httpx.RequestError as e:
        # Manejo específico de errores de conexión
        raise RuntimeError(f"No se pudo establecer conexión con el servidor. Verifica tu conexión a Internet o la URL: {url}") from e
