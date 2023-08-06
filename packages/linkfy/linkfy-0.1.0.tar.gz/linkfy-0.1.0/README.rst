linky
-----

Change plain text into HTML has ``<a>`` tag.


Getting started
===============

Call ``linky.linky``.

.. code-block:: python
   
   from linky import linky

   linky('Serching on https://google.com') # Serching on <a href="https://google.com">https://google.com</a>

Usually thease function is used on Jinja_, so it provide options to
escape some HTML special characters like ``<``, ``>``.


.. code-block:: python

   from linky import linky

   linky('Serching < on https://google.com') # Serching &lt; on <a href="https://google.com">https://google.com</a>


.. _Jinja: http://jinja.pocoo.org/
