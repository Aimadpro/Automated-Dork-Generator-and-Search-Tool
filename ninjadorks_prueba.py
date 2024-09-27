
import subprocess
import sys

# Lista de librerías requeridas
required_libraries = [
    "requests",
    "python-dotenv",
    "rich",
    "gpt4all",
    "openai"
]

# Verificar e instalar cada librería

for lib in required_libraries:
    try:
        __import__(lib)
        print(f"✅ {lib} ya está instalado.")
    except ImportError:
        print(f"Instalando {lib}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

print("Todas las dependencias están instaladas correctamente, coloca los comandos para inciar la consulta")

from dotenv import load_dotenv, set_key
import os 
from results_parser import ResultsParser
from duckduckgosearch import Ducksearch
from file_downloader import FileDownloader
import argparse
import sys 
import subprocess
import sys

# Carga las variables de entorno desde el archivo .env y configura la API KEY de DuckDuckGo.
def env_config():
    """Configurar el archivo .env con los valores proporcionados."""
    # Solicita al usuario la clave API de DuckDuckGo.
    api_key = input("Introduce tu API key de DuckDuckGo: ")
    # Almacena la clave en el archivo .env bajo la variable `API_KEY_DUCK`.
    set_key(".env", "API_KEY_DUCK", api_key)

# Solicita al usuario la clave de API de OpenAI y la guarda en el archivo .env.
def openai_config():
    """
    Solicita al usuario su API KEY de OpenAI y guarda este valor en el archivo .env.
    """
    # Solicita la clave API de OpenAI al usuario.
    api_key = input("Introduce la API KEY de OpenAI: ")
    # Almacena la clave en el archivo .env bajo la variable `OPENAI_KEY`.
    set_key(".env", "OPENAI_KEY", api_key)
    print("Archivo .env configurado satisfactoriamente.")

# Carga el archivo .env, si no existe, lo configura.
def load_env(configure_env):
    """
    Carga las variables del archivo .env al entorno. Si el archivo no existe o se fuerza su configuración, lo crea.
    
    Args:
        configure_env (bool): Indica si se debe configurar el archivo .env, aunque ya exista.

    Returns:
        str: La clave API de DuckDuckGo leída del archivo .env.
    """
    # Comprueba si existe el archivo .env en el directorio.
    env_exists = os.path.exists(".env")
    if not env_exists or configure_env:
        # Si el archivo no existe o se solicita reconfigurar, crea el archivo .env.
        env_config()
        print("Archivo .env configurado.")
        # Finaliza la ejecución del programa después de configurar .env.
        sys.exit(1)

    # Carga las variables del archivo .env en el entorno.
    load_dotenv()
    # Lee la clave API de DuckDuckGo del entorno.
    API_KEY_DUCK = os.getenv("API_KEY_DUCK")
    return API_KEY_DUCK

# Función principal que ejecuta la lógica del programa.
def main(query, configure_env, pages, start_page, date, safe, json, html, download, generateDork):
    """
    Función principal para manejar la lógica de búsqueda y generación de dorks.

    Args:
        query (str): Dork o consulta a realizar.
        configure_env (bool): Indica si se debe configurar el archivo .env.
        pages (int): Número de páginas a buscar.
        start_page (int): Página de inicio para la búsqueda.
        date (str): Rango temporal de la búsqueda.
        safe (str): Nivel de seguridad para el filtrado de contenido.
        json (str): Nombre del archivo para exportar los resultados en formato JSON.
        html (str): Nombre del archivo para exportar los resultados en formato HTML.
        download (str): Tipos de archivo a descargar.
        generateDork (str): Descripción para generar un Google Dork utilizando IA.
    """
    if generateDork:
        # Importa los generadores de IA necesarios para la creación de dorks.
        from ia_agent import OpenAIGenerator, IAagent, GPT4AllGenerator

        # Solicita al usuario confirmar si quiere usar OpenAI o una alternativa local.
        respuesta = ""
        while respuesta.lower() not in ("y", "yes", "n", "no"):
            respuesta = input("¿Quieres utilizar GPT-4 de OpenAI? Si indicas que no, se usará GPT4All local (yes/no): ")

        # Si el usuario confirma, usa el generador de OpenAI.
        if respuesta.lower() in ("y", "yes"):
            # Configurar OpenAI si no está ya configurado.
            load_dotenv()
            if "OPENAI_KEY" not in os.environ:
                openai_config()
                load_dotenv()  # Recarga las variables de entorno.
            openai_gen = OpenAIGenerator()
            ia_agent = IAagent(openai_gen)
        else:
            # Si no se quiere usar OpenAI, utiliza GPT4All como generador.
            print("Utilizando GPT4All local. Puede tardar varios minutos...")
            gpt4all_generator = GPT4AllGenerator()
            ia_agent = IAagent(gpt4all_generator)

        # Genera el dork y muestra el resultado.
        respuesta = ia_agent.generate_gdork(generateDork)
        print(f"\nResultado:\n {respuesta}")
        sys.exit(1)  # Finaliza después de generar el dork.
    # Si no se proporciona ninguna consulta, se muestra un mensaje y se cierra el programa.
    if not query:
        print("Indica una consulta con el comando -q. utiliza el comando -h para mostrar la ayuda.")
        sys.exit()

    # Si se solicita generar un dork, se utiliza un agente de IA.
    
    else:
        # Carga las variables del entorno y obtiene la API Key de DuckDuckGo.
        API_KEY_DUCK = load_env(configure_env=configure_env)
        research = Ducksearch(API_KEY_DUCK)
        # Realiza la búsqueda con los parámetros indicados.
        resultados = research.ducksearch_(query, date=date, safe=safe, start_page=start_page, pages=pages)

    print(query)
    
    # Analiza y muestra los resultados obtenidos en la búsqueda.
    rparser = ResultsParser(resultados)
    rparser.mostrar_pantalla()  # Muestra los resultados en la consola.

    # Si se solicita exportar los resultados a HTML, se realiza.
    if html:
        rparser.exportar_html(html)
    # Si se solicita exportar los resultados a JSON, se realiza.
    if json:
        rparser.exportar_json(json)
    # Si se han especificado archivos a descargar, se ejecuta el descargador.
    if download:
        # Separa las extensiones de archivos en una lista.
        file_types = download.split(",")
        # Filtra y obtiene las URLs de los resultados.
        urls = [resultado['link'] for resultado in resultados]
        fdownloader = FileDownloader("Descargas")  # Instancia el descargador de archivos.
        fdownloader.filtrar_descargar_archivos(urls, file_types)

# Punto de entrada del script.
if __name__ == "__main__":
    # Configura los argumentos del programa.
    parser = argparse.ArgumentParser(description="Herramienta de Hacking con buscadores de manera automática.")
    
    # Argumentos generales.
    parser.add_argument("-q", "--query", type=str, help="Especifica el dork que deseas buscar.")
    parser.add_argument("-c", "--configure", action="store_true", help="Configura o actualiza el archivo .env.")
    parser.add_argument("--start-page", type=int, default=1, help="Define la página de inicio del buscador.")
    parser.add_argument("--pages", type=int, default=1, help="Número de páginas a retornar. Por defecto es 1.")
    parser.add_argument("--date", type=str, default="1", help="Margen temporal d: día pasado, w: semana pasada, m: mes pasado, y: año pasado.")
    parser.add_argument("--safe", type=str, default="1", help="Nivel de filtrado de contenido para adultos (1: Estricto, -1: Moderado, -2: Desactivado).")
    parser.add_argument("--json", type=str, help="Exporta los resultados en formato JSON en el fichero especificado.")
    parser.add_argument("--html", type=str, help="Exporta los resultados en formato HTML en el fichero especificado.")
    parser.add_argument("--download", type=str, default="all", help="Extensiones de archivos a descargar separados por coma.")
    parser.add_argument("-gd", "--generateDork", type=str, help="Genera un dork a partir de una descripción proporcionada por el usuario.")

    # Parseo de los argumentos.
    args = parser.parse_args()
    
    # Llamada a la función principal con los argumentos obtenidos.
    main(query=args.query,
         configure_env=args.configure,
         pages=args.pages,
         start_page=args.start_page,
         date=args.date,
         safe=args.safe,
         json=args.json,
         html=args.html,
         download=args.download,
         generateDork=args.generateDork)
