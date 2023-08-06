elasticsearch-fabric
====================

This package provides a unified command line interface to Elasticsearch
in Fabric.

Installation
------------

The current release, published on PyPI, can be installed using the
following command:

.. code:: sh

    $ pip install elasticsearch-fabric

Configuration
-------------

Tasks
~~~~~

If you plan to use the built-in tasks, include the module in your
fabfile module (e.g. fabfile.py). Most likely you might want to assign
an alias for the task namespace:

.. code:: python

    from esfabric import tasks as es

Environment
~~~~~~~~~~~

-  ``elasticsearch_clients``: Customize elasticsearch client
   configurations.
-  ``elasticsearch_alias``: Default Elasticsearch client alias in
   elasticsearch\_clients. default "default"
-  ``elasticsearch_dest_alias``: Reindex dest Elasticsearch client alias
   in elasticsearch\_clients. default elasticsearch\_alias

Examples
^^^^^^^^

.. code:: python

    # cat fabfile.py
    from fabric.api import env
    from elasticsearch import Elasticsearch
    from esfabric import tasks as es


    env.elasticsearch_clients = {
        "default": Elasticsearch(**{
            "host": "localhost",
            "port": 9200,
            "send_get_body_as": "POST"
        }),
        "example": Elasticsearch(**{
            "host": "search.example.org",
            "port": 443,
            "send_get_body_as": "POST",
            "use_ssl": True,
            "verify_certs": True
        })
    }

Elasticsearch with Shield
~~~~~~~~~~~~~~~~~~~~~~~~~

You can configure the client to use basic authentication:

.. code:: python

    # cat fabfile.py
    from fabric.api import env
    from elasticsearch import Elasticsearch
    from esfabric import tasks as es


    env.elasticsearch_clients = {
        "default": Elasticsearch(**{
          "host": "localhost",
          "port": 9200,
          "send_get_body_as": "POST",
          "http_auth": ('user', 'secret')
        })
    }

Running on AWS with IAM
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # cat fabfile.py
    from fabric.api import env
    from elasticsearch import Elasticsearch
    from elasticsearch import RequestsHttpConnection
    from requests_aws4auth import AWS4Auth
    from esfabric import tasks as es

    awsauth = AWS4Auth(YOUR_ACCESS_KEY, YOUR_SECRET_KEY, REGION, 'es')

    env.elasticsearch_clients = {
        "default": Elasticsearch(**{
            "host": "YOURHOST.us-east-1.es.amazonaws.com",
            "port": 443,
            "send_get_body_as": "POST",
            "http_auth": awsauth,
            "use_ssl": True,
            "verify_certs": True,
            "connection_class": RequestsHttpConnection
        })
    }

Checking the setup
------------------

For checking if everything is set up properly, you can run the included
task *info*. For example, running

.. code:: sh

    $ fab es.info

you can show a similar result:

.. code:: sh

    {
      "cluster_name": "elasticsearch",
      "tagline": "You Know, for Search",
      "version": {
        "lucene_version": "5.5.0",
        "build_hash": "218bdf10790eef486ff2c41a3df5cfa32dadcfde",
        "number": "2.3.3",
        "build_timestamp": "2016-05-17T15:40:04Z",
        "build_snapshot": false
      },
      "name": "Ares"
    }


    Done.

Example use
-----------

You can do this for example with the following command:

