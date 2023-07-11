from flask import Flask
from dotenv import load_dotenv
load_dotenv('.env')

app = Flask(__name__, template_folder='../templates',
            static_folder='../static')
app.config['MONGO_URI'] = app.config['MONGO_URI']
