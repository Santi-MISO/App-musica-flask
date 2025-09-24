# Se importa desde el modulo principal -flaskr- a la función de creación de la app
from flaskr import create_app

# Se importan la base de datos y la clase Cancion
from .models import db, Cancion, Usuario, Album, Medio

# Se importa el esquema (autoschema) para la serialización
from .models import AlbumSchema

# Se importa Api
from flask_restful import Api

# Se importan las vistas
from .vistas import VistaCanciones, VistaCancion, VistaAlbumes, VistaAlbum, VistaUsuarios, VistaUsuario

# Se instancia a la aplicación
app = create_app('default')

# Se le hace push al contexto de la aplicación
app_context = app.app_context()
app_context.push()

# Se inicializa la base de datos
db.init_app(app)

# Se crean todas las tablas que se definieron como clases
db.create_all()

# Se crea inicializa el api
api = Api(app) # Se iniciliza la aplicación con la app
api.add_resource(VistaCanciones, '/canciones') # VistaCanciones es el recurso, '/canciones' es la url con la que se accede al recurso
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>') # Se añade VistaCancion como recurso, la url '/cancion/<int:id_cancion>' es la url de la cancion con id id_cancion, int indica que id_cancion es entero, se usa <> porque es una variable
api.add_resource(VistaAlbumes, '/albumes') # VistaAlbumes es el recurso, '/albumes' es la url con la que se accede al recurso
api.add_resource(VistaAlbum, '/album/<int:id_album>') # VistaAlbum es el recurso, la url es '/album/<int:id_album>' con id id_cancion, int indica que el id es entero, se usa <> porque se está viendo una variable
api.add_resource(VistaUsuarios, '/usuarios') # VistaUsuarios es el recurso, '/usuarios' es la url del recurso
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>') # VistaUsuario es el recurso, se accede a este con la url '/usuario/<int:id_usuario>', con id id_usuario, se usa int porque id es un entero, se usa <> porque se maneja una variable

# ------------------------------------------------------

# Se realiza una prueba para comprobar el estado de la base de datos y la clase
with app.app_context():
    # Para probar la clase Cancion, se crea el objeto prueba_cancion
    prueba_cancion = Cancion(titulo='Titulo de prueba', minutos=2, segundos=35, interprete='Santiago Felipe')
    
    # Se añade el objeto prueba_cancion a la base de datos
    db.session.add(prueba_cancion)

    # Se hace commit para que se guarde el objeto en la base de datos
    db.session.commit()

    # Para verificar que todo se realizó correctamente, se hace una consulta a la base de datos
    print(Cancion.query.all()) # Muestra en consola la canción que fue agregada en la prueba

    # ------------------------------------------------------

    # Para probar la clase Usuario y la clase Album
    prueba_usuario = Usuario(nombre_usuario='Usuario de prueba', contrasena='12345')
    prueba_album = Album(titulo='Album de prueba', anio=1998, descripcion='Descripcion de prueba', medio=Medio.CD)

    # Para probar la asociacion del album con el usuario
    prueba_usuario.albums.append(prueba_album)

    # Se añade el objeto prueba_usuario a la base de datos
    db.session.add(prueba_usuario)

    # Se hace commit para que se guarde el objeto en la base de datos
    db.session.commit()

    # Para verificar que todo se realizó correctamente, se hace una consulta a la base de datos
    print(Usuario.query.all()) # Muestra en consola el usuario que fue agregado en la prueba

    # Para verificar que la asociación del album con el usuario se realizó correctamente
    print(Usuario.query.all()[0].albums) # Debería mostrar en consola al album asociado al usuario de prueba

    # Para verificar la compisición del album con su usuario
    db.session.delete(prueba_usuario) # Elimina al usuario de prueba de la base de datos
    print(Usuario.query.all()) # Se hace la consulta a los usuarios, no debería mostrar nada
    print(Album.query.all()) # Se hace la consulta a los albumes, como se eliminó al usuario, no debería mostrar nada

    # ------------------------------------------------------

    # Para probar la serialización de la clase Album
    album_schema = AlbumSchema() # Hace la traducción de los objetos de la db a dict con json
    
    # Se crea de nuevo un objeto de la clase Album para la prueba
    prueba_album = Album(titulo='Album de prueba', anio=1998, descripcion='Descripcion de prueba', medio=Medio.CD) # Objeto de la clase Album, objeto de prueba

    # Guardar el objeto de prueba en la base de datos
    db.session.add(prueba_album) # Se añade a la base de datos
    db.session.commit() # Se hace commit a la db, con eso se guarda el objeto de prueba

    # Ahora si, se prueba la traducción del objeto a json
    print([album_schema.dumps(album) for album in Album.query.all()]) # Se regresa una lista de la traducción en dict de todos los objetos en Album