.. code:: sh

    # -------------------------------------------------------------
    # by Default connect to localhost:9200
    $ fab es.info
    {
      "cluster_name": "elasticsearch",
      "tagline": "You Know, for Search",
      "version": {
        "lucene_version": "5.5.0",
        "build_hash": "218bdf10790eef486ff2c41a3df5cfa32dadcfde",
        "number": "2.3.3",
        "build_timestamp": "2016-05-17T15:40:04Z",
        "build_snapshot": false
      },
      "name": "Ares"
    }


    Done.

    # -------------------------------------------------------------
    # index a document
    #
    # $ cat doc.json
    # {
    #   "title": "Hello Elasticsearch",
    #   "description": "elasticsearch fabric test"
    # }
    $ cat doc.json | fab es.index:index=blog,doc_type=posts,id=1
    {
      "_type": "posts",
      "created": true,
      "_shards": {
        "successful": 1,
        "failed": 0,
        "total": 2
      },
      "_version": 1,
      "_index": "blog",
      "_id": "1"
    }


    Done.

    # -------------------------------------------------------------
    # get the document.
    $ fab es.get:index=blog,doc_type=posts,id=1
    {
      "_type": "posts",
      "_source": {
        "description": "elasticsearch fabric test",
        "title": "Hello Elasticsearch"
      },
      "_index": "blog",
      "_version": 1,
      "found": true,
      "_id": "1"
    }


    Done.

    # -------------------------------------------------------------
    # simple query search.
    $ fab es.search:q="title:hello"
    {
      "hits": {
        "hits": [
          {
            "_score": 0.19178301,
            "_type": "posts",
            "_id": "1",
            "_source": {
              "description": "elasticsearch fabric test",
              "title": "Hello Elasticsearch"
            },
            "_index": "blog"
          }
        ],
        "total": 1,
        "max_score": 0.19178301
      },
      "_shards": {
        "successful": 26,
        "failed": 0,
        "total": 26
      },
      "took": 4,
      "timed_out": false
    }

    Done.

    # -------------------------------------------------------------
    # request body search.
    #
    # $ cat query.json
    # {
    #   "query": {
    #     "match": {
    #       "title": "hello"
    #     }
    #   }
    # }
    $ cat query.json | fab es.search
    {
      "hits": {
        "hits": [
          {
            "_score": 0.19178301,
            "_type": "posts",
            "_id": "1",
            "_source": {
              "description": "elasticsearch fabric test",
              "title": "Hello Elasticsearch"
            },
            "_index": "blog"
          }
        ],
        "total": 1,
        "max_score": 0.19178301
      },
      "_shards": {
        "successful": 26,
        "failed": 0,
        "total": 26
      },
      "took": 8,
      "timed_out": false
    }


    Done.

    # -------------------------------------------------------------
    # change number of replicas
    #
    # cat indices
    $ fab es.cat.indices
    health status index                  pri rep docs.count docs.deleted store.size pri.store.size
    yellow open   blog                     5   1          1            0      3.9kb          3.9kb
    # change number of replicas
    $ fab es.helpers.change_replicas:index=blog,number_of_replicas=0
    {
      "acknowledged": true
    }
    # cat indices
    $ fab es.cat.indices:v=1
    health status index                  pri rep docs.count docs.deleted store.size pri.store.size
    green  open   blog                     5   0          1            0      3.9kb          3.9kb


    # -------------------------------------------------------------
    # reindex blog to blog2
    $ fab es.helpers.reindex:source_index=blog,dest_index=blog2
    {
      "dest": {
        "index": "blog2",
        "host": "http://localhost:9200"
      },
      "source": {
        "index": "blog",
        "host": "http://localhost:9200"
      },
      "errors": 0,
      "success": 1
    }


    Done.
    # cat indices
    $ fab es.cat.indices:v=1
    health status index                  pri rep docs.count docs.deleted store.size pri.store.size
    yellow open   blog2                    5   1          1            0      3.7kb          3.7kb
    green  open   blog                     5   0          1            0      3.9kb          3.9kb

Command help
------------

.. code:: sh

    $ fab es.search:help=true

Client selection
----------------

.. code:: python

    # fabfile.py
    from esfabric import tasks as es
    from esfabric.tasks import client_selection

    env.elasticsearch_clients = {
        "client1": Elasticsearch(**{
          ...
        }),
        "client2": Elasticsearch(**{
          ...
        })
    }

.. code:: sh

    $ fab c:client2 es.info

``c`` is client\_selection alias

Logging
-------

you can enable the elasticsearch.trace logger and have it log a shell
transcript of your session using curl:

