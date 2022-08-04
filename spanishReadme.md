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
acceder a los valores de configuración. No te preocupes, no necesitas usar el descriptor directamente, el decorador de clase hará todo el trabajo por ti.

Hay muchas maneras de usarlo, pero la más sencilla es usar el decorador de clase.

Nota: cuando returnValue se establece en false, obtener el valor de una propiedad devolverá la descripción de la configuración.

Esto está por defecto en False, pero cuando se llama a la función register, se establecerá este valor a True.
Por lo tanto, no tendrá que preocuparse por esto.

### ejemplo de código:

```
# Primero, importemos la utilidad. El decorador y la función para registrar la configuración.
from ._configHelper import configSpec, registerConfig

# Ahora, la declaración de la clase, con el decorador primero.
# este decorador remplazará los atributos con un descriptor para manejar el acceso y la actualización de los valores de la configuración.
# puedes definir la ruta de la configuración en el decorador o en la clase.
# yo la prefiero en el decorador. Si la quieres en la clase, debes definir un atributo dentro de la clase así:
# __path__ = "..."
# la ruta en el decorador tiene prioridad sobre la declarada dentro de la clase.

@configSpec('beepKeyboard')
class AppConfig:
	# la declaración de cada configuración. En forma de nombre = 'descripción'
	beepUpperWithCapsLock = 'boolean(default=True)'
	beepCharacterWithShift = 'boolean(default=False)'
	beepToggleKeyChanges = 'boolean(default=False)'
	announceToggleStatus = 'boolean(default=True)'
	disableBeepingOnPasswordFields = 'boolean(default=True)'
	ignoredCharactersForShift = "string(default='\\x1b\\t\\b\\r ')"
	beepForCharacters = "string(default='')"
	shiftedCharactersTone = 'int_list(default=list(6000,10,25))'
	customCharactersTone = 'int_list(default=list(6000,10,25))'
	capsLockUpperTone = 'int_list(default=list(3000,40,50))'
	toggleOffTone = 'int_list(default=list(500,40,50))'
	toggleOnTone = 'int_list(default=list(2000, 40, 50))'
# ahora registramos la descripción de la configuración que acabamos de hacer.
AF = registerConfig(AppConfig)

# accediendo al valor de una opción:
print("Esto debería imprimir False", AF.disableBeepingOnPasswordFields)
# Actualizando el valor:
AF.disableBeepingOnPasswordFields  = True
# Veamos el nuevo valor.
print("Esto debería imprimir True", AF.disableBeepingOnPasswordFields)
```

### Casos reales de uso:

* [beepKeyboard](https://github.com/davidacm/beepkeyboard)
* [SpeechHistoryExplorer](https://github.com/davidacm/SpeechHistoryExplorer)

## typeString.
[Encuentra el código de la función aquí](https://raw.githubusercontent.com/davidacm/NVDADevelopmentUtilities/master/src/typeString.py)

Este es un pequeño fragmento de código para ayudarte a escribir una cadena en una entrada de texto. A veces los desarrolladores de complementos copian un texto en el portapapeles, y luego lo pegan. Pero en mi opinión, eso no es una buena idea porque interfiere con el portapapeles del usuario.

Desarrollé esta función hace mucho tiempo. Actualmente no la estoy usando, esto podría tener algunos errores. Úsalo, y si encuentras un problema y puedes arreglarlo, por favor hazme saber la solución.

### Uso

Simplemente llama a la función con la cadena que necesitas escribir. Por ejemplo

typeString("Hola, esto es una prueba")


## Notas:

Normalmente trabajo dentro de una carpeta llamada "nvda/addons", y cada complemento está dentro de esa carpeta.
Dentro de la carpeta nvda, tengo un clon del código fuente de nvda, sería "nvda/nvda".

Lo menciono porque así podrás entender las rutas preconfiguradas en el archivo ".code-workspace" para usar con VS Code.
