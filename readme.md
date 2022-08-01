# NVDA development utilities.

See the
[spanish version here](/spanishReadme.md)

This repo will contain all the utilities I've written or found in any place, to help with the development of NVDA's add-ons.

## config helper.
[Get the utility here](https://raw.githubusercontent.com/davidacm/NVDADevelopmentUtilities/master/src/_configHelper.py)

This is a small utility to deal with NVDA's settings in our add-ons.

The philosophy here is that strings related to coding should only be written in a centralized place.
Because IDE's usually can't help you to autocomplete inside a string, then you can make mistakes if you change just a letter. Remember that, for example a string as a key in a dict, is case sensitive.


I really hate to write config.conf.['a1']['a2]['option'] each time I
need to access, or set a value in the configuration.

### usage.

This consist on a class for the specification and a very simple descriptor, to get and
access the config values.

See an example here:

```
# first, import the utility.
from ._configHelper import *

# and then, let's do the class with the spec.
# this class must inherit from the BaseConfig class.
class AppConfig(BaseConfig):
	# set the path to save the add-on settings.
	path  = 'beepKeyboard'
	# you can set it in the constructor also, or setting a second parameter when calling registerConfig(AppConfig, "path")

	# now, define your config properties / attributes / options.
	# optConfig is a descriptor class and it will do all the magic behind.
	# OptConfig will take the name you declared here and will use it for the name of the config option.
	# you just need to specify the description of the data.
	# you can set a distinct name for the option if you want, but it isn't usually needed.
	# if you need this anyway, just call OptConfig so:
	# OptConfig("optionName", "data description")
	# let'st start with the config deffinition.
	beepUpperWithCapsLock = OptConfig('boolean(default=True)')
	beepCharacterWithShift = OptConfig('boolean(default=False)')
	beepToggleKeyChanges = OptConfig('boolean(default=False)')
	announceToggleStatus = OptConfig('boolean(default=True)')
	disableBeepingOnPasswordFields = OptConfig('boolean(default=True)')
	ignoredCharactersForShift = OptConfig("string(default='\\x1b\\t\\b\\r ')")
	beepForCharacters = OptConfig("string(default='')")
	shiftedCharactersTone = OptConfig('int_list(default=list(6000,10,25))')
	customCharactersTone = OptConfig('int_list(default=list(6000,10,25))')
	capsLockUpperTone = OptConfig('int_list(default=list(3000,40,50))')
	toggleOffTone = OptConfig('int_list(default=list(500,40,50))')
	toggleOnTone = OptConfig('int_list(default=list(2000, 40, 50))')

# now, we need to register the config specification and get an instance of the class to be used in our code.
AF = registerConfig(AppConfig)

# accessing an option:
print("this should print False", af.disableBeepingOnPasswordFields)
# changing the value:
af.disableBeepingOnPasswordFields  = True
# let's see the new value.
print("this should print True", af.disableBeepingOnPasswordFields)
```

## typeString.
[Get the function code here](https://raw.githubusercontent.com/davidacm/NVDADevelopmentUtilities/master/src/typeString.py)
this is a small piece of code to help you to write a string in a text input. Sometimes add-on developers copy a text in the clipboard, and then paste it. But in my opinion, that is not a good idea because it interferes with the clipboard of the user.

I developed this function a long time ago. Currently I'm not using it, this might have some bugs. Use it, and if you encounter an issue and you can fix it, please let me know the solution.

### usage

Just call the function with the string that you need to type. For example:

typeString("Hello, this is a test")


## Notes:

I usually work inside a folder called "nvda/addons", and each add-on is inside that folder.
Inside nvda folder, I have a clone of the source code of nvda, it would be "nvda/nvda".

I mentioning it because so, you can understand the paths pre-configured in the ".code-workspace" file for vs code.
