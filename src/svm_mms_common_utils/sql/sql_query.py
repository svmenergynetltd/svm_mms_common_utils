from dataclasses import dataclass
from enum import Enum
from typing import Any


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
    rawQuery: str | None = None
    columns: list[str] | None = None
    joinTables: list[str] | None = None
    valuesToInsert: list[dict[str, Any]] | None = None
    tableName: str | None = None
    where: list[dict[str, Any]] | None = None

    def to_dict(self) -> dict[str, Any]:
        _dict: dict[str, Any] = {
            "queryType": self.queryType.value,
        }

        match self.queryType:
            case QueryType.SELECT:
                _dict["tableName"] = self.tableName
                _dict["columns"] = self.columns
                _dict["joinTables"] = self.joinTables
            case QueryType.INSERT:
                _dict["tableName"] = self.tableName
                _dict["columns"] = self.columns
                _dict["valuesToInsert"] = self.valuesToInsert
            case QueryType.UPDATE:
                _dict["tableName"] = self.tableName
                _dict["valuesToInsert"] = self.valuesToInsert
                _dict["where"] = self.where
            case _:
                _dict["rawQuery"] = self.rawQuery

        return _dict

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
        columns = ", ".join(self.columns or [])
        filters = " AND ".join(
            [f"{where['column']} = '{where['value']}'" for where in self.where or []]
        )

        return f"SELECT {columns} FROM {self.tableName} WHERE {filters}"

    def __compile_insert(self):
        columns = ", ".join(self.columns or [])

        valuesArr = []

        for valDict in self.valuesToInsert or []:
            valArr = []
            for column in self.columns or []:
                if column not in valDict:
                    continue
                valArr.append(f"'{valDict[column]}'" if valDict[column] is not None else "NULL")
            values = ", ".join(valArr)
            valuesArr.append(f"({values})")

        values = ", ".join(valuesArr)

        return f"INSERT INTO {self.tableName} ({columns}) VALUES {values}"

    def __compile_update(self):
        if not self.valuesToInsert or not self.where:
            raise ValueError("UPDATE query must have values to update and where clause")

        if self.valuesToInsert and len(self.valuesToInsert) > 1:
            raise ValueError("UPDATE query can only update one row at a time")

        values = [
            f"{col} = '{val if val is not None else 'NULL'}'"
            for col, val in self.valuesToInsert[0].items()
        ]

        filters = " AND ".join([f"{where['column']} = '{where['value']}'" for where in self.where])

        return f"UPDATE {self.tableName} SET {', '.join(values)} WHERE {filters}"
