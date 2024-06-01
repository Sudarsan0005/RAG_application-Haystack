import os
from flask_cors import CORS
from retriver import _responseGenerator
from flask import Flask, request, jsonify
from embedDbGenerator import documentStore
from constant import *

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            print("no filename")
            return None
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            if documentStore([filepath]):
                return jsonify({"uploadStatus":"Inserted to DB successfully!","status":1})
            return jsonify({"uploadStatus": "Failed to insert", "status": 0})
        return jsonify({"uploadStatus": "Please Upload .txt FILE", "status": 0})
    return jsonify({"uploadStatus": "Use Post method", "status": 0})


@app.route('/query', methods=['POST'])
def query():
    if request.method == 'POST':
        if not os.listdir(DB_FOLDER):
            return jsonify({"ragResponse": "DB doesn't exhist so please upload documents", 'status': 0})
        if 'question' not in request.form:
            print("Provide query")
            return "provide query"
        query = request.form.get('question')
        response = _responseGenerator(query)
        return jsonify({'ragResponse':response,'status':1})
    return jsonify({"ragResponse":"Use POST method",'status':0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001, debug=False)
