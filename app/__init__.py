import os
from flask import Flask
from app.models import FileWorker, RLECompression, FileProcessor

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = './uploads'
app.secret_key = os.urandom(52)

file_handler = FileWorker(app.config['UPLOAD_FOLDER'])
compression_strategy = RLECompression()
file_processor = FileProcessor(compression_strategy, file_handler)


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
