# Shitty Feed To Cool Feed (sf2cf)

Some RSS feeds do not actually include any "real" content: instead, they only
provide a link to a website, which makes reading your feeds in your favorite
feed reader harder than it should be.

Shitty Feed To Cool Feed (sf2cf) turns such a shitty RSS/Atom feed into a really
cool one, featuring the actual content users are interested in. 

Some plugins come bundled with sf2cf, and users may write their own plugins in
order to support more websites (see HACKING). 


## Installation

$ python3 setup.py install --user

OR

\# python3 setup.py install


## Usage example
List all the available plugins:
```sh
$ sf2cf -l
dilbert 0.1
	This feed provider creates an ATOM feed similar to the one provided by
http://www.dilbert.com, but makes sure the comic is included.
```

Get more help about a given plugin:
```sh
$ sf2cf --help-dilbert
* DESCRIPTION
This feed provider creates an ATOM feed similar to the one provided by
http://www.dilbert.com, but makes sure the comic is included.

* SAMPLE CONF
[feed:dilbert]
plugin=dilbert
output=/path/to/output.xml
```

A configuration file must be provided to sf2cf. See the relevant plugin help for
its configuration documentation.
```sh
$ cat config.ini
[feed:dilbert]
plugin=dilbert
output=/home/user/rss-feeds/dilbert.xml
```

Then, one may run sf2cf like this:
```sh
$ sf2cf -c config.ini
[+] Loading dilbert
[+] Using http://www.dilbert.com/feed as an input feed.
[+] Writing the output feed to /home/user/rss-feeds/dilbert.xml.
```

This should probably done using cron(8).


