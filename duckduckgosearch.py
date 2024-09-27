import requests

url ="https://serpapi.com/search.json?engine=google&q=Coffee"
class Ducksearch:
    """Clase para realizar búsquedas usando la API personalizada de búsqueda de DuckDuckGo.
    
    Esta clase permite a los usuarios ejecutar búsquedas en DuckDuckGo utilizando la API personalizada,
    manejando la paginación de resultados y permitiendo configurar el idioma de los resultados.

    Attributes:
        api_key (str): Clave de API para acceder a la API de DuckDuckGo.
    """
    def __init__(self,api_key):
        """Inicializa una nueva instancia de GoogleSearch con la clave de API y el ID del motor de búsqueda.

        Args:
            api_key (str): La clave de API para acceder a la API de DuckDuckGo.
        """
        self.api_key=api_key
        pass
    def ducksearch_(self,query,date='y',safe=-2,start_page=1,pages=1):
        """Realiza una búsqueda en DuckDuckGo utilizando la API.

        La función gestiona la paginación y la recuperación de los resultados de la búsqueda,
        procesando cada página según se especifica.

        Args:
            query (str): Texto de la consulta para la búsqueda.
            date (str): Antinguedad máxima de la búsqueda.
            safe (int): filtrado de contenido
            start_page (int): Página inicial desde la que empezar la búsqueda.
            pages (int): Número de páginas de resultados a recuperar.
            

        Returns:
            list[dict]: Lista de resultados personalizados de la búsqueda, cada uno como un diccionario.

        Raises:
            Exception: Si la respuesta de la API tiene un estado HTTP que no es 200.
        """
        final_results = []
        results_per_page = 10  # DuckDuckgo muestra 10 resultados por página
        for page in range(pages):
            start_index = (start_page - 1) * results_per_page + 1 + (page * results_per_page)
            url = (f"https://serpapi.com/search.json?engine=duckduckgo&q={query}&safe={safe}"
                   f"&df={date}&start={start_index}&num={results_per_page}&api_key={self.api_key}")
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                results = data.get("organic_results", [])
                cresults = self.custom_results(results)
                final_results.extend(cresults)
            else:
                error_msg = f"Error obtaining page {page + 1}: HTTP {response.status_code}"
                print(error_msg)
                raise Exception(error_msg)

        return final_results

    def custom_results(self, results):
        """Procesa y filtra los resultados brutos de la API de búsqueda de Google.

        Args:
            results (list[dict]): Lista de resultados brutos de la API.

        Returns:
            list[dict]: Lista de resultados procesados, cada uno con título, descripción y enlace.
        """
        custom_results = []
        for result in results:
            cresult = {
                "title": result.get("title"),
                "description": result.get("snippet"),
                "link": result.get("link")
            }
            custom_results.append(cresult)
        return custom_results