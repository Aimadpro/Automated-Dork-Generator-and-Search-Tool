🔍 DorkFinder: Herramienta de Hacking para Búsqueda Automatizada con Dorks e Integración de IA
Descripción
DorkFinder es una herramienta automatizada para realizar búsquedas avanzadas (dorks) en motores de búsqueda utilizando DuckDuckGo, complementado con análisis y generación de consultas con ayuda de inteligencia artificial. Este proyecto tiene como objetivo facilitar la investigación de información en internet a través de técnicas de dorks, permitiendo a los usuarios realizar búsquedas específicas y descargar archivos de manera automática.

Características
🌐 Búsquedas Automatizadas: Realiza búsquedas avanzadas en motores como DuckDuckGo usando dorks.
🤖 Generación de Dorks con IA: Genera dorks automáticamente usando GPT-4 de OpenAI o GPT4All local.
📄 Descarga de Archivos: Filtra y descarga archivos automáticamente de las búsquedas realizadas.
📋 Exportación de Resultados: Exporta los resultados de las búsquedas en formatos JSON y HTML.
🔧 Configuración Personalizada: Permite configurar claves de API y ajustes de búsqueda a través de un archivo .env.
Parámetros disponibles
-q o --query: La consulta que deseas ejecutar.
-c o --configure: Configura o actualiza el archivo .env con las claves de API.
--pages: Número de páginas a analizar en los resultados de búsqueda.
--start-page: Página desde la que se comenzará a buscar.
--date: Rango temporal de la búsqueda (d: día, w: semana, m: mes, y: año).
--safe: Nivel de filtrado de contenido para adultos (1: Estricto, -1: Moderado, -2: Desactivado).
--json: Exporta los resultados en formato JSON.
--html: Exporta los resultados en formato HTML.
--download: Descarga archivos específicos por extensión (ej: pdf, docx, xls).
-gd o --generateDork: Genera dorks basados en una descripción dada por el usuario usando un modelo de IA.

⚙️ Uso
Ejemplo de uso para generar dorks con IA: python dorkfinder.py -gd "Búsqueda de archivos .env en repositorios de GitHub"
Ejemplo de uso para ejecutar el script principal y comenzar con las búsquedas, usa el siguiente comando: python dorkfinder.py -q "site:example.com filetype:pdf" --pages 2 --download pdf

🚀 Flujo de trabajo
Carga de Configuración: El script comienza verificando si el archivo .env está presente. Si no, solicita al usuario que ingrese las claves de API y las guarda automáticamente.
Ejecución de Búsqueda: Realiza la consulta en DuckDuckGo o Google según la configuración y parámetros dados.
Análisis y Descarga: Los resultados se analizan y, si se especifica, se descargan los archivos encontrados.
Integración con IA: Si se requiere, el script puede generar dorks utilizando IA para mejorar la precisión de las búsquedas.

📜 Licencia Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
✉️ Contacto Para cualquier consulta o sugerencia, no dudes en ponerte en contacto:
Nombre: Aimad Aisa Driouchi Correo: aaisad2324@politecnics.barcelona Mi Perfil de LinkedIn
