# MIDIg0d


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


## Funcionalidades avanzadas (ideas futuras)

- Elegir el número de stems al separar el audio.
- Ajustar parámetros para la conversión a MIDI.
- Gestionar varias tareas en cola y mostrar una barra de progreso.

Con estas extensiones MIDIg0d podría adaptarse a usuarios con necesidades más específicas sin perder su simplicidad.
