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

Para acceder a la especificación de configuración, accede a la propiedad de la clase que declaraste. La instancia accederá únicamente al valor actual de la configuración.

Normalmente la especificación la escribirás en un string. Pero si tu configuración se comporta de forma un poco distinta a lo usual, puedes usar una tupla de valores para modificar el comportamiento de las configuraciones.
Estos son los valores soportados actualmente si usas tuplas:

1. String con la especificación de la opción.
2. True para indicar que la configuración se debe generalizar, o false para indicar que debe ser específica para cada perfil de NVDA. Por defecto es false.
3. (parámetro opcional) Una función de validación de tipos. Ya que NVDA no comprueba ni convierte tipos al acceder directamente al perfil general, puedes especificar una función para que valide de manera automática el valor de la opción. Esto tiene sentido únicamente si estableciste el segundo parámetro en True.

### ejemplo de código:

Este ejemplo fue tomado del complemento [Beep Keyboard.](https://github.com/davidacm/beepKeyboard)

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

Beamos un ejemplo con configuraciones de perfil general. El ejemplo fue tomado del complemento [IBMTTS.](https://github.com/davidacm/NVDA-IBMTTS-Driver)

```
from ._configHelper import configSpec, registerConfig, boolValidator
@configSpec("ibmeci")
class _AppConfig:
	dllName = ("string(default='eci.dll')", True)
	TTSPath = ("string(default='ibmtts')", True)
	# opcion de perfil general con validador (bool)
	autoUpdate  = ('boolean(default=True)', True, boolValidator)
appConfig = registerConfig(_AppConfig)
```

### Casos reales de uso:

* [beepKeyboard](https://github.com/davidacm/beepkeyboard)
* [SpeechHistoryExplorer](https://github.com/davidacm/SpeechHistoryExplorer)
* [IBMTTS](https://github.com/davidacm/NVDA-IBMTTS-Driver)
* [Wake Speaker](https://github.com/davidacm/WakeSpeaker)

## typeString.
[Encuentra el código de la función aquí](https://raw.githubusercontent.com/davidacm/NVDADevelopmentUtilities/master/src/typeString.py)

Este es un pequeño fragmento de código para ayudarte a escribir una cadena en una entrada de texto. A veces los desarrolladores de complementos copian un texto en el portapapeles, y luego lo pegan. Pero en mi opinión, eso no es una buena idea porque interfiere con el portapapeles del usuario.

Desarrollé esta función hace mucho tiempo. Actualmente no la estoy usando, esto podría tener algunos errores. Úsalo, y si encuentras un problema y puedes arreglarlo, por favor hazme saber la solución.

### Uso

Simplemente llama a la función con la cadena que necesitas escribir. Por ejemplo

typeString("Hola, esto es una prueba")

## "updateVersion.py". Utilidad para actualizar la versión de buildVars.py

Este pequeño script no requiere módulos externos. Simplemente es un archivo python al que le debes pasar la versión a la cual deseas actualizar el archivo buildVars, utilizado por scons para empaquetar los complementos de NVDA.

Por ejemplo:

"python updateVersion.py 2023.5.2"

Si el script reconoce un argumento pasado al script, lo identificará como la versión que deseas asignar.

## "post-commit". Hook para actualizar la versión si olvidaste hacerlo.

Esta idea nació porque siempre olvido actualizar buildVars.py, actualizar la versión de un add-on requiere actualizar lo mismo en muchas partes y no se me dan bien las tareas repetitivas.
Solía actualizar la versión en un github workflow que utilizo para publicar releases automáticamente, pero no me gusta la idea de tener un buildVars desinscronizado con la última versión.

Entonces, si no quieres complicarte con todo eso, deja que un hook lo haga por ti.
Para poder hacerlo, se requiere del uso del script "updateVersion.py".

### Funcionamiento:

1. Pon el archivo "post-commit" dentro de la carpeta .git/hooks.
2. Si vas a liberar una nueva versión, escribe en la primera línea del commit la versión de esta forma: "version 1.2.3". La versión debe estar compuesta por tres números, dado que es requisito para la tienda de complementos de NVDA.
3. En el post commit, el hook analizará si tu commit posee en la primera línea un mensaje del tipo "version x.y.z". Si lo encuentra, verificará que "buildVars.py" coincida con la versión especificada.
4. En caso de no coincidir, actualizará la versión usando updateVersion.py, agregará el archivo modificado al índice, y hará un commit --amend.
5. Creará un tag con la versión especificada.

El hook mostrará un mensaje por consola indicando que ha reconocido una indicación de versión, y el script de python también. Puedes revisar los mensajes de la consola si deseas estar seguro que todo ha ido bien.

Si usas un github workflow para lanzar releases al subir un tag, solo te toca introducir "git push origin x.y.z".
Si bien podrías agregar este último comando al hook, no lo considero buena idea. Pero puedes añadirlo tu si lo deseas. tal vez algún día lo haga.

## Notas:

Normalmente trabajo dentro de una carpeta llamada "nvda/addons", y cada complemento está dentro de esa carpeta.
Dentro de la carpeta nvda, tengo un clon del código fuente de nvda, sería "nvda/nvda".

Lo menciono porque así podrás entender las rutas preconfiguradas en el archivo ".code-workspace" para usar con VS Code.
