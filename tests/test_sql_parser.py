import pytest

from svm_mms_common_utils.sql.sql_parser import SQL_Parser
from svm_mms_common_utils.sql.sql_query import QueryType


def test_parse_select_extracts_columns_table_and_joins():
    query = (
        "SELECT a.id, b.name , c.qty FROM MMS_A JOIN MMS_B ON a.id = b.id JOIN MMS_C ON b.id = c.id"
    )

    parsed = SQL_Parser(f"  {query}  ").parse()

    assert parsed.queryType is QueryType.SELECT
    assert parsed.tableName == "MMS_A"
    assert parsed.columns == ["a.id", "b.name", "c.qty"]
    assert parsed.joinTables == ["MMS_B", "MMS_C"]
    assert parsed.rawQuery == query
    assert parsed.where is None
    assert parsed.to_dict() == {
        "queryType": "SELECT",
        "tableName": "MMS_A",
        "columns": ["a.id", "b.name", "c.qty"],
        "joinTables": ["MMS_B", "MMS_C"],
    }


def test_parse_select_without_join_has_an_empty_join_list():
    parsed = SQL_Parser("SELECT id FROM MMS_FOO WHERE id = '1'").parse()

    assert parsed.joinTables == []
    assert parsed.columns == ["id"]
    assert parsed.tableName == "MMS_FOO"
    assert parsed.get_sql() == "SELECT id FROM MMS_FOO WHERE "


def test_parse_insert_builds_records_from_value_tuples():
    query = "INSERT INTO MMS_FOO (id, name, qty) VALUES (1, 'alpha', 1.5), (2, 'beta', 2)"

    parsed = SQL_Parser(query).parse()

    assert parsed.queryType is QueryType.INSERT
    assert parsed.tableName == "MMS_FOO"
    assert parsed.columns == ["id", "name", "qty"]
    assert parsed.valuesToInsert == [
        {"id": 1, "name": "alpha", "qty": 1.5},
        {"id": 2, "name": "beta", "qty": 2.0},
    ]
    assert parsed.to_dict()["valuesToInsert"] == parsed.valuesToInsert
    assert (
        parsed.get_sql() == "INSERT INTO MMS_FOO (id, name, qty) VALUES "
        "('1', 'alpha', '1.5'), ('2', 'beta', '2.0')"
    )


def test_parse_insert_keeps_integer_columns_when_every_value_is_an_int():
    parsed = SQL_Parser("INSERT INTO MMS_FOO (id, qty) VALUES (1, 2), (3, 4)").parse()

    assert parsed.valuesToInsert == [{"id": 1, "qty": 2}, {"id": 3, "qty": 4}]
    assert parsed.get_sql() == "INSERT INTO MMS_FOO (id, qty) VALUES ('1', '2'), ('3', '4')"


def test_parse_to_dict_matches_parse():
    parser = SQL_Parser("SELECT id, name FROM MMS_FOO")

    assert parser.parseToDict() == parser.parse().to_dict()
    assert parser.getQueryType() is QueryType.SELECT


def test_parse_delete_splits_and_conditions():
    parsed = SQL_Parser("DELETE FROM MMS_FOO WHERE id = '15' AND status = 'PENDING'").parse()

    assert parsed.queryType is QueryType.DELETE
    assert parsed.tableName == "MMS_FOO"
    assert parsed.where == [
        {"column": "id", "value": "15"},
        {"column": "status", "value": "PENDING"},
    ]
    assert parsed.to_dict() == {
        "queryType": "DELETE",
        "rawQuery": "DELETE FROM MMS_FOO WHERE id = '15' AND status = 'PENDING'",
    }
    assert parsed.get_sql() == "DELETE FROM MMS_FOO WHERE id = '15' AND status = 'PENDING'"


def test_parse_update_falls_back_to_the_raw_query():
    raw = "UPDATE MMS_FOO SET name = 'alpha' WHERE id = '2'"

    parsed = SQL_Parser(raw).parse()

    assert parsed.queryType is QueryType.UNKNOWN
    assert parsed.rawQuery == raw
    assert parsed.tableName is None
    assert parsed.to_dict() == {"queryType": "UNKNOWN", "rawQuery": raw}


def test_parse_unknown_statement():
    parsed = SQL_Parser("UNKNOWN MMS_FOO").parse()

    assert parsed.queryType is QueryType.UNKNOWN
    assert parsed.rawQuery == "UNKNOWN MMS_FOO"


def test_get_query_type_is_case_insensitive():
    assert SQL_Parser("select id FROM MMS_FOO").getQueryType() is QueryType.SELECT
    assert SQL_Parser("insert INTO MMS_FOO (id) VALUES (1)").getQueryType() is QueryType.INSERT


def test_parse_requires_uppercase_sql_keywords():
    with pytest.raises(IndexError):
        SQL_Parser("select id from MMS_FOO").parse()


def test_get_query_type_rejects_an_unknown_verb():
    with pytest.raises(ValueError):
        SQL_Parser("MERGE INTO MMS_FOO").getQueryType()


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("", "UNKNOWN_TABLE"),
        (None, "UNKNOWN_TABLE"),
        ("   ", "UNKNOWN_TABLE"),
        ("INSERT INTO foo (a) VALUES (1)", "FOO"),
        ("insert   into   bar(a) values (1)", "BAR"),
        ("SELECT a FROM schema.table WHERE x = 1", "SCHEMA.TABLE"),
        ("UPDATE baz SET a = 1", "BAZ"),
        ("DELETE FROM qux WHERE id = 1", "QUX"),
        ("EXPLAIN ANALYZE", "ANALYZE"),
        ("VACUUM", "UNKNOWN_TABLE"),
    ],
)
def test_get_table_name(query, expected):
    assert SQL_Parser.getTableName(query) == expected
