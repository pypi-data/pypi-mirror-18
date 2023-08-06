#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import optparse
import os
import sys
import textwrap

from pysodbm import Database

__author__ = 'Marco Bartel'

LOG = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class mysqlTableConverter(object):
    fieldTypeMapping = {
        'int': 'int',
        'text': 'str',
        'float': 'float',
        'numeric': 'Decimal',
        'datetime': 'datetime.datetime',
        'char': 'str',
        'bigint': 'int',
        'smallint': 'int',
        'binary': 'str',
        'mediumblob': 'str',
        'tinyint': 'int',
        'blob': 'str',
        'varchar': 'str',
        'timestamp': 'datetime.datetime',
        'time': 'datetime.time',
        'date': 'datetime.date',
        'tinytext': 'str',
        'mediumint': 'int',
        'decimal': 'Decimal',
        'mediumtext': 'str',
        'longtext': 'str',
        'double': 'float',
        'varbinary': 'str',
        'tinyblob': 'str',
        'longblob': 'str'
    }

    @staticmethod
    def convertField(fieldTypeStr, valueStr):
        if fieldTypeStr == "str":
            if valueStr is None:
                return "None"
            else:
                return "\"%s\"" % valueStr
        elif fieldTypeStr == "datetime.datetime":
            if valueStr == "CURRENT_TIMESTAMP":
                return "None"
        else:
            return valueStr


class TableNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class command(object):
    @classmethod
    def splitCommand(cls, args):
        if len(args) == 0:
            return None, []
        cmd, params = args[0], args[1:]
        return cmd, params


