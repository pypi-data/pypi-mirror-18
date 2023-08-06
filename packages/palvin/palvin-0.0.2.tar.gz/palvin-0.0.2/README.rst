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

2. palvin-attachement
---------------------

Inspired by
`sqlalchemy-imageattach <https://sqlalchemy-imageattach.readthedocs.io/en/1.0.0/>`__.

declaring attachment model.
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    # -*- coding:utf-8 -*-
    from palvin import (
        Palvin,
        FileSystemStore,
        PalvinFile,
        PalvinImage,
        file_relationship,
        image_relationship
    )

    store = FileSystemStore('/tmp/uploads')
    db = Palvin(uri='sqlite:///:memory:', store=store)

    from palvin import file_relationship, image_relationship, PalvinFile, PalvinImage


    class UserPicture(db.Model, PalvinImage):
        pass


    class File(db.Model, PalvinFile):
        pass


    class User(db.Model):
        picture = image_relationship(UserPicture)
        file = file_relationship(File)

create
~~~~~~

::

    u = User.create(picture=UserPicture.from_file(open('/tmp/test.jpg', 'rb')))
    u.save()

update
~~~~~~

::

    u = User.get(1)
    u.picture = UserPicture.from_file(open('/tmp/test.jpg', 'rb'))
    u.save()

delete
~~~~~~

::

    u = User.get(1)
    u.picture = None
    u.save()
