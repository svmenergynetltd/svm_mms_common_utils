from dataclasses import dataclass
from ...sql import SQL_Query, QueryType


class BaseTableModel:
    __tablename__: str

    def to_db(self):
        raise NotImplementedError

    @classmethod
    def from_db(cls, data: dict):
        raise NotImplementedError

    def construct_query(self):
        if self.__tablename__ is None:
            raise NotImplementedError("Table name not defined")
        values = self.to_db()
        columns = values.keys()
        return SQL_Query(
            queryType=QueryType.INSERT,
            tableName=self.__tablename__,
            columns=columns,
            valuesToInsert=[values],
        )
