nameko-objectstorage
=================

A IBM Bluemix Object Storage dependency for `nameko <http://nameko.readthedocs.org>`_, enabling services to interface with object storage containers and objects. Future improvements are full support for open stack object storage in general.

Usage
-----

.. code-block:: python

    from nameko_objectstorage import ObjectStorage

    class Service:

        storage = ObjectStorage()

        @event_handler("dispatcher", "topic")
        def handler(self, payload):
            obj = self.storage.get_object(container, object_name)

            # Do stuff with object


            ...

To-Do
-----
1. Write tests!
2. Implement support for native open stack.
