import os
from pyaml_env import parse_config
import pytest


# TODO: Get this function from qe-metrics once we have a release for it
def verify_queries(queries_dict: dict[str, str]) -> None:
    required_queries = ["blocker", "critical-blocker"]
    missing_queries = [query for query in required_queries if query not in queries_dict]

    if len(missing_queries) == len(required_queries):
        raise ValueError(f"All queries are missing in the products file: {' '.join(missing_queries)}")

    if none_values_queries := [query for query in queries_dict if queries_dict.get(query) is None]:
        raise ValueError(f"The following queries have None values: {' '.join(none_values_queries)}")

    if extra_queries := [query for query in queries_dict if query not in required_queries]:
        raise ValueError(f"Extra queries in the products file: {' '.join(extra_queries)}")


def test_parse_config_and_verify_queries():
    parse_failed = []
    query_failed = {}
    for root, _, config_file in os.walk("configs"):
        for _file in config_file:
            file_path = os.path.join(root, _file)
            try:
                config_dict = parse_config(file_path)
                verify_queries(queries_dict=config_dict[[*config_dict][0]])

            except Exception as exp:
                if isinstance(exp, ValueError):
                    query_failed[file_path] = exp

                else:
                    parse_failed.append(file_path)

    if parse_failed or query_failed:
        msg = ""
        if parse_failed:
            msg += f"failed to parse config files: {' '.join(parse_failed)}\n"

        if query_failed:
            msg += "\n".join([f"{_key}: {_val}" for _key, _val in query_failed.items()])

        pytest.fail(msg)
