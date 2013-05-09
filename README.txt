Installation
============

After installing the package you will need to add the following settings
into your Django configuration:

  ACTIONKIT_API_USER = "username"
  ACTIONKIT_API_PASSWORD = "unencrypted_password"
  ACTIONKIT_API_HOST = "https://act.mydomain.com"

To use the ORM layer you will also need to configure the Actionkit client-db
as a secondary database in your settings.DATABASES.  I always call mine "ak".
This package's ORM layer does not handle routing -- it's up to you to explicitly
call .using("ak") (or whatever your client-db's alias is) every time you use
the ORM layer.  This allows you to use the same ORM models in multiple databases
(e.g. for mirroring the Actionkit database locally) and I've found it helpful
to keep the .using("ak") explicit, just to remind myself while coding that the
performance characteristics of these database queries are very different from 
a typical locally hosted read/write database.

Usage
=====

XML-RPC
-------

>>> from actionkit.utils import get_client
>>> ak = get_client()
>>> ak.act(..)

REST
----

>>> from actionkit.rest import client
>>> ak = client()
>>> ak.user.get(1)
>>> ak.action.put(100, {...})

By default the REST client checks for valid HTTP methods before making any
call, and throws an error if you're trying to use an unsupported method.
It does this by making an additional HTTP call when you access a particular
resource type, so if you're going to use the same resource type multiple
times in the same scope, you should probably save a reference to the resource
to reduce HTTP traffic:

>>> akuser = ak.user
>>> akuser.get(1)
>>> akuser.put(1, {...})
>>> akuser.get(1)

Alternatively, you can tell the client to skip this check altogether:

>>> ak = client(safety_net=False)
>>> ak.user.get(1)
>>> ak.user.put(1, {...})
>>> ak.user.get(1)

ORM
---

The ORM layer is just a normal Django models file; it's up to you to route
it to the right database and to remember not to try to save or create any
objects (which will raise database-layer exceptions if you try)

>>> from actionkit.models import CoreUser
>>> CoreUser.objects.using("ak").get(id=1)

