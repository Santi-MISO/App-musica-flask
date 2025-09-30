# Para importar Resource, con los que se crean los recursos
from flask_restful import Resource

# Para importar los modelos que se usaran en las resource
from ..models import db, Cancion, CancionSchema, Album, AlbumSchema, Usuario, UsuarioSchema, Medio

# Para importar request, lo que va a permitir usar los request
from flask import request


### Para la vista de las canciones

# Se instancia el esquema de Cancion
cancion_schema = CancionSchema()

# Se crea la clase con la vista de las canciones
class VistaCanciones(Resource): # Hereda de un recurso
    def get(self): # Metodo para conseguir toda la lista de canciones
        return [cancion_schema.dump(cancion) for cancion in Cancion.query.all()] # Regresa una lista con todas las canciones en la db, como se usó .dump() se va a obtener un dict de python
    
    def post(self): # Se define POST como método de la clase de la vista de las canciones, crea una nueva canción
        nueva_cancion = Cancion(titulo=request.json['titulo'], \
                                minutos=request.json['minutos'], \
                                segundos=request.json['segundos'], \
                                interprete=request.json['interprete']) # Se recibe la cancion con todos sus atributos por medio de request desde json, NO se usa get porque se espera un diccionario con todos los atributos, son obligatorios
        db.session.add(nueva_cancion) # Se agrega la canción a la db
        db.session.commit() # Se guardan los cambios en la db
        return cancion_schema.dump(nueva_cancion)

# Para el metodo de editar cancion y borrar cancion es necesario crear otra vista
class VistaCancion(Resource): # Hereda de Resource, clase asociada a una sola cancion, el recurso se crea para editar y borrar
    def get(self, id_cancion): # Metodo para regresar una cancion asociada a un id 
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion)) # Regresa la información de la canción asociada al id, se usa get_or_404 en caso de que ese id no exista en la db

    def put(sel, id_cancion): # Metodo para editar una cancion en especifico
        cancion = Cancion.query.get_or_404(id_cancion) # Se consigue el objeto Cancion que se va a editar
        cancion.titulo = request.json.get('titulo', cancion.titulo) # Como json entrega diccionario, esto busca una clave, se usa get porque el atributo es opcional, se usa cancion.titulo como campo por defecto en caso de que la entrada no se ingrese
        cancion.minutos = request.json.get('minutos', cancion.minutos) # Se hace el request opcional para minutos
        cancion.segundos = request.json.get('segundos', cancion.segundos) # Se hace el request opcional para segundos
        cancion.interprete = request.json.get('interprete', cancion.interprete) # Se hace el request opcional para interprete
        db.session.commit() # Se guardan los cambios en la db
        return cancion_schema.dump(cancion) # Regresa la canción actualizada

    def delete(self, id_cancion): # Metodo para borrar una cancion en especifico
        cancion = Cancion.query.get_or_404(id_cancion) # Se consigue el objeto Cancion que se va a borrar
        db.session.delete(cancion) # Se borra al objeto cancion de la db
        db.session.commit() # Se guardan los cambios en la db
        return 'Cancion eliminada con exito', 204 # Confirmación de la operación, el codigo 204 indica que el recurso ya no existe, para evitar solicitudes por parte del usuario sobre este
    

### Para la vista de los albumes

# Instancia del esquema de Album
album_schema = AlbumSchema()

# Se crea la clase de la vista de los albumes para los metodos get (lista) y post
class VistaAlbumes(Resource): # Como es un recurso hereda de Resource
    def get(self): # Metodo get (lista albumes)
        return [album_schema.dump(album) for album in Album.query.all()] # Regresa una lista con todos los albumes en la db
    
    def post(self): # Metodo post (crear album)
        nuevo_album = Album(titulo=request.json['titulo'], \
                            anio=request.json['anio'], \
                            descripcion=request.json['descripcion'], \
                            medio=Medio[request.json['medio']]) # Se crea el objeto clase Album, el mapeo del medio se recibe como string, como 'CD'. Si se quiere recibir el valor numerico, como 1, 2 o 3 el medio se recibe con Medio(request.json['medio'])
        db.session.add(nuevo_album) # Se agrega el nuevo objeto album a la db
        db.session.commit() # Se guardan los cambios a la db
        return album_schema.dump(nuevo_album) # Se regresa el nuevo album creado
    
