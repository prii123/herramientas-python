# web-scraping

#Driver

docker pull selenium/standalone-chrome

#correr Driver

docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-chrome:latest

# correr imagen scraping
docker run -p 3000:8000 -d scraping_dian




# ejecucion por archivo de texto .bat
@echo off

REM Crear y activar el entorno virtual (opcional pero recomendado)
python -m venv myenv
call myenv\Scripts\activate.bat


REM Verificar si la carpeta "web-scraping" existe
if not exist "web-scraping" (
    REM La carpeta no existe, hacer un git clone
    git clone https://github.com/prii123/web-scraping.git

    REM Acceder al directorio del proyecto clonado
    cd web-scraping
) else (
    REM La carpeta existe, hacer un git pull
    cd web-scraping
    git pull origin main
)



REM Instalar las dependencias
pip install -r requirements.txt

REM Ejecutar el servidor de desarrollo
python manage.py runserver


