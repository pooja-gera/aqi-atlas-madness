from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__, template_folder='../templates',
            static_folder='../static')
app.config['SECRET_KEY'] = 'my secret key'
