
# ejecutar entorno local
python -m venv mi_entorno
mi_entorno/Scripts/activate



# ejecucion por archivo de texto .bat
```código
@echo off

REM Crear y activar el entorno virtual (opcional pero recomendado)
python -m venv myenv
call myenv\Scripts\activate.bat


REM Verificar si la carpeta "herramientas-python" existe
if not exist "herramientas-python" (
	REM La carpeta no existe, hacer un git clone
	git clone https://github.com/prii123/herramientas-python.git

	REM Verificar si el clonado del repositorio fue exitoso
	if errorlevel 1 (
		echo Error: No se pudo clonar el repositorio.
		exit /b 1
	)


) else (
	REM La carpeta existe, hacer un git pull
	cd herramientas-python
	git pull origin main

	REM Verificar si el git pull fue exitoso
	if errorlevel 1 (
		echo Error: No se pudo hacer un git pull del repositorio.
		exit /b 1
	)

   

)

REM Instalar las dependencias
pip install -r requirements.txt

REM Ejecutar el servidor de desarrollo
python manage.py runserver


