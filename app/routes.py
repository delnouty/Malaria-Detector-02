from flask import request, redirect, url_for, send_from_directory, render_template, flash, jsonify
from werkzeug.utils import secure_filename
import os
from .ml_model import MalariaDetector

def init_routes(app):
    detector = MalariaDetector()

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('Veuillez sélectionner une image à analyser.', 'error')
                return redirect(url_for('upload_file'))
            
            file = request.files['file']
            if file.filename == '':
                flash('Aucune image sélectionnée.', 'error')
                return redirect(url_for('upload_file'))
            
            if not allowed_file(file.filename):
                flash('Format de fichier non supporté. Utilisez PNG, JPG, JPEG ou GIF.', 'error')
                return redirect(url_for('upload_file'))
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                try:
                    file.save(file_path)
                    # Faire la prédiction
                    result = detector.predict(file_path)
                    return jsonify(result)
                except Exception as e:
                    flash(f'Erreur lors de l\'analyse : {str(e)}', 'error')
                    return redirect(url_for('upload_file'))
                
        return render_template('index.html')

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        try:
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        except FileNotFoundError:
            flash('Fichier non trouvé.', 'error')
            return redirect(url_for('upload_file')) 