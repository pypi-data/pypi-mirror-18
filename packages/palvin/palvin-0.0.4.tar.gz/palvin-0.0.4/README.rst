Palvin
======

Redice SQLAlchemy Boost Library. It's based
`sqlalchemy-wrapper <https://github.com/jpscaletti/sqlalchemy-wrapper>`__.

1. declaring plavin
-------------------

::

    from palvin import Palvin

    db = Palvin(uri='sqlite:///:memory:')

    class ToDo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        ...

    db.create_all()
    todos = Todo.query.all()

