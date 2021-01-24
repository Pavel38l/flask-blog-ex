from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from app.generator import Generator
app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
generator = Generator()
from app import routes

