import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import pvd_core

# Konfigurasi aplikasi Flask
app = Flask(__name__)
# app.config = 'supersecretkey'
# app.config = 'static/uploads/'
# app.config = 16 * 1024 * 1024 # Batas ukuran file 16MB

app.secret_key = 'supersecretkey'  # untuk flash message dan session
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB


ALLOWED_EXTENSIONS = {'png', 'bmp', 'tiff'} # Format lossless lebih disarankan

def allowed_file(filename):
    """Memeriksa apakah ekstensi file diizinkan."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Menampilkan halaman utama."""
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed_route():
    """Menangani proses penyisipan data."""
    if 'cover_image' not in request.files or 'secret_message' not in request.form:
        flash('Formulir tidak lengkap.')
        return redirect(url_for('index'))

    file = request.files['cover_image']
    message = request.form['secret_message']
    

    if file.filename == '' or message == '':
        flash('Gambar penampung dan pesan rahasia tidak boleh kosong.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_dir = app.config['UPLOAD_FOLDER']
        original_path = os.path.join(upload_dir, 'original_' + filename)
        stego_path = os.path.join(upload_dir, 'stego_' + filename)
        
        # DEBUG LOG
        print("[DEBUG] File yang diupload      : ", filename)
        print("[DEBUG] Pesan yang disembunyikan: ", message)

        file.save(original_path)

        try:
            cover_image = Image.open(original_path).convert('RGB')
            stego_image = pvd_core.embed(cover_image, message)
            stego_image.save(stego_path)
            
            return render_template('index.html', 
                                   original_image_url=url_for('uploads', filename='original_' + filename),
                                   stego_image_url=url_for('uploads', filename='stego_' + filename))
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
    """Menangani proses ekstraksi data."""
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
    """Menyajikan file yang diunggah untuk pratinjau."""
    # return send_from_directory(app.config, filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # if not os.path.exists(app.config):
    #     os.makedirs(app.config)
        
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    app.run(debug=True)