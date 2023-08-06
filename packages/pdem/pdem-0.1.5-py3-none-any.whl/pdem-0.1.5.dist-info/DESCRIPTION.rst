=========================
pdem - Process Daemonizer
=========================

Purpose
-------

A tool, consists of server and client, used to run long processes, collect information from the processes, such as
progress and time elapsed and astimated.
Client could command to run process, kill process, get info about live or already dead process.

Install
-------

::
    # pip3 install pdem


Usage of library
----------------

Write config file to ~/.config/pdem.conf

::
    $ pdem-server writeConf --conf ~/.config/pdem.conf --daemonize Yes --logLevel WARNING --daemonLogFile /tmp/pdem.log

Start server with default params, or by params, written to ~/.config/pdem.conf:

::
    $ pdem-server start

Status of server:

::
    $ pdem-server status

Stop server:

::
    $ pdem-server stop

Display help:

::
    $ pdem-server help

Display help on

Run as client, send command to server, display result and exit:

display list of running processes:
::
    $ pdem-server do proclist

display list of running and dead processes:
::
    $ pdem-server do proclist showdead

run process by a server (bash0 would became it's identifier, "name"):
::
    $ pdem-server runprocess bash0 bash_interpreter local /bin/bash

kill running process by a server:
::
    $ pdem-server kill bash0





* 2016-11-18 mihanentalpo <mihanentalpo@yandex.ru> 0.1.5
- Fixed bugs in package

* 2016-10-30 mihanentalpo <mihanentalpo@yandex.ru> 0.1.4
- Finished python3 implementation, and uploaded pypi package "pdem"

* Sun Sep 08 2013 mihanentalpo <mihanentalpo@yandex.ru> 0.0.12
- AFixed bug - when some of process' vars contain newline symbol it lead to a broken output. Now, '\n' converted to '\\n'.

* Mon May 27 2013 mihanentalpo <mihanentalpo@yandex.ru> 0.0.11
- added functionality to see old dead processes, by send "proclist showdead", and remove them by send "burndead"

* Sat May 25 2013 mihanentalpo <mihanentalpo@yandex.ru> 0.0.10
- fixed bug with stack opverflow in case of lots of incoming process'es data. But now it will consume more CPU.

* Thu Feb 28 2013 mihanentalpo <mihanentalpo@yandex.ru> 0.0.8
- added daemonization config option

* Wed Feb 27 2013 mihanentalpo <mihanentalpo@yandex.ru> 0.0.5
- added [PDEM[var:x=y]PDEM]

* Tue Feb 26 2013 mihanentalpo <mihanentalpo@yandex.ru> 0.0.4
- working release

* Wed Feb 20 2013 mihanentalpo <mihanentalpo@yandex.ru> 0.0.3
- First alpha release



