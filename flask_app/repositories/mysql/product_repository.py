from datetime import datetime

from flask_app.database.mysql import get_connection
from flask_app.http_resources.request_control import Order
from flask_app.logging import get_logger
from flask_app.repositories.mysql import AbstractRepository
from flask_app.vos.product import ProductVO
from vendor import pymysql


class ProductRepository(AbstractRepository):
    BASE_TABLE = 'products'
    BASE_SCHEMA = 'store'
    BASE_TABLE_ALIAS = 'p'
    PK = 'id'

    def __init__(self, logger=None, mysql_connection=None):
        super().__init__(logger, mysql_connection)

    def create(self, product: ProductVO):

        keys = list(product.keys())
        # remove the PK
        keys.remove(self.PK)
        keys_str = ",".join(keys)
        values_count = len(product.values()) - 1
        values_str = ",".join(['%s' for i in range(0, values_count)])

        # query
        sql = "INSERT INTO {} ({}) VALUES ({})".format(self.BASE_TABLE, keys_str, values_str)

        product_dict = product.to_dict()
        del product_dict["id"]
        values = tuple(product_dict.values())

        # try to create
        try:
            created = self._execute(sql, values)
            # get last inserted id
            product.id = self.connection.insert_id()
            # commit
            self.connection.commit()

        except Exception as err:
            self.logger.error(err)
            self.connection.rollback()
            self._exception = err
            created = False
        finally:
            self._close()

        return created

    def get(self, value, key=None):
        key_type = '%s'
        if key is None:
            key = self.PK
        sql = "SELECT * FROM {} WHERE {} = {}".format(self.BASE_TABLE, key, key_type)

        try:
            result = self._execute(sql, value)

            item = result.fetchone()
        except Exception as err:
            self.logger.error(err)
            item = None
        finally:
            self._close()

        return item

    def list(self, where: dict, offset=None, limit=None, fields: list = None, sort_by=None, order_by=None):

        if fields is None or len(fields) == 0:
            fields = '*'
        else:
            fields = [self.BASE_TABLE_ALIAS + '.' + v for v in fields]
            fields = ",".join(fields)

        if order_by is None:
            order_by = Order.ASC

        if sort_by is None:
            sort_by = self.PK

        sort_by = self.BASE_TABLE_ALIAS + '.' + sort_by

        sql = "SELECT {} FROM {} as {}".format(fields, self.BASE_TABLE, self.BASE_TABLE_ALIAS)

        if where != dict():
            where_list = ['{} = {}'.format(self.BASE_TABLE_ALIAS + "." + k, '"{}"'.format(v) if isinstance(v, str) else v) for k, v in where.items()]
            where_str = ",".join(where_list)

            sql = sql + " WHERE {}".format(where_str)

        sql = sql + " ORDER BY {} {}".format(sort_by, order_by)

        try:
            result = self._execute(sql)
            result = result.fetchall()
        except Exception as err:
            self.logger.error(err)
            self._exception = err
            result = None
        finally:
            self._close()

        return result

    def count(self, where, sort_by=None, order_by=None):
        if order_by is None:
            order_by = Order.ASC

        if sort_by is None:
            sort_by = self.PK

        sort_by = self.BASE_TABLE_ALIAS + '.' + sort_by

        sql = "SELECT COUNT(1) as total FROM {} as {}".format(self.BASE_TABLE, self.BASE_TABLE_ALIAS)

        if where != dict():
            where_list = [
                '{} = {}'.format(self.BASE_TABLE_ALIAS + "." + k, '"{}"'.format(v) if isinstance(v, str) else v) for
                k, v in where.items()]
            where_str = ",".join(where_list)

            sql = sql + " WHERE {}".format(where_str)

        sql = sql + " ORDER BY {} {}".format(sort_by, order_by)

        try:
            result = self._execute(sql)
            result = result.fetchone()
            result = result['total']
        except Exception as err:
            self.logger.error(err)
            self._exception = err
            result = 0
        finally:
            self._close()

        return result

    def soft_delete(self, sku_parent):
        sql = "UPDATE {}.{} SET deleted_at = %s WHERE sku_parent = %s" \
            .format(self.BASE_SCHEMA, self.BASE_TABLE)

        data = (datetime.today(), sku_parent,)
        try:
            result = self._execute(sql, data)
            self.connection.commit()
        except Exception as err:
            self.logger.error("SQL: {} ".format(sql))
            self.logger.error("Params: {} ".format(data))
            self.logger.error(err)
            result = None
            self.connection.rollback()
        finally:
            self._close()

        return result
