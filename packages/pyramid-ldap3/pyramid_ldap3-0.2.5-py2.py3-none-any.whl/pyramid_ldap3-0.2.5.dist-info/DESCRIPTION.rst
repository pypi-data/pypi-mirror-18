``pyramid_ldap3``
=================

``pyramid_ldap3`` provides LDAP authentication services for your Pyramid
application.  It is a fork of the ``pyramid_ldap`` package with the goal
of eliminating the dependency on ``python-ldap`` and ``ldappool``,
replacing it with a dependency on ``ldap3``, which is a pure Python package
that supports both Python 2 and Python 3.

See the documentation at
http://pyramid-ldap3.readthedocs.org/en/latest/
for more information.



0.2.5
-----

- Explicitly requires ldap3 < version 2.0 because in version 2 of ldap3
  some default values have been changed and constants renamed or changed.
  This version is intended to support the older ldap3 versions.


0.2.4
-----

- The pool lifetime is now configurable



0.2.3
-----

- Account for renaming of python3-ldap to ldap3
- Proper unbinding of Connections
- Do not fill cache if caching has been disabled
- Release as source package and universal wheel


0.2.2
------

- Support server pools
- Ignore results without a dn instead of raising an error
- Escape special characters when querying for groups
- Do not cache invalid responses
- Added documentation on recursive group queries


0.2.1
------

- Use implicit binding and proper unbinding of connections.


0.2
---

- Made return values of pyramid_ldap3 compatible with pyramid_ldap.


0.1
---

-  Initial version


