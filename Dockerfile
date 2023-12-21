# # Usa una imagen base de Python
# # docker run -d -p 8000:8000 --name mi_contenedor nombre_imagen
# # docker build -t nombre_imagen .


# FROM python:3.9

# # Establece el directorio de trabajo en /app
# WORKDIR /app

# # Instala Chrome y ChromeDriver
# RUN apt-get update && apt-get -y install wget unzip
# # RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# # RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# # RUN apt-get -y update && apt-get -y install google-chrome-stable
# # RUN wget -N https://chromedriver.storage.googleapis.com/$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip -P /tmp/
# # RUN unzip /tmp/chromedriver_linux64.zip -d /tmp/
# # RUN mv /tmp/chromedriver /usr/local/bin/chromedriver
# # RUN chmod +x /usr/local/bin/chromedriver

# RUN wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
# RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/
# RUN chmod +x /usr/local/bin/chromedriver

# # Copia el archivo requirements.txt y los instala
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copia todo el contenido de tu proyecto al directorio de trabajo
# COPY . .

# # Define el comando por defecto para ejecutar tu aplicación
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Usa una imagen oficial de Python como base
FROM python:3.9

WORKDIR /app

# Instala las dependencias necesarias para Selenium y Chrome
RUN apt-get update && apt-get -y install wget unzip


# Copia los archivos de tu aplicación a la imagen
WORKDIR /app
COPY . /app

# Copia el driver de Chrome desde tu proyecto a la ubicación deseada en el contenedor
COPY drivers/chromedriver /usr/local/bin/chromedriver

# Establece la variable de entorno para que Selenium pueda encontrar el driver
ENV PATH="/usr/local/bin/chromedriver:${PATH}"

# Instala las dependencias de tu aplicación
RUN pip install -r requirements.txt

# Comando para ejecutar tu aplicación Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
