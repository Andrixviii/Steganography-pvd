import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import base64
from io import BytesIO
import pvd_core  # pastikan file ini ada di repo kamu atau installable

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed_route():
    if 'cover_image' not in request.files or 'secret_message' not in request.form:
        flash('Formulir tidak lengkap.')
        return redirect(url_for('index'))

    file = request.files['cover_image']
    message = request.form['secret_message']

    if file.filename == '' or message == '':
        flash('Gambar penampung dan pesan rahasia tidak boleh kosong.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        try:
            cover_image = Image.open(file.stream).convert('RGB')
            stego_image = pvd_core.embed(cover_image, message)

            stego_io = BytesIO()
            stego_image.save(stego_io, format='PNG')
            stego_io.seek(0)
            stego_base64 = base64.b64encode(stego_io.read()).decode('utf-8')
            stego_data_url = f"data:image/png;base64,{stego_base64}"

            cover_io = BytesIO()
            cover_image.save(cover_io, format='PNG')
            cover_io.seek(0)
            cover_base64 = base64.b64encode(cover_io.read()).decode('utf-8')
            cover_data_url = f"data:image/png;base64,{cover_base64}"

            return render_template('index.html',
                                   original_image_url=cover_data_url,
                                   stego_image_url=stego_data_url)
        except ValueError as e:
            flash(str(e))
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Terjadi kesalahan: {e}')
            return redirect(url_for('index'))
    else:
        flash('Jenis file tidak diizinkan. Gunakan PNG, BMP, atau TIFF.')
        return redirect(url_for('index'))

@app.route('/extract', methods=['POST'])
def extract_route():
    if 'stego_image' not in request.files:
        flash('Silakan unggah citra stego.')
        return redirect(url_for('index'))
        
    file = request.files['stego_image']

    if file.filename == '':
        flash('Tidak ada file yang dipilih.')
        return redirect(url_for('index'))
        
    if file and allowed_file(file.filename):
        try:
            stego_image = Image.open(file.stream).convert('RGB')
            extracted_message = pvd_core.extract(stego_image)
            
            return render_template('index.html', extracted_message=extracted_message)
        except Exception as e:
            flash(f'Gagal mengekstrak pesan: {e}')
            return redirect(url_for('index'))
    else:
        flash('Jenis file tidak diizinkan.')
        return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 🚀 Bagian penting untuk Railway
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
