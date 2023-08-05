.. image:: https://img.shields.io/codeship/e8d9f750-264b-0134-0de7-62f9de04cc38/default.svg
   :target: https://bitbucket.org/hellwig/django-cenvars
.. image:: https://coveralls.io/repos/bitbucket/hellwig/django-cenvars/badge.svg?branch=default 
   :target: https://coveralls.io/bitbucket/hellwig/django-cenvars?branch=default
.. image:: https://img.shields.io/pypi/v/django-cenvars.svg
   :target: https://pypi.python.org/pypi/django-cenvars
.. image:: https://img.shields.io/badge/Donate-PayPal-blue.svg
   :target: https://paypal.me/MartinHellwig
.. image:: https://img.shields.io/badge/Donate-Patreon-orange.svg
   :target: https://www.patreon.com/hellwig
   
##############
django-cenvars
##############

What is it?
===========
Django Cenvars is the reference implementation of cenvars, the Centralised
Environment Variables Service. Cenvars describes a method by which a machine
fetches and sets environmental variables that are stored on a central server.


What problem does it solve?
===========================
When developing server side applications you often have to store username and
passwords for the interaction with other services. As storing these security
sensitive information in the repository is a huge risk, developers often have to
resort to either having a non-versioned secret file or store these in the 
environment variables. Both solutions provide a problem with management of these
data points. django-cenvars mitigates the management side of these problems by
requiring only the cenvars connection details to be stored in the environment.
All other variables can than be resolved via this service.

The Protocol
============

Overview
--------
For encryption we use both RSA and AES, for AES a 256 bit key is used which is
encrypted with an 2048 bit RSA key. 
The RSA is an asymmetric key, the decryption key (Private key) is used by the
client, whilst the encryption key (Public key) is used by the server.

Prior to sending the 'data' to the client, the server creates a new 256 bit AES
key. This key is used to encrypt the text block and than is encrypter with the
RSA encryption key. The resulting blob is prepended to the 


> json dict > zip > AES encrypt > 
 


> https://example.com/cenvars/?identifier=hexdigest
< BLOB

  

(this is the hexdigest of the N value of
an RSA key).




Caveat
-------
Introducing single points of failure in your architecture should not be
undertaken lightly, unless having a centralised variables services makes sense
in your setup, I would recommend against using this service.
  
The cryptography used in the library (RSA and AES) are there to provide a
barrier for accidental leaking of the raw file data, however the access keys are
in the end stored on the machines themselves, thus having login access to the
client machine will show all the environment variables of that machine.
Having login access to the server will reveal all environmental variables.

Proceed with caution, be forewarned and vigilant, you are putting all eggs into
one basket here, however unless you have another way to cryptographically
store and injecting environmental variables, this will be a big improvement,
both for security and management.



How do I install it?
====================
::

  $ pip install django-cenvars


How do I use it?
================
This is an Django-Integrator compliant project, thus in the settings file add:
::

  django_integrator.add_application('django_cenvars')

You will also need to set the following environment variables:

  - CENVARS_URL
  - CENVARS_KEY
  
The CENVARS_URL is the url where the exernal client can connect to the server
and get it's environment variables. 

The CENVARS_KEY is the encryption key used for encrypting the data in the
persistent database. It can be generated with the following command:

::

  python manage.py cenvars_newkey 


What license is this?
=====================
Two-clause BSD


How can I get support?
======================
Please use the repo's bug tracker to leave behind any questions, feedback,
suggestions and comments. I will handle them depending on my time and what looks
interesting. If you require guaranteed support please contact me via
e-mail so we can discuss appropriate compensation.


Signing Off
===========
Is my work helpful or valuable to you? You can repay me by donating via:

https://paypal.me/MartinHellwig

.. image:: https://img.shields.io/badge/PayPal-MartinHellwig-blue.svg
  :target: https://paypal.me/MartinHellwig
  :alt: Donate via PayPal.Me
  :scale: 120 %

-or-

https://www.patreon.com/hellwig

.. image:: https://img.shields.io/badge/Patreon-hellwig-orange.svg
  :target: https://www.patreon.com/hellwig
  :alt: Donate via Patreon
  :scale: 120 %


Thank you!