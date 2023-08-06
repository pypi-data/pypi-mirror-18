import operator

from pkg_resources import parse_version


operator_mapping = {"<": operator.lt, "<=": operator.le, "==": operator.eq, "!=": operator.ne, ">=": operator.ge,
                    ">": operator.gt}


def compare_versions_str(version_str_obj1, comparison_operator_str, version_str_obj2, default=False):
    if version_str_obj1 is None or version_str_obj2 is None or comparison_operator_str not in operator_mapping:
        return default
    v1 = parse_version(version_str_obj1)
    op = operator_mapping[comparison_operator_str]
    v2 = parse_version(version_str_obj2)
    return op(v1, v2)