.. code:: python

    # fabfile.py
    import logging
    tracer = logging.getLogger('elasticsearch.trace')
    tracer.setLevel(logging.DEBUG)
    tracer.addHandler(logging.FileHandler('/tmp/elasticsearch-py.sh'))

Custom Task
-----------

.. code:: python

    from esfabric import tasks as es
    from fabric.api import execute, task


    @task
    def change_replicas(number_of_replicas=1):
        execute(es.cat.indices, v=1)
        execute(es.helpers.change_replicas, number_of_replicas=number_of_replicas)
        execute(es.cat.indices, v=1)

run task:

.. code:: sh

    $ fab change_replicas:10

Available commands
------------------

The following command will show a list of avaliable commands.

.. code:: sh

    $ fab -l

-  Available commands
-  es.bulk
-  es.c
-  es.clear\_scroll
-  es.client\_selection
-  es.count
-  es.count\_percolate
-  es.create
-  es.delete
-  es.delete\_by\_query
-  es.delete\_script
-  es.delete\_template
-  es.exists
-  es.explain
-  es.field\_stats
-  es.get
-  es.get\_script
-  es.get\_source
-  es.get\_template
-  es.index
-  es.info
-  es.mget
-  es.mpercolate
-  es.msearch
-  es.msearch\_template
-  es.mtermvectors
-  es.percolate
-  es.ping
-  es.put\_script
-  es.put\_template
-  es.reindex
-  es.reindex\_rethrottle
-  es.render\_search\_template
-  es.scroll
-  es.search
-  es.search\_shards
-  es.search\_template
-  es.suggest
-  es.termvectors
-  es.update
-  es.update\_by\_query
-  es.cat.aliases
-  es.cat.allocation
-  es.cat.count
-  es.cat.fielddata
-  es.cat.health
-  es.cat.indices
-  es.cat.master
-  es.cat.nodeattrs
-  es.cat.nodes
-  es.cat.pending\_tasks
-  es.cat.plugins
-  es.cat.recovery
-  es.cat.repositories
-  es.cat.segments
-  es.cat.shards
-  es.cat.snapshots
-  es.cat.thread\_pool
-  es.cluster.allocation\_explain
-  es.cluster.get\_settings
-  es.cluster.health
-  es.cluster.pending\_tasks
-  es.cluster.put\_settings
-  es.cluster.reroute
-  es.cluster.state
-  es.cluster.stats
-  es.helpers.bulk
-  es.helpers.change\_replicas
-  es.helpers.reindex
-  es.helpers.scan
-  es.indices.analyze
-  es.indices.clear\_cache
-  es.indices.close
-  es.indices.create
-  es.indices.delete
-  es.indices.delete\_alias
-  es.indices.delete\_template
-  es.indices.exists
-  es.indices.exists\_alias
-  es.indices.exists\_template
-  es.indices.exists\_type
-  es.indices.flush
-  es.indices.flush\_synced
-  es.indices.forcemerge
-  es.indices.get
-  es.indices.get\_alias
-  es.indices.get\_field\_mapping
-  es.indices.get\_mapping
-  es.indices.get\_settings
-  es.indices.get\_template
-  es.indices.get\_upgrade
-  es.indices.open
-  es.indices.put\_alias
-  es.indices.put\_mapping
-  es.indices.put\_settings
-  es.indices.put\_template
-  es.indices.recovery
-  es.indices.refresh
-  es.indices.rollover
-  es.indices.segments
-  es.indices.shard\_stores
-  es.indices.shrink
-  es.indices.stats
-  es.indices.update\_aliases
-  es.indices.upgrade
-  es.indices.validate\_query
-  es.nodes.hot\_threads
-  es.nodes.info
-  es.nodes.stats
-  es.snapshot.create
-  es.snapshot.create\_repository
-  es.snapshot.delete
-  es.snapshot.delete\_repository
-  es.snapshot.get
-  es.snapshot.get\_repository
-  es.snapshot.restore
-  es.snapshot.status
-  es.snapshot.verify\_repository
