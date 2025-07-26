# MIDIg0d

MIDIg0d es una pequeña aplicación web para separar audio y descargar el resultado en formato MIDI. Ha sido pensada para usuarios sin experiencia previa y solo requiere conocimientos básicos de Python.



Instala todo en un entorno virtual para evitar problemas con otros proyectos:

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa venv\Scripts\activate
pip install -r requirements.txt
```

## Puesta en marcha

1. Ejecuta la aplicación con:
   ```bash
   python app.py
   ```
2. Abre tu navegador en `http://127.0.0.1:5000/`.
3. Usa el botón **Subir** para cargar un archivo `.mp3` o `.wav`.
4. Tras la subida aparecerá un enlace para descargar el archivo procesado.

Los archivos que subas quedarán en la carpeta `uploads/`.

## Funcionalidades avanzadas (ideas futuras)

- Elegir el número de stems al separar el audio.
- Ajustar parámetros para la conversión a MIDI.
- Gestionar varias tareas en cola y mostrar una barra de progreso.

Con estas extensiones MIDIg0d podría adaptarse a usuarios con necesidades más específicas sin perder su simplicidad.
