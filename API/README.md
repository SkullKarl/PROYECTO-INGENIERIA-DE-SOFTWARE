# Instrucciones para Configurar el Entorno y Ejecutar la Aplicación

Este proyecto utiliza un entorno virtual para gestionar las dependencias. A continuación se detallan los pasos para configurar el entorno virtual, instalar las dependencias necesarias y ejecutar la aplicación.

## Configuración del Entorno Virtual

Sigue los siguientes pasos en el terminal para crear y activar el entorno virtual, instalar las dependencias y ejecutar la aplicación.

### 1. Crear el Entorno Virtual

Ejecuta el siguiente comando en el terminal desde la raíz del proyecto para crear un entorno virtual llamado `.env`:

```bash
python3 -m venv .env
```

### 2. Activar el Entorno Virtual
Una vez creado el entorno, actívalo con el siguiente comando:

En Windows:

```bash
Copiar código
.env\Scripts\activate
```

En macOS/Linux:

```bash
Copiar código
source .env/bin/activate
```

### 3. Instalar Dependencias
Con el entorno virtual activo, instala las dependencias especificadas en requirements.txt ejecutando:

```bash
Copiar código
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación
Para iniciar la aplicación, simplemente ejecuta el siguiente comando:

```bash
Copiar código
python app.py
```

### Notas Adicionales
* Asegúrate de activar el entorno virtual cada vez que trabajes en el proyecto para evitar conflictos de dependencias.
* Si deseas desactivar el entorno virtual, utiliza el comando deactivate en el terminal.
* Asegúrate de que el archivo .env y cualquier archivo de configuración sensible estén incluidos en .gitignore para evitar subirlos al repositorio.
