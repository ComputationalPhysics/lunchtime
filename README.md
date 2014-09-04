# CompPhys Lunchtime #

Reminds everyone that it is time for lunch at CompPhys.

Driven by a PHP script and MySQL database on the server side, and a Python script with Appindicator on the client side.

## Creating a debian package ##

    python setup.py --command-packages=stdeb.command bdist_deb
