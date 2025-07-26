

app = Flask(__name__)
app.secret_key = 'change_me'
UPLOAD_FOLDER = 'uploads'



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


if __name__ == '__main__':
    app.run(debug=True)
