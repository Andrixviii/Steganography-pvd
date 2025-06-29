import os
from flask import Flask, render_template, request, redirect, url_for, flash
from PIL import Image
import base64
from io import BytesIO
# Pastikan Anda memiliki file pvd_core.py di direktori yang sama
import pvd_core 

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ekstensi file yang diizinkan
ALLOWED_EXTENSIONS = {'png', 'bmp', 'tiff', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed_route():
    if 'cover_image' not in request.files or 'secret_message' not in request.form:
        flash('Formulir tidak lengkap.', 'error')
        return redirect(url_for('index'))

    file = request.files['cover_image']
    message = request.form['secret_message']

    if file.filename == '' or message == '':
        flash('Gambar penampung dan pesan rahasia tidak boleh kosong.', 'error')
        return redirect(url_for('index'))

    if file and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'bmp'}:
        try:
            cover_image = Image.open(file.stream).convert('RGB')
            stego_image = pvd_core.embed(cover_image, message)

            # Konversi gambar hasil stego ke Base64 Data URL
            stego_io = BytesIO()
            stego_image.save(stego_io, format='PNG')
            stego_io.seek(0)
            stego_base64 = base64.b64encode(stego_io.read()).decode('utf-8')
            stego_data_url = f"data:image/png;base64,{stego_base64}"

            # Konversi gambar asli ke Base64 Data URL
            cover_io = BytesIO()
            cover_image.save(cover_io, format='PNG')
            cover_io.seek(0)
            cover_base64 = base64.b64encode(cover_io.read()).decode('utf-8')
            cover_data_url = f"data:image/png;base64,{cover_base64}"
            
            # Render template dengan URL gambar
            return render_template('index.html',
                                   original_image_url=cover_data_url,
                                   stego_image_url=stego_data_url)
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Terjadi kesalahan saat embedding: {e}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Jenis file tidak diizinkan. Gunakan PNG, JPG, BMP, atau TIFF.', 'error')
        return redirect(url_for('index'))

@app.route('/extract', methods=['POST'])
def extract_route():
    if 'stego_image' not in request.files:
        flash('Silakan unggah citra stego.', 'error')
        return redirect(url_for('index'))
        
    file = request.files['stego_image']

    if file.filename == '':
        flash('Tidak ada file yang dipilih.', 'error')
        return redirect(url_for('index'))
        

    if file and file.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'bmp'}:
        try:
            stego_image = Image.open(file.stream).convert('RGB')
            extracted_message = pvd_core.extract(stego_image)
            
            if not extracted_message:
                 flash('Tidak ada pesan tersembunyi yang ditemukan.', 'error')
                 return redirect(url_for('index'))

            # Render template dengan pesan yang diekstrak
            return render_template('index.html', extracted_message=extracted_message)
        
        except Exception as e:
            flash(f'Gagal mengekstrak pesan: {e}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Jenis file tidak diizinkan untuk ekstraksi. Gunakan format PNG, JPG, JPEG, atau BMP.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Membuat folder upload jika belum ada (opsional, karena tidak dipakai)
    upload_folder = 'static/uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)