FROM python:3.11.10-alpine3.20

# Establece el directorio de trabajo
WORKDIR /app

# Copia solo el archivo requirements.txt primero para evitar reinstalar dependencias innecesariamente
COPY requirements.txt .

# Instala las dependencias, si el archivo requirements.txt cambia, esta capa se volverá a ejecutar
RUN pip install --no-cache-dir -r requirements.txt

# Luego copia el resto del código
COPY . .

# Define el punto de entrada de la aplicación
ENTRYPOINT [ "python", "./src/main.py" ]
