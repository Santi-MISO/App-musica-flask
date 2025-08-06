# Se importa flask desde las librerias
from flask import Flask

# Se crea la instancia de la aplicación, con entradas por defecto
def create_app(config_name):
    app = Flask(__name__)
    return app