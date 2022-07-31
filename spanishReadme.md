# Utilidades de desarrollo de NVDA.
Este repo contendrá todas las utilidades que he escrito o encontrado en cualquier lugar, para ayudar al desarrollo de los complementos de NVDA.

## config helper.
[Encuentra la utilidad aquí](https://raw.githubusercontent.com/davidacm/NVDADevelopmentUtilities/master/src/_configHelper.py)

Esta es una pequeña utilidad para manejar la configuración de NVDA en nuestros complementos.

La filosofía aquí es que las cadenas relacionadas con la codificación sólo deben ser escritas en un lugar centralizado.
Debido a que los IDE's usualmente no pueden ayudarte a autocompletar dentro de una cadena, entonces puedes cometer errores si cambias sólo una letra. Recuerda que, por ejemplo, una cadena como clave en un diccionario, es sensible a las mayúsculas y minúsculas.

Realmente odio escribir config.conf.['a1']['a2]['option'] cada vez que
necesito acceder, o establecer un valor en la configuración.

### Uso.

Esto consiste en una clase para la especificación y un descriptor muy simple, para obtener y
acceder a los valores de la configuración.

Vea un ejemplo aquí:

```
# primero, importa la utilidad.
from ._configHelper import *

# y luego, hagamos la clase con la especificación.
# esta clase debe heredar de la clase BaseConfig.
class AppConfig(BaseConfig):
	def __init__(self):
		# indica el path de tu configuración al constructor del superclass.
		super().__init__('beepKeyboard')

	# ahora, define tus propiedades / atributos / opciones de configuración.
	# optConfig es una clase descriptiva y es la que hará toda la magia detrás.
	# OptConfig tomará el nombre que declaraste aquí y lo usará para el nombre de la opción de configuración.
	# solo necesitas especificar la descripción de los datos.
	# puedes establecer un nombre distinto para la opción si quieres, pero normalmente no es necesario.
	# si usted necesita esto de todos modos, sólo llame a OptConfig así:
	# OptConfig("NombreDeOpcion", "descripcion de datos")
	# Hagamos la definición de la configuración. ¡Mira que fácil!
	beepUpperWithCapsLock = OptConfig('boolean(default=True)')
	beepCharacterWithShift = OptConfig('boolean(default=False)')
	beepToggleKeyChanges = OptConfig('boolean(default=False)')
	announceToggleStatus = OptConfig('boolean(default=True)')
	disableBeepingOnPasswordFields = OptConfig('boolean(default=True)')
	ignoredCharactersForShift = OptConfig("string(default='\x1b\t\b\\r ')")
	beepForCharacters = OptConfig("string(default='')")
	shiftedCharactersTone = OptConfig('int_list(default=list(6000,10,25))')
	customCharactersTone = OptConfig('int_list(default=list(6000,10,25))')
	capsLockUpperTone = OptConfig('int_list(default=list(3000,40,50))')
	toggleOffTone = OptConfig('int_list(default=list(500,40,50))')
	toggleOnTone = OptConfig('int_list(default=list(2000, 40, 50))')

# ahora, necesitamos registrar la especificación de la configuración y obtener una instancia de la clase para ser utilizada en nuestro código.
AF = registerConfig(AppConfig)

# Como acceder al valor de una opción:
print("Esto debería iprimir False", af.disableBeepingOnPasswordFields)
# cambiando el valor a True:
af.disableBeepingOnPasswordFields = True
# veamos el nuevo valor
print("Esto debería iprimir True", af.disableBeepingOnPasswordFields)
```

## typeString.
[Encuentra el código de la función aquí](https://raw.githubusercontent.com/davidacm/NVDADevelopmentUtilities/master/src/typeString.py)
este es un pequeño fragmento de código para ayudarte a escribir una cadena en una entrada de texto. A veces los desarrolladores de complementos copian un texto en el portapapeles, y luego lo pegan. Pero en mi opinión, eso no es una buena idea porque interfiere con el portapapeles del usuario.

Desarrollé esta función hace mucho tiempo. Actualmente no la estoy usando, esto podría tener algunos errores. Úsalo, y si encuentras un problema y puedes arreglarlo, por favor hazme saber la solución.

### Uso

Simplemente llama a la función con la cadena que necesitas escribir. Por ejemplo

typeString("Hola, esto es una prueba")


## Notas:

Normalmente trabajo dentro de una carpeta llamada "nvda/addons", y cada complemento está dentro de esa carpeta.
Dentro de la carpeta nvda, tengo un clon del código fuente de nvda, sería "nvda/nvda".

Lo menciono porque así podrás entender las rutas preconfiguradas en el archivo ".code-workspace" para usar con VS Code.
