from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any


class QueryType(Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    UNKNOWN = "UNKNOWN"

    def __repr__(self):
        return self.value


@dataclass
class SQL_Query:
    queryType: QueryType
    rawQuery: str = None
    columns: List[str] = None
    joinTables: List[str] = None
    valuesToInsert: List[Dict[str, Any]] = None
    tableName: str = None
    where: List[Dict[str, Any]] = None

    def __dict__(self):
        dict = {
            "queryType": self.queryType.value,
        }

        match self.queryType:
            case QueryType.SELECT:
                dict["tableName"] = self.tableName
                dict["columns"] = self.columns
                dict["joinTables"] = self.joinTables
            case QueryType.INSERT:
                dict["tableName"] = self.tableName
                dict["columns"] = self.columns
                dict["valuesToInsert"] = self.valuesToInsert
            case QueryType.UPDATE:
                dict["tableName"] = self.tableName
                dict["valuesToInsert"] = self.valuesToInsert
                dict["where"] = self.where
            case _:
                dict["rawQuery"] = self.rawQuery

        return dict

    def copy(self):
        return SQL_Query(
            queryType=self.queryType,
            rawQuery=self.rawQuery,
            columns=self.columns,
            joinTables=self.joinTables,
            valuesToInsert=self.valuesToInsert,
            tableName=self.tableName,
            where=self.where,
        )

    def get_sql(self):
        self.compile_sql()
        return self.rawQuery

    def compile_sql(self):
        q = self.rawQuery
        if self.queryType == QueryType.SELECT:
            q = self.__compile_select()
        elif self.queryType == QueryType.INSERT:
            q = self.__compile_insert()
        elif self.queryType == QueryType.UPDATE:
            q = self.__compile_update()
        else:
            q = self.rawQuery
        self.rawQuery = q

    def __compile_select(self):
        # TODO: Implement SELECT query compilation
        columns = ", ".join(self.columns)
        filters = " AND ".join([f"{where['column']} = '{where['value']}'" for where in self.where])

        return f"SELECT {columns} FROM {self.tableName} WHERE {filters}"
        # raise NotImplementedError("SELECT query compilation not yet supported")

    def __compile_insert(self):
        columns = ", ".join(self.columns)

        valuesArr = []

        for valDict in self.valuesToInsert:
            valArr = []
            for column in self.columns:
                if column not in valDict:
                    continue
                valArr.append(f"'{valDict[column]}'" if valDict[column] is not None else "NULL")
            values = ", ".join(valArr)
            valuesArr.append(f"({values})")

        values = ", ".join(valuesArr)

        return f"INSERT INTO {self.tableName} ({columns}) VALUES {values}"

    def __compile_update(self):
        if len(self.valuesToInsert) == 0 or len(self.where) == 0:
            raise ValueError("UPDATE query must have values to update and where clause")

        if len(self.valuesToInsert) > 1:
            raise ValueError("UPDATE query can only update one row at a time")

        values = [
            f"{col} = '{val if val is not None else 'NULL'}'"
            for col, val in self.valuesToInsert[0].items()
        ]

        filters = " AND ".join([f"{where['column']} = '{where['value']}'" for where in self.where])

        return f"UPDATE {self.tableName} SET {', '.join(values)} WHERE {filters}"