class cli(object):
    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option('-l', '--host', dest='host', help='hostname')
        parser.add_option('-u', '--user', dest='user', help='username')
        parser.add_option('-p', '--password', dest='password', help='password')
        parser.add_option('-d', '--database', dest='database', help='database')
        (options, args) = parser.parse_args()

        config = {
            "host": options.host,
            "user": options.user,
            "passwd": options.password,
            "db": options.database,
        }
        if not all(config.values()):
            parser.print_help()
            sys.exit()

        self.db = Database(config=config)
        cmd, args = command.splitCommand(args)

        if cmd == "dumpModel":
            self.dumpModel(args)

        elif cmd == "dumpAllModels":
            self.dumpAllModels(args)

    def dumpModel(self, args):
        tableName, args = command.splitCommand(args)
        filePath, args = command.splitCommand(args)

        if not tableName and not filePath:
            return

        tName = self.camelTableName(tableName)
        corePath = os.path.join(filePath, "{tName}CoreModel.py".format(tName=tName))
        path = os.path.join(filePath, "{tName}Model.py".format(tName=tName))
        initpath = os.path.join(filePath, "__init__.py")
        print("dump", tableName, "to", filePath)
        try:
            self.generateCoreModel(tableName=tableName, filePath=corePath)
            self.generateModel(tableName=tableName, filePath=path)
            self.updateInitPy(tableName=tableName, filePath=initpath)

        except TableNotFoundException as e:
            print("table not found.")

    def dumpAllModels(self, args):
        """

        :param args: filepath [filter] [filterquery]
        :return:
        """
        filePath, args = command.splitCommand(args)

        if not filePath:
            return

        tables = list(x[0] for x in self.db.dbQuery("show full tables where Table_type = 'BASE TABLE'"))

        if len(args) >= 2:
            cmd, args = command.splitCommand(args)
            if cmd == "filter":
                filterquery = args[0].strip()
                if filterquery[0] == '*':
                    filter = filterquery[1:]
                    tables = list(t for t in tables if not t.endswith(filter))
                elif filterquery[-1] == '*':
                    filter = filterquery[:-1]
                    tables = list(t for t in tables if not t.startswith(filter))

        print(tables)

        for table in tables:
            self.dumpModel([table, filePath])

    def camelTableName(self, tableName, dePluralization=True):
        tableName = tableName.replace("&", "_and_")
        tName = "".join(list(x.capitalize() for x in tableName.split("_")))
        if dePluralization:
            if not tName.endswith('ss'):
                tName = tName[:-1] if tName.endswith('s') else tName
        return tName

    def createDirs(self, filePath):
        dirname = os.path.dirname(filePath)
        if not os.path.exists(dirname):
            print("create directory {dirname}".format(dirname=dirname))
            os.makedirs(dirname)

    def getColumnInfo(self, tableName):
        specialDefault = {"CREATED": "dbNow", "LOG_TIME": "dbNow"}

        try:
            fields = self.db.dbQueryDict("show full columns from %s" % tableName)
        except:
            raise TableNotFoundException("table not found")

        pkFields = {}
        pkret = ""
        ret = []
        for field in fields:
            fieldName = field["Field"].upper()
            comment = field["Comment"]
            mysqlFieldType = field["Type"].lower().split("(")[0]
            pythonFieldType = mysqlTableConverter.fieldTypeMapping[mysqlFieldType]

            key = field["Key"]
            if key == "PRI":
                pkFields[fieldName] = field

            defaultValue = mysqlTableConverter.convertField(pythonFieldType, field["Default"])

            if fieldName in specialDefault.keys():
                defaultValue = specialDefault[fieldName]

            extra = ", extra=\"%s\"" % field["Extra"] if field["Extra"] != "" else ""
            ret.append("{fieldName} = DbModelField(\"{comment}\", {fieldType}, {defaultValue}{extra})".format(
                fieldName=fieldName,
                comment=comment,
                fieldType=pythonFieldType,
                defaultValue=defaultValue,
                extra=extra
            )
            )

        pkret += u"\t\tfields={\n"
        pkret += u",\n".join(list(u"\t\t\t\"%s\": %s" % (key, key) for key in pkFields.keys()))
        pkret += u"\n\t\t},\n"
        pkret += u"\t\tprimaryKey=True\n"

        if len(pkFields) != 0:
            pkFieldList = ",\n".join(list("\"{key}\": {key}".format(key=key) for key in pkFields.keys()))
            pkret = """
            dbPrimaryKey = DbModelKey(
                fields={{
                    {pkFieldList}
                }},
                primaryKey=True
            )
            """
            pkret = textwrap.dedent(pkret)
            pkret = pkret.format(
                pkFieldList=self.indentText(pkFieldList, 2)
            )

        else:
            pkret = ""
        return ret, pkret

    def indentText(self, text, indents, indentWidth=4, first=False):
        tsp = text.split("\n")
        ret = []
        for t in tsp:
            if not first:
                ret.append(t)
                first = True
                continue
            ret.append(" " * indentWidth * indents + t)
        return "\n".join(ret)

    def generateCoreModel(self, tableName=None, filePath=None):
        self.createDirs(filePath)
        print("generating {filePath}".format(filePath=filePath))
        columns, pk = self.getColumnInfo(tableName=tableName)
        fieldData = "\n    ".join(columns)

        primaryKeyDef = self.indentText(pk, 1)
        data = """
        #!/usr/bin/env python
        # -*- coding: utf-8 -*-

        from pysodbm import *
        import datetime
        from decimal import Decimal

        __author__ = 'pysodbmcli'

        class {camelTableName}CoreModel(DbModel):
            {fieldData}

            dbTableName = "{tableName}"
            {primaryKeyDef}
        """

        data = textwrap.dedent(data)
        data = data.format(
            tableName=tableName,
            camelTableName=self.camelTableName(tableName),
            fieldData=fieldData,
            primaryKeyDef=primaryKeyDef,
        )
        with open(filePath, "w", encoding="utf8") as fd:
            fd.write(data[1:])

    def generateModel(self, tableName=None, filePath=None):
        self.createDirs(filePath)
        if os.path.exists(filePath):
            return

        print("generating {filePath}".format(filePath=filePath))

        data = """
            #!/usr/bin/env python
            # -*- coding: utf-8 -*-

            from pysodbm import DbDataClass, DbSingletonClass
            from .{camelTableName}CoreModel import {camelTableName}CoreModel

            __author__ = 'pysodbmcli'


            class {camelTableName}Model({camelTableName}CoreModel):
                pass

            class {camelTableName}Data(DbDataClass):
                dbModel = {camelTableName}Model


            class {camelTableName}(DbSingletonClass):
                dbModel = {camelTableName}Model
                dataClass = {camelTableName}Data
        """.format(camelTableName=self.camelTableName(tableName))
        data = textwrap.dedent(data)
        with open(filePath, "w", encoding="utf8") as fd:
            fd.write(data[1:])

    def updateInitPy(self, tableName=None, filePath=None):
        print("updating {filePath}".format(filePath=filePath))
        listModelNames = [self.camelTableName(tableName)]
        if os.path.exists(path=filePath):
            with open(filePath, "r", encoding="utf8") as fd:
                buffer = fd.readlines()
                for line in buffer:
                    if line.startswith("from ."):
                        modelName = line.split("import")[1].strip()
                        listModelNames.append(modelName)

        with open(filePath, "w", encoding="utf8") as fd:
            fd.write("#!/usr/bin/env python\n")
            fd.write("# -*- coding: utf-8 -*-\n\n")
            fd.write("__author__ = 'pysodbmcli'\n\n")

            for modelName in sorted(list(set(listModelNames))):
                fd.write("from .{mn}Model import {mn}\n".format(mn=modelName))


if __name__ == '__main__':
    c = cli()
