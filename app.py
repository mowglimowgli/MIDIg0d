from flask import (
    Flask,
    request,
    redirect,
    render_template,
    flash,
    url_for,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import os
from typing import List

import librosa
import numpy as np
import pretty_midi

app = Flask(__name__)
app.secret_key = 'change_me'
UPLOAD_FOLDER = 'uploads'
MIDI_FOLDER = 'midi'
ALLOWED_EXTENSIONS = {"mp3", "wav"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MIDI_FOLDER'] = MIDI_FOLDER


def allowed_file(filename: str) -> bool:
    """Return True if the filename has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_notes(path: str) -> List[pretty_midi.Note]:
    """Detect notes in an audio file and return a list of PrettyMIDI Notes."""
    y, sr = librosa.load(path, sr=None, mono=True)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
    f0, voiced, _ = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7"),
        sr=sr,
    )
    notes: List[pretty_midi.Note] = []
    onset_indices = list(onset_frames) + [len(f0)]
    for start_frame, end_frame in zip(onset_indices[:-1], onset_indices[1:]):
        pitch_region = f0[start_frame:end_frame]
        voiced_region = voiced[start_frame:end_frame]
        if not np.any(voiced_region):
            continue
        freq = np.nanmedian(pitch_region[voiced_region])
        pitch = int(np.round(librosa.hz_to_midi(freq)))
        velocity = int(
            127
            * np.mean(rms[start_frame:end_frame])
            / (np.max(rms) if np.max(rms) > 0 else 1)
        )
        start = times[start_frame]
        end = times[end_frame]
        notes.append(
            pretty_midi.Note(
                velocity=max(1, min(127, velocity)),
                start=float(start),
                end=float(end),
                pitch=pitch,
            )
        )
    return notes


def audio_to_midi(audio_path: str, midi_path: str) -> None:
    """Convert an audio file to MIDI and store the result."""
    pm = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    instrument = pretty_midi.Instrument(program=piano_program)
    instrument.notes = extract_notes(audio_path)
    pm.instruments.append(instrument)
    pm.write(midi_path)


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
        os.makedirs(app.config['MIDI_FOLDER'], exist_ok=True)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        midi_name = os.path.splitext(filename)[0] + '.mid'
        midi_path = os.path.join(app.config['MIDI_FOLDER'], midi_name)
        try:
            audio_to_midi(file_path, midi_path)
            flash('Archivo convertido a MIDI')
            return redirect(url_for('download', filename=midi_name))
        except Exception as exc:
            flash(f'Error al procesar el archivo: {exc}')
            return redirect(request.url)
    return render_template('index.html')


@app.route('/downloads/<filename>')
def uploaded_file(filename: str):
    """Serve the processed MIDI file to the user."""
    return send_from_directory(app.config['MIDI_FOLDER'], filename, as_attachment=True)


@app.route('/download/<filename>')
def download(filename: str):
    """Show download page for processed file."""
    return render_template('download.html', filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
