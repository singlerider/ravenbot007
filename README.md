Try it out! Code is live at
http://www.twitch.tv/ravenhart007
===============================

# ravenbot007

This is a Twitch chat/irc bot written in Python (2.6 / 2.7).

## Installation

### Steps

Make a copy of the example config file:

`cp src/config/config_example.py src/config/config.py`

Make a copy of the example globals file:

`cp globals_example.py globals.py`


#### Globals and Config Files

Head into src/config/config.py and enter the correct channels and cron jobs
you'd like to run, then go into globals.py and at the very least replace the
mysql credentials. Leave global_channel, CURRENT_USER, VARIABLE, and
channel_info alone.

## Make It Do

### Adding your own commands

You're going to need to know basic Python if you want to add your own commands. Open up 'lib/command_headers.py'. There are examples of pre-made commands in there as examples. The limit parameter is the amount of times a command can be used in seconds, if you don't want a limit to be enforced put in 0.

If your command is only going to return a string, ex - '!hello' returns 'Welcome!', don't include the 'argc' parameter. Place the string you wish to be returned to the user in the 'return' parameter. For example, if you wanted to create a command such as this and limit it to being used ever 30 seconds, you would add in:

```python
'!hello': {
		'limit': 10,
		'return': 'Welcome!'
}
```

However, if your command has to have some logic implemented and if the command is just going to return whatever a function returns, set the 'return' parameter on the command to 'command', and set 'argc' to '0'. If your command is going to take arguments, ex '!hello <name>', set argc to '1' or however many arguments the command is going to take in.

Make a new file in 'lib/commands/' and give the filename 'command.py' where command is the command name. If your 'argc' was set to '0', don't include 'args' in the functions parameters, else set the only parameter to 'args'. Args will contain a list of whatever arguments were passed to the command.

This command will contain whatever logic needs to be carried out. You should validate the arguments in there. After you have the response that you want a user to see, just 'return' it.

Let's say we want to add a command which will take two arguments, we will call it '!random' and it will take a 'minimum' and 'maximum' argument. We will limit this command to be allowed to be called every 20 seconds.

Add the following to the 'commands' dictionary:

```python
'!random': {
		'limit': 20,
		'argc': 2,
		'return': 'command',
		'ul': 'mod',
		'space_case': True
}
```

'limit' refers to the cooldown. The cooldown is only active per separate channel
'argc' refers to the number of arguments a command accepts, separated by spaces. If the command does not have 'command' as its 'return' value, this is not necessary. However, even if there are no arguments and 'command' is listed, 0 should be used.
If a command is not intended for use by moderators, there is no need for 'ul' to be included
a 'space_case' is a special scenario where you would like a command to have a single argument, but no limits to the number of separate strings you can input, such as '!requests', wherein directly after you would type an entire set of search items, but they should not be counted as arguments. Normally, arguments are separated by spaces.

## Finally

### To run:

`./serve.py`
