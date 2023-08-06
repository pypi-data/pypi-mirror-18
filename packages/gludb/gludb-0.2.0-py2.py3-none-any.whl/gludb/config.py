"""Provide gludb configuration.

This consists mainly of a mapping from Storable classes to a database
configuration. It also includes a default mapping for classes not specifically
mapped to a database.

We check for a mapping for a class in MRO (Method Resolution Order). Suppose
a class Busy derives from the three classes X, Y, and Z - all of which derive
from class Base:

    class Base(object):
        pass

    class X(Base):
        pass
    class Y(Base):
        pass
    class Z(Base):
        pass

    class Busy(X, Y, Z):
        pass

Then a check for mapping would first checking for class Busy, then (in order)
classes X, Y, Z, Base, and object. If this is the first time you've seen
multiple inheritance, you'll note that the order of Busy's super classes is
important. This is how Python resolves method calls (we didn't just make this
up). In fact, we depend on the results of the standard library call
`inspect.getmro`.

If none of the classes mentioned have a mapping, then the default mapping will
be used. If there is no default mapping, then the class can't be mapped to a
database instance and an error will be thrown.

Astute readers will note that you could map the class `object` to a database
as a kind of default mapping. We generally don't recommend this, because it
would work *sort of*. Some notes:

* Recall that we support Python 2 and 3. In Python 3.4, classes declared
  without a base class get `object` as a base class automatically. In Python
  2.7 they just don't have a base class. That means that using an `object`
  DB mapping won't work as a default in every case.
* We always check for the default database mapping last, so mapping to object
  would be the last thing checked before the actual default.
"""

# pylama:ignore=D213

from inspect import getmro
from importlib import import_module

_APPLICATION_PREFIX = None
_APPLICATION_SEP = '_'


class Database(object):
    """Configuration class.

    Represents a database instance supported by one of our backends.
    """

    def __init__(self, db_driver, **kwrds):
        """Construct instance for a driver (and optionally parameters)."""
        mod = import_module('.backends.'+db_driver, __package__)
        Backend = getattr(mod, "Backend")
        self.backend = Backend(**kwrds)

    def ensure_table(self, cls):
        """Ensure the table exists - defer to backend."""
        return self.backend.ensure_table(cls)

    def find_one(self, cls, id):
        """Find one record  - defer to backend."""
        return self.backend.find_one(cls, id)

    def find_all(self, cls):
        """Find all records - defer to backend."""
        return self.backend.find_all(cls)

    def find_by_index(self, cls, index_name, value):
        """Find records matching index query - defer to backend."""
        return self.backend.find_by_index(cls, index_name, value)

    def save(self, obj):
        """Save the object instance - defer to backend."""
        self.backend.save(obj)

    def delete(self, obj):
        """Delete the object instance - defer to backend."""
        self.backend.delete(obj)


# Note our use of a class with a singleton instance - so configuration is
# process-wide. This makes things much simpler for some users (which is one
# of our main design drivers). One potential enhancement is to allow multiple
# database mappings - perhaps as a Flask Blueprint plugin/addon
class _DatabaseMapping(object):
    def __init__(self):
        self.clear_mappings()

    def add_mapping(self, cls, db):
        self.mapping[cls] = db

    def get_mapping(self, cls, no_mapping_ok=False):
        db = None

        for candidate_cls in getmro(cls):
            db = self.mapping.get(candidate_cls, None)
            if db is not None:
                break

        if db is None:
            db = self.default_database

        if db is None:
            if no_mapping_ok:
                return None
            raise ValueError("There is no database mapping for %s" % repr(cls))

        return db

    def clear_mappings(self):
        self.default_database = None
        self.mapping = {}

_database_mapping = _DatabaseMapping()


def default_database(db):
    """Set default database config for classes without a specific mapping."""
    _database_mapping.default_database = db


def class_database(cls, db):
    """Map a class to a database configuration.

    We assume issubclass(cls, Storable)==True).
    """
    _database_mapping.add_mapping(cls, db)


def clear_database_config():
    """Reset all mappings to default state.

    Note that any in-memory databases will be lost.
    """
    _database_mapping.clear_mappings()


def get_mapping(cls, no_mapping_ok=False):
    """Return a database config object for the given class."""
    return _database_mapping.get_mapping(cls, no_mapping_ok)


def apply_db_application_prefix(name):
    """Return name with app prefix if necessary."""
    if _APPLICATION_PREFIX is not None:
        return _APPLICATION_SEP.join([_APPLICATION_PREFIX, name])
    else:
        return name


def get_db_application_prefix():
    """Global application prefix accessor."""
    return _APPLICATION_PREFIX


def get_db_application_sep():
    """Global application separator accessor."""
    return _APPLICATION_SEP


def set_db_application_prefix(prefix, sep=None):
    """Set the global app prefix and separator."""
    global _APPLICATION_PREFIX, _APPLICATION_SEP
    _APPLICATION_PREFIX = prefix
    if (sep is not None):
        _APPLICATION_SEP = sep
