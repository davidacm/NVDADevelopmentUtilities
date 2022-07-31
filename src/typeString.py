# TypeString.
# Copyright (C) 2022 David CM
# this is a small piece of code to help you to write a string in a text input.

import brailleInput, threading, winUser

modifiers = [
	winUser.VK_LCONTROL,
	winUser.VK_RCONTROL,
	winUser.VK_LSHIFT,
	winUser.VK_RSHIFT,
	winUser.VK_LMENU,
	winUser.VK_RMENU,
	winUser.VK_LWIN,
	winUser.VK_RWIN
]

def typeString(s):
	""" this function types the specified string acting like an user typing.
	params:
	@s: the string to type.
	"""
	# first, release all modifiers to avoid issues when typing.
	for k in modifiers:
		if winUser.getKeyState(k) & 32768:
				winUser.keybd_event(k, 0, 2, 0)
	# now type the string. I used a timer, I didn't remember why.
	# but I'm sure that it was to solve an issue.
	threading.Timer(0.01, brailleInput.handler.sendChars, [s]).start()
