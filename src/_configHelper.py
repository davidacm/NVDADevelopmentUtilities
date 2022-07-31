# NVDA configHelper.
# Copyright (C) 2022 David CM

""" this helps you to build the configurations for your add-ons easily, using class attributes, and python descriptors.
by this way, your ide or text editor will be enabled to know the information about your config spec, and since the spec is just in one place, you will never do a mistake.
Say goodbye those tedious config.conf['cat']['subcat']['option'] each time you need to access some config in your add-on.
this does not support subcategories, if you need that, you can build a new class. It can be improved a lot, and I will do it when I need a better feature.
"""

import config

def getConfigValue(path, optName):
	""" this function helps to accessing config values.
	params
	@path: the path to the option.
	@optName: the option name
	"""
	ops = config.conf[path[0]]
	for k in path[1:]:
		ops = ops[k]
	return ops[optName]


def setConfigValue(path, optName, value):
	""" this function helps to accessing and set config values.
	params
	@path: the path to the option.
	@optName: the option name
	@value: the value to set.
	"""
	ops = config.conf[path[0]]
	for k in path[1:]:
		ops = ops[k]
	ops[optName] = value


def registerConfig(clsSpec):
	""" this function registers your spec in the NVDA's config. It will instantiate the spec class, register it, and return the instance to you ready to be used.
	@params:
	clsSpec: the class with the config spec to be registered.
	@return: the instance ready to be used to accessing and changing values in the configuration of your add-on.
	"""
	AF = clsSpec()
	config.conf.spec[AF.path[0]] = AF.createSpec()
	AF.returnValue = True
	return AF


class OptConfig:
	""" just a helper descriptor to create the main class to accesing config values.
	the option name will be taken from the declared variable. if you need to set another name, set it in the first param.
	"""
	def __init__(self, a, b = None):
		"""
		params:
		@a: usually the spec description. But if b is not none, a will be the name of the option.
		@b: the config description when is not None.
		"""
		if b:
			self.name = a
			self.desc = b
		else:
			self.desc = a
			self.name = None

	def __set_name__(self, owner, name):
		if not self.name:
			self.name = name
		owner._confOpts.append(name)

	def __get__(self, obj, type=None):
		if obj.returnValue:
			return getConfigValue(obj.path, self.name)
		return self.name, self.desc

	def __set__(self, obj, value):
		setConfigValue(obj.path, self.name, value)


class BaseConfig:
	""" this class will help to get and set config values.
	the idea behind this is to generalize the config path and config names.
	sometimes, a mistake in the dict to access the values can produce an undetectable bug.
	if returnValue attribute is set to False, this will return the option name instead of the value.
	by default this value is False, to help to create the configuration spec first.
	Set it to true after creating this spec.
	"""

	def __init__(self, path):
		self.returnValue = False
		if isinstance(path, list):
			self.path = path
		else:
			self.path = [path]

	def createSpec(self):
		""" this method creates a config spec with the provided attributes in the class
		"""
		s = {}
		for k in self.__class__._confOpts:
			k = self.__getattribute__(k)
			s[k[0]] = k[1]
		return s
	# an array of the available options.
	_confOpts = []
