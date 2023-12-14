# Utiliza una imagen base de Python
FROM python:3.7.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el resto de los archivos al contenedor
COPY . .

# Comando para ejecutar tu aplicación (ajústalo según tu proyecto)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
