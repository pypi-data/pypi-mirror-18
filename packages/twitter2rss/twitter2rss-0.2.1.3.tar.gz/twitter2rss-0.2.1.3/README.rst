-  `English <#english>`__

   -  `About <#about>`__
   -  `DISCLAIMER <#disclaimer>`__
   -  `Requirements <#requirements>`__
   -  `Git repository <#git-repository>`__
   -  `Installation <#installation>`__
   -  `Settings <#settings>`__
   -  `Web Interface <#web-interface>`__
   -  `Crontab <#crontab>`__

-  `Castellano <#castellano>`__

   -  `Acerca de <#acerca-de>`__
   -  `DISCLAIMER <#disclaimer>`__
   -  `Requisitos <#requisitos>`__
   -  `Repositorio git <#repositorio-git>`__
   -  `Instalación <#instalación>`__
   -  `Configuración <#configuración>`__
   -  `Interfaz Web <#interfaz-web>`__
   -  `Crontab <#crontab>`__

Twitter2RSS
===========

English
-------

About
~~~~~

twitter2rss searches for twitter's user data and creates a feed from it.

DISCLAIMER
~~~~~~~~~~

This program searches the data directly on the twitter's website using a
technique called scrapping, it does not use it's API. This means that
any changes made to the website can bug this program. Each time it
happens, will be fixed, but it probably will not work for a while.

Requirements
~~~~~~~~~~~~

You need a version of Python and pip equal to or greater than 3.4 and
two libraries:

-  `requests <https://pypi.python.org/pypi/requests>`__ >= 2.9.0

-  `PyRSS2Gen <https://pypi.python.org/pypi/PyRSS2Gen>`__ >= 1.1

It can be used with Python 3.2 (the version that comes with Debian
Wheezy), but it may be unreliable.

Git repository
~~~~~~~~~~~~~~

It's in two places:

-  http://daemons.cf/cgit/twitter2rss: the original repository

Installation
~~~~~~~~~~~~

As any program written in Python, is it advisable to use a virtual
environment (virtualenv), but that is user's choice. It can choosen from
the following installation methods:

Installed using pip:

.. code:: bash

    $ su -c "pip3 install twitter2rss"

Using git:

.. code:: bash

    $ git clone git: //daemons.cf/twitter2rss

    $ cd twitter2rss
    $ su -c "pip3 install -r requirements.txt"
    $ su -c "python3 setup.py install"

Settings
~~~~~~~~

This program has no options, so it should be easy to use. All it have to
be done is to create a file in the directory where ``twitter2rss`` run
and fill it with twitter user's names:

.. code:: bash

    $ cd PATH/TO/twitter2rss/
    # Edit user file. The following are just four examples
    $ echo -e "snowden\nioerror\neldiarioes\nlamarea_com" > twitter_users
    $ twitter2rss.py
    # Or if you just want to add or update one
    $ twitter2rss.py snowden

In addition, it's possible change the threads used by the program. If
they're increased and the machine is powerful enough, it will run
faster.

By default it uses two threads in the implementation of the program. You
can add up to, if the machine supports it, to five threads. From ten
threads, the speed increase is no longer noticed, so is not worth it.

Web Interface
~~~~~~~~~~~~~

This repository can be cloned directly into the root of the web server
and run as is with the standard configuration of PHP. For the nginx
virtual host, you can use the file called ``nginx_virtualhost`` file.

This interface does two things: put the Twitter user in the file
``twitter_users`` and run a Python function in which only creates the
feed of that user.

Crontab
~~~~~~~

The ``twitter2rss`` preferred execution mode is using crontab. If added
the following, should apply:

.. code:: bash

    $ crontab -e
    # A file is open and gets the following
    */5 * * * * cd /var/www/twitter2rss && twitter2rss.py

Like this, it runs every five minutes. Is recommended this low execution
time as tweets could be lost otherwise. It has to be remembered that
it's important to run it in the directory where the file
``twitter_users`` was created, since it's there where it will try to
find it.

