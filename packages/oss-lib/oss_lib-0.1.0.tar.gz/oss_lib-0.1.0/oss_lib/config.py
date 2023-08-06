import logging
import os
import re

import yaml

LOG = logging.getLogger(__name__)
CONF = None


def get_env_prefix(service_name):
    assert re.match(r"^[a-zA-Z][-\w]*$", service_name), \
        "service_name have to start from letter and can contain letters, " \
        "numbers, dashes and underscores"
    prefix = service_name.upper().replace("-", "_")
    return prefix


def setup_config(service_name, default_config=None):
    conf_filename = ""
    try:
        with open(
