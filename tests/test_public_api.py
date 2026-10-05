import svm_mms_common_utils.constants as constants_pkg
import svm_mms_common_utils.enums as enums_pkg
import svm_mms_common_utils.models as models_pkg
import svm_mms_common_utils.models.entities as entities_pkg
import svm_mms_common_utils.models.tables as tables_pkg
import svm_mms_common_utils.sql as sql_pkg
import svm_mms_common_utils.utils as utils_pkg


def _assert_exports(module):
    assert module.__all__
    for name in module.__all__:
        assert hasattr(module, name), name


def test_package_exports():
    _assert_exports(constants_pkg)
    _assert_exports(enums_pkg)
    _assert_exports(entities_pkg)
    _assert_exports(tables_pkg)
    _assert_exports(sql_pkg)
    _assert_exports(utils_pkg)


def test_models_package_reexports_entities_and_tables():
    for name in entities_pkg.__all__ + tables_pkg.__all__:
        assert hasattr(models_pkg, name), name
