import pandas as pd
from ast import literal_eval
from .sqlQuery import QueryType, SQL_Query


class SQL_Parser:

    def __init__(self, query: str):
        self.query = query.strip()

    def parseToDict(self):
        return self.parse().__dict__()

    def parse(self):
        queryType = self.getQueryType()

        match queryType:
            case QueryType.SELECT:
                return self.__parseSelect()
            case QueryType.INSERT:
                return self.__parseInsert()
            case _:
                return self.__defaultParse()

    def getQueryType(self):
        typeStr = self.query.strip().split(" ")[0]
        cleanedTypeStr = typeStr.strip().upper()

        return QueryType(cleanedTypeStr)

    def __parseSelect(self):
        query = self.query

        tableName = query.split("FROM")[1].split(" ")[1]
        columns = query.split("SELECT")[1].split("FROM")[0].strip()
        columns = [c.strip() for c in columns.split(",")]

        # Find JOINS
        joins = query.split("JOIN")
        if len(joins) > 1:
            joinTables = [j.split(" ")[1].strip() for j in joins[1:]]
        else:
            joinTables = []

        return SQL_Query(
            queryType=QueryType.SELECT,
            tableName=tableName,
            columns=columns,
            joinTables=joinTables,
            rawQuery=self.query,
        )

    def __parseInsert(self):
        query = self.query

        tableName = query.split("INTO")[1].split("(")[0].strip()
        columns = query.split("(")[1].split(")")[0].strip()
        columns = [c.strip() for c in columns.split(",")]

        # Find last closing bracket
        qValues = query.split("VALUES")[1]
        lastBracket = qValues.rfind(")")
        # Get the values string
        valuesStr = qValues[: lastBracket + 1]
        parsedValuesArr = literal_eval(f"[{valuesStr}]")

        keyValue: pd.DataFrame = pd.DataFrame(parsedValuesArr, columns=columns)

        return SQL_Query(
            queryType=QueryType.INSERT,
            tableName=tableName,
            columns=columns,
            valuesToInsert=keyValue.to_dict(orient="records"),
            rawQuery=self.query,
        )

    def __defaultParse(self):
        return SQL_Query(
            queryType=QueryType.UNKNOWN,
            rawQuery=self.query,
        )

    @staticmethod
    def getTableName(query: str):
        tableName = query.split("FROM")[1].split(" ")[1].strip()
        return tableName
