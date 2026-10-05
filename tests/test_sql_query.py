import pytest

from svm_mms_common_utils.sql.sql_query import QueryType, SQL_Query


def test_query_type_values_and_repr():
    assert [member.value for member in QueryType] == [
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE",
        "UNKNOWN",
    ]
    assert repr(QueryType.SELECT) == "SELECT"
    assert QueryType("DELETE") is QueryType.DELETE

    with pytest.raises(ValueError):
        QueryType("MERGE")


def test_select_to_dict_and_compiled_sql():
    query = SQL_Query(
        queryType=QueryType.SELECT,
        tableName="MMS_FOO",
        columns=["id", "name"],
        joinTables=["MMS_BAR"],
        where=[{"column": "id", "value": 7}, {"column": "name", "value": "alpha"}],
    )

    assert query.to_dict() == {
        "queryType": "SELECT",
        "tableName": "MMS_FOO",
        "columns": ["id", "name"],
        "joinTables": ["MMS_BAR"],
    }
    assert query.get_sql() == "SELECT id, name FROM MMS_FOO WHERE id = '7' AND name = 'alpha'"
    assert query.rawQuery == query.get_sql()


def test_select_compile_keeps_an_empty_where_clause():
    query = SQL_Query(
        queryType=QueryType.SELECT,
        tableName="MMS_FOO",
        columns=["id"],
    )

    assert query.get_sql() == "SELECT id FROM MMS_FOO WHERE "


def test_insert_compile_quotes_values_and_writes_null():
    query = SQL_Query(
        queryType=QueryType.INSERT,
        tableName="MMS_FOO",
        columns=["id", "name", "note"],
        valuesToInsert=[
            {"id": 1, "name": "alpha", "note": None},
            {"id": 2, "name": "beta"},
        ],
    )

    assert query.to_dict() == {
        "queryType": "INSERT",
        "tableName": "MMS_FOO",
        "columns": ["id", "name", "note"],
        "valuesToInsert": query.valuesToInsert,
    }
    assert (
        query.get_sql() == "INSERT INTO MMS_FOO (id, name, note) VALUES "
        "('1', 'alpha', NULL), ('2', 'beta')"
    )


def test_update_compile_quotes_null_and_joins_filters():
    query = SQL_Query(
        queryType=QueryType.UPDATE,
        tableName="MMS_FOO",
        valuesToInsert=[{"name": "alpha", "note": None}],
        where=[{"column": "id", "value": 4}],
    )

    assert query.to_dict() == {
        "queryType": "UPDATE",
        "tableName": "MMS_FOO",
        "valuesToInsert": [{"name": "alpha", "note": None}],
        "where": [{"column": "id", "value": 4}],
    }
    assert query.get_sql() == "UPDATE MMS_FOO SET name = 'alpha', note = 'NULL' WHERE id = '4'"


@pytest.mark.parametrize(
    ("values", "where", "match"),
    [
        (None, [{"column": "id", "value": 1}], "values to update and where clause"),
        ([{"name": "a"}], None, "values to update and where clause"),
        ([], [{"column": "id", "value": 1}], "values to update and where clause"),
        (
            [{"name": "a"}, {"name": "b"}],
            [{"column": "id", "value": 1}],
            "one row at a time",
        ),
    ],
)
def test_update_compile_rejects_invalid_payloads(values, where, match):
    query = SQL_Query(
        queryType=QueryType.UPDATE,
        tableName="MMS_FOO",
        valuesToInsert=values,
        where=where,
    )

    with pytest.raises(ValueError, match=match):
        query.compile_sql()


def test_delete_and_unknown_dicts_keep_the_raw_query():
    delete_query = SQL_Query(
        queryType=QueryType.DELETE,
        tableName="MMS_FOO",
        where=[{"column": "id", "value": "1"}],
        rawQuery="DELETE FROM MMS_FOO WHERE id = '1'",
    )
    unknown_query = SQL_Query(queryType=QueryType.UNKNOWN, rawQuery="VACUUM MMS_FOO")

    assert delete_query.to_dict() == {
        "queryType": "DELETE",
        "rawQuery": "DELETE FROM MMS_FOO WHERE id = '1'",
    }
    assert unknown_query.to_dict() == {"queryType": "UNKNOWN", "rawQuery": "VACUUM MMS_FOO"}
    assert delete_query.get_sql() == "DELETE FROM MMS_FOO WHERE id = '1'"
    assert unknown_query.get_sql() == "VACUUM MMS_FOO"


def test_copy_is_a_shallow_copy():
    row = {"id": 1}
    columns = ["id"]
    original = SQL_Query(
        queryType=QueryType.INSERT,
        tableName="MMS_FOO",
        columns=columns,
        valuesToInsert=[row],
        rawQuery="raw",
    )

    cloned = original.copy()
    row["id"] = 2
    columns.append("name")

    assert cloned is not original
    assert cloned.queryType is original.queryType
    assert cloned.columns is original.columns
    assert cloned.valuesToInsert is original.valuesToInsert
    assert cloned.valuesToInsert[0]["id"] == 2
    assert cloned.columns == ["id", "name"]
    assert cloned.rawQuery == "raw"
    assert cloned.tableName == "MMS_FOO"
