# Se importa flask desde las librerias
from flask import Flask

# Se crea la instancia de la aplicación, con entradas por defecto
def create_app(config_name):
    app = Flask(__name__)

    # Indicar que se va a usar una base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///canciones.db'

    # Desactivar momentaneamente ciertos warnings que se presentarían en la base de datos 
    # mientras la app está en etapa de desarrollo
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app