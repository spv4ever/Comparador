# Comparador de Ficheros Pro ✨

Herramienta de escritorio construida en Python para comparar dos ficheros (Excel o CSV), identificar diferencias a nivel de fila y de valor, y exportar los resultados. Ideal para tareas de conciliación de datos, auditorías o control de calidad de la información.

<img width="639" height="473" alt="image" src="https://github.com/user-attachments/assets/7b64bab5-b413-4d90-9e1f-4e7dc46b4397" />

<img width="1191" height="822" alt="image" src="https://github.com/user-attachments/assets/1385d238-a9e3-4c7b-be54-8c10b643aebb" />




---

## 🚀 Características Principales

*   **Carga Flexible**: Soporta ficheros `.xlsx` y `.csv` sin una estructura de columnas fija.
*   **Clave de Comparación Dinámica**: Permite seleccionar una o varias columnas para crear una clave de identificación única, incluso si los nombres de las columnas no coinciden entre ficheros.
*   **Doble Motor de Comparación**:
    1.  **Comparador de Filas**: Identifica las filas que existen en un fichero pero no en el otro.
    2.  **Comparador de Valores**: Para las filas que sí coinciden, permite comparar el valor de una columna específica y resalta las diferencias.
*   **Interfaz Gráfica Moderna**: Construida con `Tkinter` y `ttkthemes` para una experiencia de usuario limpia e intuitiva.
*   **Exportación de Resultados**: Todos los resultados de las comparaciones pueden ser exportados fácilmente a Excel o CSV.
*   **Empaquetado como Ejecutable**: Preparado para ser convertido en un archivo `.exe` para Windows, sin necesidad de instalar Python.

---

## 🔧 ¿Cómo Usar la Aplicación?

1.  **Cargar Ficheros**: Usa los botones "Cargar Fichero 1" y "Cargar Fichero 2" para seleccionar tus datos.
2.  **Seleccionar Claves de Unión**:
    *   Haz clic en "Seleccionar..." para cada fichero.
    *   En la ventana emergente, marca las casillas de las columnas que formarán el ID único. Puedes usar el buscador para filtrar la lista.
3.  **(Opcional) Comparar Valores**:
    *   Si deseas comparar un campo específico en las filas coincidentes, selecciónalo en los menús desplegables "Comparar valor de:". Debes seleccionar una columna en ambos ficheros.
4.  **Realizar Comparación**: Haz clic en el botón central "Realizar Comparación".
5.  **Revisar Resultados**:
    *   **Pestaña "Faltan en Fichero 2"**: Muestra las filas que están en el fichero 1 pero no en el 2.
    *   **Pestaña "Faltan en Fichero 1"**: Muestra las filas que están en el fichero 2 pero no en el 1.
    *   **Pestaña "Diferencias de Valor"**: Muestra el ID, el valor del fichero 1 y el valor del fichero 2 para las filas donde no coinciden.
6.  **Exportar**: Usa el botón "Exportar a Excel/CSV" en cada pestaña para guardar los resultados.

---

## 🛠️ Instalación y Ejecución (para Desarrolladores)

Si deseas ejecutar el proyecto desde el código fuente, sigue estos pasos.

### Requisitos

*   Python 3.9+
*   Librerías: `pandas`, `openpyxl`, `ttkthemes`, `pyinstaller`

### Pasos

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/spv4ever/Comparador.git
    cd Comparador
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    *   En Windows: `venv\Scripts\activate`
    *   En macOS/Linux: `source venv/bin/activate`

3.  **Instala las dependencias:**
    Crea un archivo `requirements.txt` con el siguiente contenido:
    ```txt
    pandas
    openpyxl
    ttkthemes
    pyinstaller
    pyinstaller-hooks-contrib
    ```
    Y luego instálalo:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación:**
    ```bash
    python main.py
    ```

---

## 📦 Crear el Ejecutable (`.exe`)

Para empaquetar la aplicación en un único archivo `.exe` para Windows, asegúrate de tener `pyinstaller` instalado y sigue estos pasos:

1.  Prepara un icono (`icon.ico`) y una imagen de pantalla de carga (`splash.png`) en la carpeta raíz del proyecto (opcional pero recomendado).
2.  Abre una terminal en la carpeta del proyecto.
3.  Ejecuta el siguiente comando:
    ```bash
    pyinstaller --onefile --windowed --name="ComparadorPro" --splash="splash.png" main.py
    ```
    > **Nota**: Si no tienes un archivo de splash, simplemente elimina la opción `--splash="splash.png"`.

4.  El ejecutable final se encontrará en la carpeta `dist/`.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
