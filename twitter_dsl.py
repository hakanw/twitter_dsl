#!/usr/bin/env python
# encoding: utf-8

# a simple twitter DSL proof of concept
# by Håkan Waara (hwaara@gmail.com) 2010

import re
import sys
import twitter

# builtin utils
from random import randint
# add more ...
code = sys.stdin.read()
# @foo -> _usr("foo")
code = re.sub(r'\@(\w+)', r'_usr("\1")', code)
# #foo -> _tag("foo")
code = re.sub(r'#(\w+)', r'_tag("\1")', code)
# @(foo) -> _usr(foo)
code = re.sub(r"@(\([^\)]+\))", r'_usr(\1)', code)
# #(foo) -> _tag(foo)
code = re.sub(r"#(\([^\)]+\))", r'_tag(\1)', code)
# _N -> _args[N-1]
code = re.sub(r"_(\d+)", r'_args[\1-1]', code)

_args = []

api = twitter.Api()

def _usr(username):
	global api
	class TwitterUser:
		def __init__(self):
			self.user = api.GetUser(username)
		
		def __getitem__(self, key):
			return api.GetUserTimeline(username)[key].GetText()
		
		def __len__(self):
			return self.user.GetStatusesCount()
	
	return TwitterUser()
	
def _tag(name):
	# TODO using a twitter library that supports the search API
	pass

print code	
result = compile(code, '', 'exec')

# TODO: pass safe environment instead of passing along everything
eval(result)
