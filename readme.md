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

To access the configuration spec, access the property of the declared class. The instance will only access the current value of the setting and not the spec.

Usually the specification can be written in a string. But if your configuration behaves a little differently than usual, you can use a tuple of values to change the behavior of the configurations.
These are the currently supported values when you use tuples:

1. String specifying the option.
2. True to indicate that the settings should be generalized for all profiles, or false to indicate that they should be specific to each NVDA profile. Default is false.
3. (optional parameter) A type validation function. Since NVDA does not check or convert types when accessing the general profile directly, you can specify a function to automatically validate the option's value. This only makes sense if you set the second parameter to True.

### Code example.

This example was taken from the [Beep Keyboard](https://github.com/davidacm/beepKeyboard) add-on.

```
# first, import the utility. The decorator and the register config function.

from ._configHelper import configSpec, registerConfig

# now the class definition, with the decorator first.
# this decorator will replace the attributes with a descriptor to manage accessing and updating values.
# you can specify the path config in the decorator or in the class. I prefer it in the decorator.
# if you prefer to set it in the class, just add an attribute called __path__ inside the class, e.g.
# __path__ = "..."
# the path given in the decorator has a higher priority.

@configSpec('beepKeyboard')
class AppConfig:
	# the definition of the settings. in form of name = 'desc'
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

Let's see an example with options for the general profile only. This was taken from [IBMTTS](https://github.com/davidacm/NVDA-IBMTTS-Driver) add-on.

```
from ._configHelper import configSpec, registerConfig, boolValidator
@configSpec("ibmeci")
class _AppConfig:
	dllName = ("string(default='eci.dll')", True)
	TTSPath = ("string(default='ibmtts')", True)
	# General profile option with a validator function for bools.
	autoUpdate  = ('boolean(default=True)', True, boolValidator)
appConfig = registerConfig(_AppConfig)
```

### Real use cases:

* [beepKeyboard](https://github.com/davidacm/beepkeyboard)
* [SpeechHistoryExplorer](https://github.com/davidacm/SpeechHistoryExplorer)
* [IBMTTS](https://github.com/davidacm/NVDA-IBMTTS-Driver)
* [Wake Speaker](https://github.com/davidacm/WakeSpeaker)

## typeString.
[Get the function code here](https://raw.githubusercontent.com/davidacm/NVDADevelopmentUtilities/master/src/typeString.py)

This is a small piece of code to help you to write a string in a text input. Sometimes add-on developers copy a text in the clipboard, and then paste it. But in my opinion, that is not a good idea because it interferes with the clipboard of the user.

I developed this function a long time ago. Currently I'm not using it, this might have some bugs. Use it, and if you encounter an issue and you can fix it, please let me know the solution.

### usage

Just call the function with the string that you need to type. For example:

typeString("Hello, this is a test")

## "updateVersion.py". Utility to update the version of buildVars.py

This little script does not require any external modules. It's just a python file to update the version of the add-on in the "buildVars.py". Just pass the desired version, for example:
"python updateVersion.py 2023.5.2"

If the script recognizes an argument passed to the script, it will identify that as the version you want to assign.

## "post-commit". Hook to update the version if you forgot to do it.

This idea came about because I always forget to update buildVars.py.. Updating the version of an add-on requires updating the same thing in several parts and I'm not good at repetitive tasks.
I used to update the version in a github workflow that I use to automatically launch new releases, but I don't like the idea of ​​having buildVars out of sync with the latest version.

So if you don't want to mess with all that, let a hook do it for you.
In order to do so, the use of the "updateVersion.py" script is required.

### Usage.
1. Put the file "post-commit" inside .git/hooks folder.
2. If you are going to release a new version, write in the first line of the commit the version in this way: "version 1.2.3". The version must consist of three numbers, as it is a requirement for the NVDA Add-on Store.
3. In the post commit stage, the hook will analyze if your commit has a message of the type "version x.y.z" in the first line. If it finds it, it will check that "buildVars.py" matches the specified version.
3. If they don't match, it will update the version using updateVersion.py, add the modified file to the index, and do a commit --amend.
4. It will create a tag with the specified version.

The hook will display a console message to announce that it has recognized a version indication, and the python script will too. You can check the console messages if you want to make sure that everything went well.

If you use a github workflow to push releases by uploading a tag, all you have to do is enter "git push origin x.y.z".
While you could add this last command to the hook, I don't think it's a good idea. But you can add it if you want. maybe one day I will.

## Notes:

I usually work inside a folder called "nvda/addons", and each add-on is inside that folder.
Inside nvda folder, I have a clone of the source code of nvda, it would be "nvda/nvda".

I mentioning it because so, you can understand the paths pre-configured in the ".code-workspace" file for vs code.

See this information in [spanish here](https://github.com/davidacm/NVDADevelopmentUtilities/blob/main/spanishReadme.md)
