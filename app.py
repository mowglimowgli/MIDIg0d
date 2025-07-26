from flask import Flask, request, redirect, render_template, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'change_me'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {"mp3", "wav"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename: str) -> bool:
    """Return True if the filename has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Solo se permiten archivos .mp3 o .wav')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('Archivo subido correctamente')
        return redirect(url_for('download', filename=filename))
    return render_template('index.html')


@app.route('/downloads/<filename>')
def uploaded_file(filename: str):
    """Serve the uploaded file to the user."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/download/<filename>')
def download(filename: str):
    """Show download page for processed file."""
    return render_template('download.html', filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
