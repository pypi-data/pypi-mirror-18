Changelog
=========


4.3.1 (2016-11-18)
------------------

- Require transaction 1 to avoid cleanups that break ZEO 4.


4.3.0 (2016-08-02)
------------------

- Refuse to work with ZODB 5.

  Some recent cleanups in the ZODB commit protocol are incompatible with ZEO 4.

- Fix ZEO cache tracing on Python 3.

4.2.1 (2016-06-30)
------------------

- Fix bug connecting to ``localhost`` on Windows. (#8).

4.2.0 (2016-06-15)
------------------

- Changed loadBefore to operate more like load behaved, especially
  with regard to the load lock.  This allowes ZEO to work with the
  upcoming ZODB 5, which used loadbefore rather than load.

  Reimplemented load using loadBefore, thus testing loadBefore
  extensively via existing tests.

- Other changes to work with ZODB 5 (as well as ZODB 4)

- Fixed: the ZEO cache loadBefore method failed to utilize current data.

- Drop support for Python 2.6 and 3.2.

4.2.0b1 (2015-06-05)
--------------------

- Add support for PyPy.

4.1.0 (2015-01-06)
------------------

- Add support for Python 3.4.

- Added a new ``ruok`` client protocol for getting server status on
  the ZEO port without creating a full-blown client connection and
  without logging in the server log.

- Log errors on server side even if using multi threaded delay.

4.0.0 (2013-08-18)
------------------

- Avoid reading excess random bytes when setting up an auth_digest session.

- Optimize socket address enumeration in ZEO client (avoid non-TCP types).

- Improve Travis CI testing support.

- Assign names to all threads for better runtime debugging.

- Fix "assignment to keyword" error under Py3k in 'ZEO.scripts.zeoqueue'.

4.0.0b1 (2013-05-20)
--------------------

- Depend on ZODB >= 4.0.0b2

- Add support for Python 3.2 / 3.3.

4.0.0a1 (2012-11-19)
--------------------

First (in a long time) separate ZEO release.

Since ZODB 3.10.5:

- Storage servers now emit Serving and Closed events so subscribers
  can discover addresses when dynamic port assignment (bind to port 0)
  is used. This could, for example, be used to update address
  information in a ZooKeeper database.

- Client storages have a method, new_addr, that can be used to change
  the server address(es). This can be used, for example, to update a
  dynamically determined server address from information in a
  ZooKeeper database.
