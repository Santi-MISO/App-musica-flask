# Se importa el módulo que se va a usar para crear los modelos
from flask_sqlalchemy import SQLAlchemy

# Se importa enum para la enumeración
import enum

# Se importa la libreria para crear las clases autoschema, que heredan de sqlaclhemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# Se importa fields de marshmallow para serializar las enumeraciones
from marshmallow import fields

# Instancia de la base de datos
db = SQLAlchemy()

### Se declaran las clases

# Para la relación de Album con Cancion es necesario hacer una tabla intermediaria.
# Esto se hace porque la relación de Album con Cancion es muchos a muchos
album_cancion = db.Table(
    "album_cancion", # Lo que relaciona la tabla
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True), # Apunta al id de los albumes, que son un entero, como llave foranea y llave primaria
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key=True) # Apunta al id de las canciones, que son un entero, como llave foranea y llave primaria
)

# Para implementar la clase Usuario, las clases heredan de un modelo SQLAlchemy, de db.Model
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(128)) # Máximo 128 caracteres para el nombre del usuario
    contrasena = db.Column(db.String(128)) # Máximo 128 caracteres para la contraseña del usuario

    # Para la relación de composición de Usuario y Album, de uno a muchos. 
    albums = db.relationship(
        'Album', # La relación es con la clase Album
        back_populates='usuario', # Asegura la relación con el atributo usuario de la clase Album, esto NO estuvo en la guía
        cascade='all, delete, delete-orphan' # Elimina a los albumes si se elimina el usuario porque la relaciónn es composición
    )

    def save(): # Implementación suplementaria de save()
        check_safe = True
        return check_safe
    
    def delete(): # Implementación suplementaria de delete()
        check_delete = True
        return check_delete

# La clase canción hereda de un modelo de SQLAlchemy, de db.Model
class Cancion(db.Model):
    # Para los atributos de la clase Cancion se toma en cuenta el diagrama de clases de la wiki del repositorio
    # Para cada atributo se asigna el tipo de variable que le corresponde
    # El atributo id es la llave primaria de la clase Cancion
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128)) # Para las cadenas de caracteres hay que indicar la magnitud máxima, en este caso, 128
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    interprete = db.Column(db.String(128)) # Magnitud máxima de 128

    # Para la relación muchos a muchos de Cancion con Album
    albums = db.relationship(
        'Album', # La relación es con la clase Album
        secondary=album_cancion, # Usa la tabla intermediaria para la relación
        back_populates='canciones' # Asegura la relación con el atributo canciones de la clase Album
        ) 

    # Para la prueba se usa y redefine __repr__() para ver los atributos de la clase en la aplicación. 
    # __repr__() es una función de la clase Cancion

    def __repr__(self):
        # Se espera recibir los atributos de la clase, para comprobar que todo esté funcionando bien
        return "{}-{}-{}-{}".format(self.titulo, self.minutos, self.segundos, self.interprete)
    
# Para implementar la clase de enumeración Medio
class Medio(enum.Enum):
    DISCO = 1
    CASETE = 2
    CD = 3

# Para implementar la clase Album, hereda de un modelo SQLAlchemy, de db.Model
class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(256)) # Máximo 256 caracteres para el nombre del album
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(256)) # Máximo 256 caracteres para la descripcion del album
    medio = db.Column(db.Enum(Medio)) # Se define la enumeración del medio con la clase Medio

    # Para la relación uno a muchos de composición de Usuario y Album, 
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id')) # Puntero de la relación entre Album con usuario, esto establece y permite en si la relación, ESTO ES OBLIGATORIO PARA LA RELACION
    
    __table_args__ = (db.UniqueConstraint('usuario_id', 'titulo', name='titulo_unico_album'),) # Pone la restricción al usuario de que no pueda tener más de un album con el mismo titulo, se llama a la columna de la relacion, usuario_id, no al usuario.id como tal ni al objeto usuario
    
    usuario = db.relationship( # Hace la relación a nivel de objetos, permite acceder al usuario del album, ES OPCIONAL
        'Usuario',  # La relación es con la clase Usuario
        back_populates='albums' # Asegura la relación con el atributo albums de Usuario y permite acceder al usuario del album, sin mas queries
    )

    # Para la relación muchos a muchos con Cancion
    canciones = db.relationship(
        'Cancion', # La relación es con la clase Cancion
        secondary=album_cancion, # Usa la tabla intermediaria para la relación
        back_populates='albums' # Asegura la relación con el atributo albums de Cancion y permite aceder a la cancion del album, sin mas queries
    )

    def save(): # Implementación suplementaria de save()
        check_safe = True
        return check_safe
    
    def delete(): # Implementación suplementaria de delete()
        check_delete = True
        return check_delete
    
### Se declaran las clases autoschema de las clases

# Estas declaraciones se hacen DESPUES de haber declarado las clases originales
# Esto se hace para serializar los objetos
# Serializar los objetos permite tratar con entidades json a partir de entidades de la db de sqlalchemy
# Así mismo, serializar permite tratar con entidades de la db sqlalchemy a partir de entidades json

# SERIALIZAR EN RESUMEN:
# Serializar permite tomar un objeto de la base de datos y convertirlo a un diccionario con pares atributo-valor
# Ej: 
# El objeto 
# Usuario(id=1, nombre_usuario='Santi', contrasena='abc123')
# Se convierte en
# {'id': 1, 'nombre_usuario':'Santi', 'contrasena':'abc123'}

# Beneficios de serializar:
# Aporta al desacoplamiento entre front y back, cuando el front recibe una versión json del objeto no está viendo la db
# Manejar un dict en json es mucho más sencillo

# Se crea una clase para indicarle a marshmallow cómo pasar enum a json
# Esto es el paso 2 de las indicaciones, como AlbumSchema va a necesitar esta clase, se declara antes, pero no es un paso previo necesariamente
class EnumADict(fields.Field): # Hereda de Field, que viene de fields, por eso se importó
    def  _serialize(self, value, attr, obj, **kwargs): # El metodo para serializar, todos los valores de entradas se ingresaron solos con autocompletar omg
        if value is None: # Esto se hace para evitar problemas serializando un None
            return None 
        return {'llave':value.name, 'valor':value.value} # Esto hay que corregirlo, el retorno por defecto del autocompletar es distinto

# Se implementa la clase autoschema de Album
class AlbumSchema(SQLAlchemyAutoSchema): # Hereda de SQLAlchemyAutoSchema
    medio = EnumADict(attribute=('medio')) # Esto se realiza para pasar enum a dict, hace parte del paso 2 de las indicaciones
    class Meta: # Meta clase que corresponde al esquema (schema)
        model = Album # El modelo que se está serializando
        include_relationships = True # Incluye todas las relaciones de la clase
        load_instance = True # Se carga la instancia de la clase cuando se accede al esquema (autoschema)

### Para la serialización de las otras clases

# Serialización de Usuario
class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True

# Serialización de Cancion
class CancionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cancion
        include_relationships = True
        load_instance = True