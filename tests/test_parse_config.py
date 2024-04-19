import os
from pyaml_env import parse_config
import pytest


def test_parse_config():
    failed = []
    for root, _, config_file in os.walk("configs"):
        for _file in config_file:
            file_path = os.path.join(root, _file)
            try:
                parse_config(file_path)
            except Exception:
                failed.append(file_path)

    if failed:
        pytest.fail(f"failed to parse config files: {' '.join(failed)}")
