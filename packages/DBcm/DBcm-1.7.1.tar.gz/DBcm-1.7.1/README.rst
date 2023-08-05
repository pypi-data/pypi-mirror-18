The UseDatabase context manager for working with MySQL/MariaDB.

For more information, see Chapters 7, 8, 9, and 11 of Head First Python, 2nd edition.

Simple usage: 

::

    from DBcm import UseDatabase, SQLError

    config = { 'host': '127.0.0.1',
               'user': 'myUserid',
               'password': 'myPassword',
               'database': 'myDB' }

    with UseDatabase(config) as cursor:
        try:
            _SQL = "select * from log"
            cursor.execute(_SQL)
            data = cursor.fetchall()
        except SQLError as err:
            print('Your query broke:', str(err))

Enjoy, and have fun.
