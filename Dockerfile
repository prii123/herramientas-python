# Usa una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt y los instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de tu proyecto al directorio de trabajo
COPY . .

# Define el comando por defecto para ejecutar tu aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
