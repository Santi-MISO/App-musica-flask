# Se importa desde el modulo principal -flaskr- a la función de creación de la app
from flaskr import create_app

# Se instancia a la aplicación
app = create_app('default')

# Se le hace push al contexto de la aplicación
app_context = app.app_context()
app_context.push()