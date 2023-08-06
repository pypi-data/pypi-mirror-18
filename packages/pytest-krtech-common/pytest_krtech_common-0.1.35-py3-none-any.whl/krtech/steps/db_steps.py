# coding=utf-8
"""DbSteps"""

import allure
from hamcrest import assert_that, has_length, equal_to
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbSteps(object):
    """Класс взаимодействия пользователя с базой данных

    Attributes:
          host: сервер БД
          user: пользователь БД
          password: пароль входа БД
          db: название БД
          engine: инстанс класса Engine с набором параметров для соединения с БД
    """

    def __init__(self, config):
        self.host = config.mysqlhost
        self.user = config.mysqluser
        self.password = config.mysqlpassword
        self.db = config.mysqldb
        self.engine = create_engine('mysql+mysqldb://' + self.user + ':' + self.password
                                    + '@' + self.host + '/' + self.db + '?charset=utf8', echo=False)

    def query_first(self, table, filter_):
        """Выборка первой записи по указанному фильтру из таблицы
        
        Args:
            table: представление таблицы БД
            (см. http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table)
            filter_: фильтр данных из таблицы

        Returns:
            Первый результат запроса (заполненный 'table' инстанс) или None если резутат не содержит записей.
            Example: user.query_first(History, History.mobile_phone == '3456774')
        """
        s = sessionmaker(bind=self.engine, expire_on_commit=False)()
        result = s.query(table).filter(filter_).first()
        s.close()
        return result

    def query_all(self, table, filter_):
        """Выборка всех записей по указанному фильтру из таблицы

        Example: user.query_all(Advance, Advance.advance_time.like('2015-10-08%'))

        Args:
            table: представление таблицы БД
            (см. http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table)
            filter_: фильтр данных из таблицы

        Returns:
              список всех найденных записей
        """
        s = sessionmaker(bind=self.engine, expire_on_commit=False)()
        results = s.query(table).filter(filter_).all()
        s.close()
        return results

    def add(self, params):
        """Добавление данных в таблицу

        Example: user.add(users.OPERATOR.customers_data)

        Args:
            params: представление таблицы БД
            (см. http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table)
        """
        s = sessionmaker(bind=self.engine, expire_on_commit=False)()
        s.add(params)
        s.commit()
        s.close()

    def update(self, table, filter_, params):
        """Обновление данных в таблице базы данных

        Args:
            table: представление таблицы БД
            (см. http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table)
            filter_: фильтр данных из таблицы
            params: параметры с новыми данными, например {"name": 'new_name'}

        Returns: количество строк которые были обновлены
        """
        s = sessionmaker(bind=self.engine, expire_on_commit=False)()
        result = s.query(table).filter(filter_).update(params)
        s.commit()
        s.close()
        return result

    def delete(self, table, filter_):
        """Удаление записи(ей) из таблицы

        Example: user.delete(Customers, Customers.id == 3)

        Args:
            table: представление таблицы БД
            (см. http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table)

            filter_: фильтр данных из таблицы
        """
        s = sessionmaker(bind=self.engine)()
        s.delete(self.query_first(table, filter_))
        s.commit()
        s.close()

    @allure.step("Проверяет наличие записи '{2}' в таблице данных '{1}' ")
    def should_see_db_entry(self, table, filter_):
        """Проверяет наличие одной записи в таблице данных table по определённому условию filter_

        Args:
            table: представление таблицы БД
            (см. http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table)

            filter_: фильтр
            (см. http://docs.sqlalchemy.org/en/latest/orm/query.html?highlight=query#sqlalchemy.orm.query.Query.filter)
        """
        assert_that(self.query_all(table, filter_), has_length(1),
                    str(table) + u' не должна содержать запись ' + str(filter_.__getattribute__('left')) + ':' +
                    str(filter_.__getattribute__('right').value))

    @allure.step("Проверяет отсутствие записи '{2}' в таблице данных '{1}' ")
    def should_not_see_db_entry(self, table, filter_):
        """Проверяет отсутствие записей в таблице данных table удовлетворяющей условию filter_

        Args:
            table: представление таблицы БД
            (см. http://docs.sqlalchemy.org/en/latest/core/metadata.html#sqlalchemy.schema.Table)
            filter_: фильтр
            (см. http://docs.sqlalchemy.org/en/latest/orm/query.html?highlight=query#sqlalchemy.orm.query.Query.filter)
        """
        assert_that(self.query_all(table, filter_), has_length(0),
                    str(table) + u' не должна содержать запись ' + str(filter_.__getattribute__('left')) + ':' +
                    str(filter_.__getattribute__('right').value))

    @allure.step("Проверяет запись '{2}:{3}' в базе данных = {1} ")
    def should_see_db_entry_value(self, entry, column_name, value):
        """Проверяет значение для записи в базе данных

        Args:
            entry: интстанс класс sqlalchemy.schema.Table с данными из базы
            column_name: наименование таблицы
            value: ожидаемое значение
        """
        assert_that(entry.__getattribute__(column_name), equal_to(value),
                    u'Значение атрибута \"' + column_name + '\"  записи ' + str(entry) + ' не соответствуют ожидаемому')
