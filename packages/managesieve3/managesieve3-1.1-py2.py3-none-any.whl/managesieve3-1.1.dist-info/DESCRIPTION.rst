============
managesieve3
============

Overview
========

A pure Python client implementation of "A Protocol for Remotely
Managing Sieve Scripts", as defined in `RFC-5804
<https://tools.ietf.org/html/rfc5804>`_.  It works with either Python
2.7 or Python 3.3+.

Module Contents
===============

class Managesieve
-----------------

The main class for interactive with sieve server.

Here are the members of the *Managesive* class.  All of these methods
may raise a *ServerResponseNo* or *ServerResponseBye* exception.  See
RFC-5804 for details on when *NO* or *BYE* is returned by the server.

*Managesieve(host=None, port=None)*

   If *host* is *None*, it defaults to 'localhost'.  If *port* is
   None, it defaults to 4190.  The connection to the server is
   immediately made.  This method may raise any exception raised by
   the *socket* module.

*cmd_authenticate(auth_type, options=None)*

   Send an *AUTHENTICATION* request to the sieve server, along with
   the speficied options, any.  On success, returns None.  If the
   authentication fails, a *ServerResponseNo* exception is raised.

*cmd_capability()*

   Send a *CAPABILITY* request to the sieve server.  Returns a list of
   tuples, one per capability returned by the server.

*cmd_checkscript(contents)*

   Send a *CHECKSCRIPT* request to the sieve server.  If the contents
   of the script are valid, returns *None*.  Otherwise, a
   *ServerResponseNo* exception is raised.

*cmd_deletescript(name)*

   Send a *DELETESCRIPT* request to the sieve server.  The script
   *name* is deleted.  Returns *None* on success.  Raises a
   *ServerResponseNo* if the script cannot be deleted (for example, if
   it does not exist or is the currently active script).

*cmd_getscript(name)*

   Send a *GETSCRIPT* request to the sieve server.  On success, the
   contents script named *name* is returned.  On error (for example,
   if the script does not exist), a *ServerResponseNo* exception is
   raised.

*cmd_havespace(name, size)*

   Send a *HAVESPACE* request to the sieve server.  *name* is the name
   of a possibly non-existent script, and *size* a size, in bytes.  If
   the server is willing to store a script named *name* of size
   *size*, then *None* is returned.  Otherwise, a *ServerResponseNo*
   exception is raised.

*cmd_listscripts()*

   Send a *LISTSCRIPT* request to the sieve server.  On success, a
   2-tuple is returned.  The first element is a set containing the
   names of all of the scripts on the server.  If a script is active,
   its name is returned in the second element of the tuple.  If no
   script is active, the second element is *None*.

*cmd_logout()*

   Send a *LOGOUT* request to the sieve server.  The user is logged
   out, and on success *None* is returned.

*cmd_noop()*

   Send a *NOOP* request to the sieve server.  This is a protocol
   no-op, and may be used to keep the connection alive.  *None* is
   returned.

*cmd_putscript(name, contents)*

   Send a *PUTSCRIPT* request to the sieve server.  A script with name
   *name* and contents specified by *contents* is stored on the
   server.  On success, *None* is returned.  If an error occurs,
   including the script contents being invalid, a *ServerResponseNo*
   exception is raised.  Note that putting a script to the server does
   not change the currently active script.

*cmd_renamescript(oldname, newname)*

   Send a *RENAMESCRIPT* request to the sieve server.  The script
   named *oldname* is renamed to *newname*.  *None* is returned on
   success.

*cmd_setactive(name)*

   Send a *SETACTIVE* request to the sieve server.  The script named
   *name* is set as the active script.  Returns *None* on success.

*cmd_starttls(keyfile=None, certfile=None, cert_reqs=_ssl.CERT_NONE, ssl_version=_ssl.PROTOCOL_SSLv23, ca_certs=None, ciphers=None)*

   Send a *STARTTLS* request to the sieve server.  *keyfile* and
   *certfile* are currently ignored.  On success, the conenction to
   the sieve server is now encrypted.  The return value is the same as
   *cmd_capabilities*, which may have changed since the connection was
   first opened.

   The *keyfile*, *certfile*, *cert_reqs*, *ssl_version*, *ca_certs*,
   and *cipher* parameters have the same meaning as (and are passed
   directly to) *ssl.wrap_socket*.

*login_plain(username, authuser, password)*

   Logs on to the sieve server, using the *PLAIN* authentication
   scheme.  *username* is the user whose account will be accessed.
   *authuser* is the name of the user being authenticated, and
   *password* is that password for *authuser*.

Exceptions
----------

BaseException
+++++++++++++

The base class for all exceptions raised by managesieve3.

ServerResponseNo
++++++++++++++++

The sieve server sent an unexpected *NO* response.  See RFC-5804 for
details.

Available fields are:

+-----------+------------------------------------------------------+
| Name      | Description                                          |
+-----------+------------------------------------------------------+
| *name*    | The name of the RFC-5804 command that was being      |
|           | executed when the server returned a NO response.     |
+-----------+------------------------------------------------------+
| *code*    | The code returned in the NO response.  This is a     |
|           | list (possibly of length 1) of the heirarchical      |
|           | response codes.                                      |
+-----------+------------------------------------------------------+
| *text*    | The human readable text error message, if any.       |
+-----------+------------------------------------------------------+
| *results* | The textual body of the response, if any.            |
+-----------+------------------------------------------------------+


ServerResponseBye
+++++++++++++++++


The sieve server sent a *BYE* response.  See RFC-5804 for details.

Available fields are:

+-----------+------------------------------------------------------+
| Name      | Description                                          |
+-----------+------------------------------------------------------+
| *name*    | The name of the RFC-5804 command that was being      |
|           | executed when the server returned a BYE response.    |
+-----------+------------------------------------------------------+
| *code*    | The code returned in the BYE response.  This is a    |
|           | list (possibly of length 1) of the heirarchical      |
|           | response codes.                                      |
+-----------+------------------------------------------------------+
| *text*    | The human readable text error message, if any.       |
+-----------+------------------------------------------------------+
| *results* | The textual body of the response, if any.            |
+-----------+------------------------------------------------------+

ServerProtocolError
+++++++++++++++++++

The client code detected a protocol error when talking to the sieve
server.

Change log
==========

1.1 2016-10-27 Eric V. Smith
----------------------------

* Remove hack for setting RPM name (issue #4).

* Always use setuptools (issue #3).

* Add additional ssl.wrap_socket() parameters to starttls().


1.0 2015-06-02 Eric V. Smith
----------------------------

* Initial release.

* Implements all RFC-5804 commands.

* Contains an extensive test suite for command parsing. I really need
  to create a dummy server to test the socket handling and STARTTLS.


