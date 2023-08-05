APIG WSGI
=========

Makes Python WSGI apps compatible with AWS API Gateway proxy resources.

Example
-------

.. code:: python

    from flask import Flask
    import apigwsgi

    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello from Flask!"

    handler = apigwsgi.Handler(my_wsgi_app)

Limitations
-----------

API Gateway doesn’t currently support binary responses, and fails if your
application sends non-unicode data.

See also
--------

-  `API Gateway proxy resource docs`_
-  `WSGI spec`_

.. _API Gateway proxy resource docs: https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html#api-gateway-proxy-resource?icmpid=docs_apigateway_console
.. _WSGI spec: https://www.python.org/dev/peps/pep-3333/
