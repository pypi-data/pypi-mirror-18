UIP Is Pretty
=============

UIP scrapes images from reddit and unsplash, and applies them as a wallpaper on your desktop(with configurable schedule). Works with Windows, Mac and Gtk based desktops on Linux.

Examples of UIP wallpapers
==========================

![alt text]( examples/UIP_screenshot.png )
![alt text]( examples/mac_wallpaper.png )
![alt text]( examples/windows_wallpaper.png )

Set Up
======

For Users:
----------
To install UIP, just run the command
```
sudo pip install UIP
```

For Testers & Developers:
-------------------------
To install the requirements first run the command

```
sudo python3 setup.py install
```
>Note: We only support Python 3.5 or later versions.

>Note: there is no sudo for windows as well as when you have root privelages.
Just run commands without sudo

>Note: some setups use python instead of python3 and pip3 instead of pip

>Note: For some OS' you might need to install Imagetk(needed in our GUI) seperately
for eg: in Ubuntu you can install it by:
`sudo apt-get install python3-pil.imagetk`

Run
===

To run just type

```
UIP
```
from anywhere inside the terminal/console.

If you want to try out our experimental GUI feature:
use: `UIP --ui`

To install requirements for experimental GUI, run:
`pip install -r gui-requirements.txt`

For help use `UIP --help`

Contact Us
==========
https://gitter.im/NIT-dgp/General


HOW TO PACKAGE
==============
To package into **source distribution**, run the following command
```
python setup.py sdist
```
**How to test?** (this installs UIP to your library)
```
cd dist/
tar xzf UIP-<version-no>.tar.gz
cd UIP-<version-no>/
python setup.py install
```
How to run?
```
UIP.py
```

HOW TO CONTRIBUTE
=================

UIP is in its very early development stage, you can go over the issues on the
github issues page and send in a PR.

your commits in the PR should be of the form:

```
shortlog: commit message

commit body
Fixes <issue number>
```

where short log is the area/filename where you make the change
commit message is the very brief description of the change made by you and any
other additional details go into the commit body.

TESTING
=======

While developing, to test, you should first install the test-requirements
by running:

```
pip install -r test-requirements.txt
```
then test your work by the command:
```
pytest
```
If you want to lint your files you can run
```
coala
```
and commit all changes suggested

Do remember to keep your master branch updated at all times
and always work on a different branch.

Happy coding :)
