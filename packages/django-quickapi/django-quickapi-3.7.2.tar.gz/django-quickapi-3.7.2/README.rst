========
QuickAPI
========

Is an easy way to setup mechanism calls for Django projects. 
For the exchange of data is used JSON. The API is built on the RPC 
scheme: one URL address - many methods. This scheme allows you to share 
hard-structured data, such as nested into each other JavaScript 
objects:

.. code-block:: javascript

    $.quickAPI({
        url: "/api/", 
        data: {
            method: "settings.update",
            kwargs: { value: {
                    suppliers: ['s1', 's2', 's33'],
                    skip_goods: {
                        s1: ['g123', 'g321'],
                        s33: ['g098']
                    }
                }
            }
        },
        callback: function(json, status, xhr) {},
    })


.. code-block:: python

    from quickapi.client import BaseClient

    api = BaseClient()
    api.url = 'https://example.org/api/'
    api.username = 'login'
    api.password = 'passw'

    settings = {
        'suppliers': ['s1', 's2', 's33'],
        'skip_goods': {
            's1': ['g123', 'g321'],
            's33': ['g098']
        }
    }

    response = api.method('settings.update', value=settings)


Read the documentation_ for details.

.. _documentation: https://docs.rosix.org/django-quickapi/