# Se cre la clase de la vista de un album en especifico, para los metodos get (especifico), put y delete
class VistaAlbum(Resource): # Como es un recurso hereda de Resource
    def get(self, id_album): # Metodo get (un album en especifico)
        album = Album.query.get_or_404(id_album) # Se consulta a la db por el album en especifico con id id_album
        return album_schema.dump(album) # Se regresa el album, se podría ahorrar una línea de codigo haciendo directamente la consulta en este return
    
    def put(self, id_album): # Metodo put (editar album)
        album = Album.query.get_or_404(id_album) # Se consulta la db por el album en especifico con id id_album
        album.titulo = request.json.get('titulo', album.titulo) # Se mapea el nuevo titulo del album y se reemplaza por el titulo del album, si no se ingresa ninguno, se deja el titulo que ya tenía
        album.anio = request.json.get('anio', album.anio) # Se mapea el nuevo año del album y se reemplaza en el album, si no se ingresa ninguno se deja el año que ya tenía
        album.descripcion = request.json.get('descripcion', album.descripcion) # Se mapea la nueva descripcion del album y se reemplaza en el album, si no se ingresa ninguna se deja la descripcion que ya tenía
        # ADVERTENCIA, el mapeo del medio solo se hace así si el front es confiable, en caso contrario es necesario un try/except
        album.medio = Medio[request.json.get('medio', album.medio.name)] # Se mapea el nuevo medio, como es un enum y se recibe el str con el nombre de la enum se recibe como en el paso 9 de las indicaciones
        db.session.commit() # Se guardan los cambios en la db
        return album_schema.dump(album) # Se regresa el album con los cambios realizados
    
    def delete(self, id_album): # Metodo delete (borrar album)
        album = Album.query.get_or_404(id_album) # Se consulta la db por el album en especifico con id id_album
        db.session.delete(album) # Se borra el album de la db
        db.session.commit() # Se guardan los cambios en la db
        return 'Album borrado con exito', 204 # Se notifica que la operación se realizó correctamente, el codigo 204 indica que el recurso ya no existe, para evitar que el usuario evite regresar a este
    
### Para las vistas de los usuarios

# Se instancia el esquema de la clase Usuario

usuario_schema = UsuarioSchema()

# Se crea la clase VistaUsuarios para los metodos get (lista) y post
class VistaUsuarios(Resource): # Como es un recurso, hereda de Resource
    def get(self): # Metodo get (lista usuarios)
        return [usuario_schema.dump(usuario) for usuario in Usuario.query.all()] # Regresa una lista con todos los usuarios consultados en la db en formato dict
    
    def post(self): # Metodo post (crear usuario)
        nuevo_usuario = Usuario(nombre_usuario=request.json['nombre_usuario'], \
                                contrasena=request.json['contrasena']) # Se crea un nuevo usuario según lo mapeado
        db.session.add(nuevo_usuario) # Se añade el nuevo usuario a la db
        db.session.commit() # Se guardan los cambios en la db
        return usuario_schema.dump(nuevo_usuario) # Se regresa el usuario creado con todos sus pares clave-valor
    
# Se crea la clase VistaUsuario para los metodos get (especifico), put y delete
class VistaUsuario(Resource): # Como es un recurso, hereda de Resource
    def get(self, id_usuario): # Metodo get (usuario especifico)
        return usuario_schema.dump(Usuario.query.get_or_404(id_usuario)) # Se regresa el usuario en especifico con id id_usuario
    
    def put(self, id_usuario): # Metodo put (editar usuario)
        usuario = Usuario.query.get_or_404(id_usuario) # Se consulta la db por el usuario en especifico que se va a editar
        usuario.nombre_usuario = request.json.get('nombre_usuario', usuario.nombre_usuario) # Se mapea el cambio al nuevo nombre, en caso de no ingresar un valor, se mantiene el nombre que ya tiene el usuario
        usuario.contrasena = request.json.get('contrasena', usuario.contrasena) # Se mapea la nueva contraseña del usuario, en caso de no ingresar ningun valor, se conserva la contraseña que ya tenía el usuario
        db.session.add(usuario) # Se añaden los cambios del usuario a la db
        db.session.commit() # Se guardan los cambios en la db
        return usuario_schema.dump(usuario) # Se regresa el usuario con los cambios realizados
    
    def delete(self, id_usuario): # Metodo delete (borrar usuario)
        usuario = Usuario.query.get_or_404(id_usuario) # Se consulta la db por el usuario en especifico con id id_usuario
        db.session.delete(usuario) # Se borra al usuario en especifico de la db
        db.session.commit() # Se guardan los cambios en la db
        return 'Usuario borrado exitosamente' # Se notifica al usuario que la operación se realizó con exito