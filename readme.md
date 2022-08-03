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
access the config values. Don't worry, you don't need to use the descriptor directly, the class decorator will do all the stuff for you.

There are many ways to use it, but the simplest way is by using the class decorator.

Note: when returnValue is set to false, get the value of a property will return the config description.

This is default False, but when you call the register function, it will set this value to True.
So, you won't need to worry about this.

See an example here:

```
# first, import the utility. The decorator and the register config function.

from ._configHelper import configSpec, registerConfig

# now the class definition, with the decorator first.
# this decorator will replace the attributes with a descriptor to manage accessing and updating values.
@configSpec
class AppConfig:
	# the config path. Important to call it __path__ = ...
	__path__ = 'beepKeyboard'
	# now the definition of the settings. in form of name = 'desc'
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
AF = registerConfig(AppConfig)

# accessing an option:
print("this should print False", AF.disableBeepingOnPasswordFields)
# changing the value:
AF.disableBeepingOnPasswordFields  = True
# let's see the new value.
print("this should print True", AF.disableBeepingOnPasswordFields)
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
