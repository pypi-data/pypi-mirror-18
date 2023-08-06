# -*- coding: utf8 -*-

"""
Eines per a la connexió a bases de dades relacionals (Oracle i MariaDB)
i la manipulació de les seves dades i estructures.
"""

import json
import os
import random
import subprocess
import time

import cx_Oracle
import MySQLdb.cursors

from .constants import (APP_CHARSET, IS_PYTHON_3, TMP_FOLDER,
                        MARIA_CHARSET, MARIA_COLLATE, MARIA_STORAGE)
from .aes import AESCipher
from .textfile import TextFile


pth = os.path.dirname(os.path.abspath(__file__))
json_file = '{}/database.json'.format(pth)
INSTANCES = json.load(open(json_file))['instances']
CREDENTIALS = json.load(open(json_file))['credentials']


class Database(object):
    """
    Classe principal. S'instancia per cada connexió a una base de dades.
    Tots els mètodes es poden utilitzar per Oracle i MariaDB
    si no s'especifica el contrari.
    """

    def __init__(self, instance, schema, retry=None):
        """
        Inicialització de paràmetres i connexió a la base de dades.
        En cas d'error, intenta cada (retry) segons.
        """
        attributes = INSTANCES[instance]
        self.engine = attributes['engine']
        self.host = attributes['host']
        self.port = attributes['port']
        if self.engine == 'my':
            self.local_infile = attributes['local_infile']
            self.user, self.password = CREDENTIALS[instance]
            self.database = schema
        elif self.engine == 'ora':
            self.sid = attributes.get('sid', None)
            self.service_name = attributes.get('service_name', None)
            self.user, self.password = CREDENTIALS[instance][schema]
        self.available = False
        while not self.available:
            try:
                self.connect()
            except Exception as e:
                if '1049' in str(e):
                    self.connect(existent=False)
                    self.recreate_database()
                elif retry:
                    time.sleep(retry)
                else:
                    raise
            else:
                self.available = True

    def connect(self, existent=True):
        """Desencripta password i connecta a la base de dades."""
        password = AESCipher().decrypt(self.password) if self.password else ''
        if self.engine == 'my':
            self.connection = MySQLdb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=password,
                db=self.database if existent else 'information_schema',
                cursorclass=MySQLdb.cursors.SSCursor,
                charset=APP_CHARSET,
                use_unicode=IS_PYTHON_3,
                local_infile=1 * self.local_infile
            )
        elif self.engine == 'ora':
            if self.sid:
                self.dsn = cx_Oracle.makedsn(self.host, self.port, self.sid)
            else:
                self.dsn = cx_Oracle.makedsn(self.host,
                                             self.port,
                                             service_name=self.service_name)
            self.connection = cx_Oracle.connect(self.user, password, self.dsn)

    def execute(self, sql):
        """Executa una sentència SQL."""
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        self.cursor.close()
        self.connection.commit()

    def recreate_database(self):
        """Elimina i torna a crear una base de dades (MariaDB)."""
        self.execute('drop database if exists {}'.format(self.database))
        sql = 'create database {} character set {} collate {}'
        self.execute(sql.format(self.database, MARIA_CHARSET, MARIA_COLLATE))
        self.execute('use {}'.format(self.database))

    def create_table(self, table, columns, partitions=None, remove=False):
        """Crea una taula a la base de dades."""
        if remove:
            try:
                self.execute('drop table {}'.format(table))
            except:
                pass
        spec = '({})'.format(', '.join(columns))
        if self.engine == 'my':
            this = ' engine {} character set {} collate {}'
            spec += this.format(MARIA_STORAGE, MARIA_CHARSET, MARIA_COLLATE)
        if partitions:
            this = ' partition by hash (id) partitions {}'
            spec += this.format(partitions)
        try:
            self.execute('create table {} {}'.format(table, spec))
        except Exception as e:
            s = str(e)
            if not any([word in s for word in ('1050', 'ORA-00955')]):
                raise e

    def get_all(self, sql):
        """
        Crea un generator que retorna d'un en un tots els registres
        obtinguts per una sentència SQL.
        """
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        for row in self.cursor:
            yield row
        self.cursor.close()

    def get_many(self, sql, n):
        """
        Crea un generator que retorna de n en n tots els registres
        obtinguts per una sentència SQL.
        """
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        while True:
            result = self.cursor.fetchmany(n)
            if not result:
                break
            yield result
        self.cursor.close()

    def get_one(self, sql):
        """Retorna un registre d'una sentència SQL."""
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        resul = self.cursor.fetchone()
        self.cursor.close()
        return resul

    def list_to_table(self, iterable, table, partition=None):
        """Insereix un iterable a una taula."""
        if self.engine == 'my':
            rand = random.randrange(0, 2 ** 64)
            filename = '{}/{}_{}.txt'.format(TMP_FOLDER, table, rand)
            partition = 'PARTITION ({})'.format(partition) if partition else ''
            delimiter = '@,'
            endline = '|;'
            with TextFile(filename) as file:
                file.write_iterable(iterable, delimiter, endline)
            sql = "LOAD DATA {local} INFILE '{filename}' \
                   ignore INTO TABLE {table} {partition} \
                   CHARACTER SET {charset} \
                   FIELDS TERMINATED BY '{delimiter}' \
                   LINES TERMINATED BY '{endline}'"
            sql = sql.format(
                local='LOCAL' if self.local_infile else '',
                filename=filename,
                table=table,
                partition=partition,
                charset=APP_CHARSET,
                delimiter=delimiter,
                endline=endline
            )
            self.execute(sql)
            os.remove(filename)
        elif self.engine == 'ora':
            values = [':{}'.format(i + 1) for i in range(len(iterable[0]))]
            values = ', '.join(values)
            self.cursor = self.connection.cursor()
            sql = 'insert into {} VALUES ({})'
            self.cursor.prepare(sql.format(table, values))
            self.cursor.executemany(None, iterable)
            self.cursor.close()
            self.connection.commit()

    def get_table_owner(self, table):
        """Retorna el propietari i el nom original d'una taula (Oracle)."""
        table = table.upper()
        try:
            sql = "select table_name from user_tables \
                   where table_name = '{}'"
            table, = self.get_one(sql.format(table))
            owner, = self.get_one('select user from dual')
        except TypeError:
            try:
                sql = "select table_owner, table_name from user_synonyms \
                       where synonym_name = '{}'"
                owner, table = self.get_one(sql.format(table))
                try:
                    sql = "select table_owner, table_name from all_synonyms \
                           where owner = '{}' and synonym_name = '{}'"
                    owner, table = self.get_one(sql.format(owner, table))
                except TypeError:
                    pass
            except TypeError:
                try:
                    sql = "select table_owner, table_name from all_synonyms \
                           where owner = 'PUBLIC' and synonym_name = '{}'"
                    owner, table = self.get_one(sql.format(table))
                except TypeError:
                    sql = "select owner, table_name from all_tables \
                           where table_name = '{}'"
                    owner, table = self.get_one(sql.format(table))
        return owner, table

    def get_table_count(self, table):
        """Retorna el número de registres d'una taula."""
        if self.engine == 'my':
            sql = "select table_rows from information_schema.tables \
                   where table_schema = '{}' and table_name = '{}'"
            sql = sql.format(self.database, table)
        elif self.engine == 'ora':
            owner, table = self.get_table_owner(table)
            sql = "select nvl(num_rows, 0) from all_tables \
                   where owner = '{}' and table_name = '{}'"
            sql = sql.format(owner.upper(), table.upper())
        rows, = self.get_one(sql)
        return rows

    def get_table_partitions(self, table):
        """
        Retorna un diccionari amb les particions d'una taula
        i el seu número de registres.
        """
        if self.engine == 'my':
            sql = "select partition_name, table_rows \
                   from information_schema.partitions \
                   where table_schema = '{}' and table_name = '{}' \
                   and partition_name is not null"
            sql = sql.format(self.database, table)
        elif self.engine == 'ora':
            owner, table = self.get_table_owner(table)
            sql = "select partition_name, nvl(num_rows, 0) \
                   from all_tab_partitions \
                   where table_owner = '{}' and table_name = '{}'"
            sql = sql.format(owner.upper(), table.upper())
        partitions = {}
        for partition, rows in self.get_all(sql):
            partitions[partition] = rows
        return partitions

    def disconnect(self):
        """Desconnecta de la base de dades."""
        self.connection.close()

    def __enter__(self):
        """Context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager."""
        self.disconnect()