Castellano
----------

Acerca de
~~~~~~~~~

twitter2rss busca los datos de usuarios de twitter y crea un feed a
partir de ello.

DISCLAIMER
~~~~~~~~~~

Este programa busca los datos directamente en la web de Twitter mediante
una técnica llamada scrapping, no usa su API. Esto quiere decir que
cualquier cambio que hagan a la web puede fastidiar el funcionamiento de
este programa. Cada vez que pase, se procurará arreglarlo, pero es
probable que durante un tiempo no funcione.

Requisitos
~~~~~~~~~~

Necesita una versión de Python y pip igual o superior a la 3.4 y dos
librerias:

-  `requests <https://pypi.python.org/pypi/requests>`__ >= 2.9.0

-  `PyRSS2Gen <https://pypi.python.org/pypi/PyRSS2Gen>`__ >= 1.1

Se puede usar con Python 3.2 (la versión que usa Debian Wheezy), pero
puede no ser demasiado confiable.

Repositorio git
~~~~~~~~~~~~~~~

Está en dos sitios:

-  http://daemons.cf/cgit/twitter2rss: el repositorio original

Instalación
~~~~~~~~~~~

Cómo con cualquier programa escrito en Python, es recomendable usar un
entorno virtual (virtualenv), pero eso queda a elección del usuario. Se
puede escoger entre los siguientes métodos de instalación:

Instalar usando pip:

.. code:: bash

    $ su -c "pip3 install twitter2rss"

Usando git:

.. code:: bash

    $ git clone git://daemons.cf/twitter2rss

    $ cd twitter2rss
    $ su -c "pip3 install -r requirements.txt"
    $ su -c "python3 setup.py install"

Configuración
~~~~~~~~~~~~~

Este programa no tiene ninguna opción, por lo que debería ser sencillo
de usar. Lo único que hay que hacer es crear un archivo en el directorio
en el que se ejecute ``twitter2rss`` y llenarlo con nombres de usuarias
de Twitter:

.. code:: bash

    $ cd RUTA/A/twitter2rss/
    # editar fichero de usuarios. Lo siguiente son sólo cuatro ejemplos
    $ echo -e "snowden\nioerror\neldiarioes\nlamarea_com" > twitter_users
    $ twitter2rss.py
    # O si sólo se quiere añadir o actualizar uno
    $ twitter2rss.py snowden

Además, se pueden modificar los hilos que usa el programa. Si se
aumentan y la máquina es suficientemente potente, se ejecutará más
rápido.

Por defecto usa dos hilos en la ejecución del programa. Se puede subir a
más, si la máquina lo soporta, a cinco hilos. A partir de los diez hilos
ya no se nota el incremento de velocidad, por lo que no vale la pena.

Interfaz Web
~~~~~~~~~~~~

Este repositorio se puede clonar directamente en la raiz del servidor
web y funcionará tal cual con la configuración estándar de PHP. Para el
virtual host de nginx, se puede usar el fichero llamado
``nginx_virtualhost``.

Esta interfaz hace dos cosas, meter la usuaria de Twitter en el archivo
``twitter_users`` y ejecutar una función de Python en la que sólo crea
el feed de esa usuaria.

Crontab
~~~~~~~

El modo recomendado de ejecución de ``twitter2rss`` es usando el
crontab. Con poner lo siguiente, deberia valer:

.. code:: bash

    $ crontab -e
    # Se abrirá un archivo y se mete lo siguiente
    */5 * * * * cd /var/www/twitter2rss && twitter2rss.py

Así se ejecuta cada cinco minutos. Se recomienda este tiempo de
ejecución tan bajo por que se podrian perder tweets de no ser así. Hay
que recordar que es importante que se ejecute en el directorio en el que
se ha creado el archivo ``twitter_users``, ya que es ahí dónde lo
buscará.
