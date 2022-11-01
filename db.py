import pickle
import random

import asyncpg


class DataBase:

    def __init__(self,
                 db_user: str,
                 db_password: str,
                 IP: str,
                 db_port: int,
                 db_name: str
                 ):
        self.user = db_user
        self.password = db_password
        self.host = IP
        self.port = db_port
        self.database = db_name
        self.fields = [
            'id', 'user_id', 'title', 'description', 'content',
            'price', 'url', 'data', 'is_published', 'status'
        ]
        self.fields_str = ', '.join(self.fields)
        self.count_str = ', '.join(
            f'${i}' for i in range(1, len(self.fields) + 1)
        )
        self.titles = tuple(pickle.load(open('pickles/titles.txt', 'rb')))
        self.content = tuple(
            pickle.load(open('pickles/words_pickle.txt', 'rb')))
        self.data = tuple(pickle.load(open('pickles/datas_pickle.txt', 'rb')))
        self.url = tuple(pickle.load(open('pickles/urls_pickle.txt', 'rb')))
        self.fields = set(self.fields)
        self.conn = None

    async def create_connector(self):

        return await asyncpg.connect(
            user=self.user, password=self.password,
            host=self.host, port=self.port,
            database=self.database
        )

    async def create_data(self):
        self.conn = await self.create_connector()
        try:
            sql = """
            CREATE TABLE Data (
            id serial,
            user_id integer NOT NULL ,
            title varchar(255) NOT NULL ,
            description varchar(1000) NOT NULL ,
            content text NOT NULL ,
            price integer NOT NULL,
            url varchar(100) Not Null,
            data date NOT NULL,
            is_published boolean NOT NULL ,
            status boolean NOT NULL,
            PRIMARY KEY (id)
            )
            """
            await self.conn.execute(sql)
            for i in range(10_000):
                await self.add_data(
                    i, random.randint(1, 100), random.choice(self.titles),
                    random.choice(self.content)[:999],
                    random.choice(self.content),
                    random.randint(1, 1000), random.choice(self.url),
                    random.choice(self.data), bool(random.randint(0, 1)),
                    bool(random.randint(0, 1))
                )
        except asyncpg.exceptions.DuplicateTableError:
            pass
        except Exception as ex:
            print(f'Error {ex}')

        del self.titles
        del self.content
        del self.data
        del self.url

    def validate_fields(self, fields: str) -> list[str]:
        result = []
        for field in fields.split(','):
            if field in self.fields:
                result.append(field)
        return result

    async def add_data(self, *args):
        sql = f"INSERT INTO Data ({self.fields_str}) VALUES ({self.count_str})"
        await self.conn.execute(sql, *args)

    async def select_datas(self,
                           fields: str = '',
                           limit=None,
                           offset=None) -> tuple:
        if not self.conn:
            self.conn = await self.create_connector()
        valid_fields = self.validate_fields(fields)
        valid_fields_str = (f'({", ".join(valid_fields)})' if valid_fields
                            else '*')
        limit = f'LIMIT {limit}' if limit is not None and limit >= 0 else ''
        offset = (f'OFFSET {offset}' if offset is not None and
                                        offset >= 0 else '')
        sql = f"SELECT {valid_fields_str} FROM Data {limit} {offset}"
        return valid_fields, await self.conn.fetch(sql)

    async def select_data(self, id: int, fields: str = '') -> dict:
        if not self.conn:
            self.conn = await self.create_connector()
        valid_fields = self.validate_fields(fields)
        valid_fields_str = (f'({", ".join(valid_fields)})' if valid_fields
                            else '*')
        sql = f"SELECT {valid_fields_str} FROM Data WHERE id = $1"
        data = (await self.conn.fetchrow(sql, id))
        if data:
            if fields:
                return {i: x for i, x in
                        zip(valid_fields, data['row'])}
            return dict(data)
        return {'error': f'no item number {id}'}

    async def stop_db(self):
        if self.conn:
            self.conn.close()
