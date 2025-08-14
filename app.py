from flask import Flask, request, redirect, render_template, send_from_directory, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = 'bu-cok-gizli-bir-anahtar'

UPLOAD_FOLDER = 'yuklenen_dosyalar'
OWNER_PASSWORD = '1234'  # Yönetici şifresi
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('dosya')
    if file and file.filename != '':
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        flash("✅ Dosyanız başarıyla yüklendi!")
    else:
        flash("❌ Dosya yüklenirken bir hata oluştu veya dosya seçilmedi.")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sifre = request.form.get('sifre')
        if sifre == OWNER_PASSWORD:
            session['admin'] = True
            return redirect(url_for('show_files'))
        else:
            flash("⛔ Şifre yanlış!")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/dosyalar')
def show_files():
    if not session.get('admin'):
        return redirect(url_for('login'))
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('files.html', files=files)

@app.route('/indir/<filename>')
def download(filename):
    if not session.get('admin'):
        return redirect(url_for('login'))
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
