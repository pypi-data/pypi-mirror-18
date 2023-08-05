nameko-cloudant
=================

A Cloudant dependency for `nameko <http://nameko.readthedocs.org>`_, enabling services to interface with cloudant nosql database. Future improvements are CouchDB and local Cloudant.

Usage
-----

.. code-block:: python

    from nameko_cloudant import DatabaseSession

    class Service:

        session = Session("databasename")

        @event_handler("dispatcher", "topic")
        def handler(self, payload):
            self.session.create_document(payload)

        @rpc
        def query_db(self):
            selector = {'name': {'$eq': 'foo'}}
            docs = self.session.get_query_result(selector)

            for doc in docs:
                print doc

            ...

To-Do
-----
1. Write tests!
2. Implement support for local bluemix instances.
3. Implement support for CouchDB.
