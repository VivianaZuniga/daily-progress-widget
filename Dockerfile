# 1. Usamos una imagen oficial de Python ligera
FROM python:3.11-slim

# 2. Evita que Python escriba archivos .pyc en el contenedor
ENV PYTHONDONTWRITEBYTECODE 1
# 3. Fuerza a que los prints salgan directo a la terminal sin retrasos
ENV PYTHONUNBUFFERED 1

# 4. Creamos y nos mudamos a la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 5. Copiamos el archivo de librerías primero (ayuda a que Docker sea más rápido)
COPY requirements.txt /app/

# 6. Instalamos las librerías de Python dentro del contenedor
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiamos todo el resto del código de tu proyecto a la carpeta /app
COPY . /app/

# 8. El comando por defecto que se ejecutará al arrancar
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]