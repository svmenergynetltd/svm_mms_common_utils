import pandas as pd
from ast import literal_eval
from .sqlQuery import QueryType, SQL_Query
import re


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
            case QueryType.DELETE:
                return self.__parseDelete()
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

    def __parseDelete(self):
        query = self.query

        tableName = query.split("FROM")[1].split(" ")[1]
        whereClause = query.split("WHERE")[1].strip()

        # Parse the WHERE clause to get the conditions
        conditions = whereClause.split("AND")
        parsedConditions = []
        for condition in conditions:
            column, value = condition.split("=")
            parsedConditions.append({"column": column.strip(), "value": value.strip().strip("'")})

        return SQL_Query(
            queryType=QueryType.DELETE,
            tableName=tableName,
            where=parsedConditions,
            rawQuery=self.query,
        )

    def __defaultParse(self):
        return SQL_Query(
            queryType=QueryType.UNKNOWN,
            rawQuery=self.query,
        )

    @staticmethod
    def getTableName(query: str) -> str:
        if not query:
            return "UNKNOWN_TABLE"

        # Normalize whitespace
        q = " ".join(query.strip().split())
        q_upper = q.upper()

        try:
            # INSERT INTO table (...)
            if q_upper.startswith("INSERT"):
                match = re.search(r"INSERT\s+INTO\s+([^\s(]+)", q_upper)
                return match.group(1) if match else "UNKNOWN_TABLE"

            # SELECT ... FROM table ...
            if q_upper.startswith("SELECT"):
                match = re.search(r"FROM\s+([^\s]+)", q_upper)
                return match.group(1) if match else "UNKNOWN_TABLE"

            # UPDATE table SET ...
            if q_upper.startswith("UPDATE"):
                match = re.search(r"UPDATE\s+([^\s]+)", q_upper)
                return match.group(1) if match else "UNKNOWN_TABLE"

            # DELETE FROM table ...
            if q_upper.startswith("DELETE"):
                match = re.search(r"DELETE\s+FROM\s+([^\s]+)", q_upper)
                return match.group(1) if match else "UNKNOWN_TABLE"

            # Fallback: second token
            parts = q_upper.split(" ")
            return parts[1] if len(parts) > 1 else "UNKNOWN_TABLE"

        except Exception:
            return "UNKNOWN_TABLE"
