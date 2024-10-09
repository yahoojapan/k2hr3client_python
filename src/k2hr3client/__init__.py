# -*- coding: utf-8 -*-
#
# k2hr3client - Python client for K2HR3 REST API
#
# Copyright 2020 Yahoo Japan Corporation
# Copyright 2024 LY Corporation
#
# K2HR3 is K2hdkc based Resource and Roles and policy Rules, gathers
# common management information for the cloud.
# K2HR3 can dynamically manage information as "who", "what", "operate".
# These are stored as roles, resources, policies in K2hdkc, and the
# client system can dynamically read and modify these information.
#
# For the full copyright and license information, please view
# the license file that was distributed with this source code.
#
# AUTHOR:   Hirotaka Wakabayashi
# CREATE:   Mon Sep 14 2020
# REVISION:
#
#
"""K2HR3 Python Client of Token API."""

__author__ = 'Hirotaka Wakabayashi <hiwakaba@lycorp.co.jp>'
__version__ = '1.1.1'

import configparser
from pathlib import Path
import sys

if sys.platform.startswith('win'):
    raise ImportError(r'Currently we do not test well on windows')


def get_version() -> str:
    """Return a version of the package.

    :returns: version
    :rtype: str
    """
    return __version__


# 1. Defines the default config as a package level variable.
CONFIG = configparser.ConfigParser()
# [DEFAULT]
# debug = False
# iaas_url = http://172.24.4.1
# iaas_project = demo
# iaas_user = demo
# iaas_password = password
# log_file = sys.stdout
# log_dir = logs
# log_format = %(asctime)-15s %(levelname)s %(name)s %(message)s
# log_level = logging.INFO
default_section = CONFIG['DEFAULT']
default_section['debug'] = "False"
default_section['iaas_url'] = "http://172.24.4.1"
default_section['iaas_project'] = "demo"
default_section['iaas_user'] = "demo"
default_section['iaas_password'] = "password"
default_section['log_file'] = "sys.stderr"
default_section['log_dir'] = "logs"
default_section['log_level'] = "logging.INFO"

# [k2hr3]
# api_url = "http://127.0.0.1:18080"
# api_version = "v1"
CONFIG['k2hr3'] = {}
k2hr3_section = CONFIG['k2hr3']
k2hr3_section['api_url'] = "http://127.0.0.1:18080"
k2hr3_section['api_version'] = "v1"

# [http]
# timeout_seconds = 30
# retry_interval_seconds = 60
# max_retries = 3
# allow_self_signed_cert = True
CONFIG['http'] = {}
http_section = CONFIG['http']
http_section['timeout_seconds'] = "30"
http_section['retry_interval_seconds'] = "60"
http_section['max_retries'] = "3"
http_section['allow_self_signed_cert'] = "True"

# 2. Overrides the default config by the config file.
# Find the config using precedence of the location:
#   ./k2hr3client.ini
#   ~/.k2hr3client.ini
#   /etc/antpickax/k2hr3client.ini
# NOTE:
# Using the configuration value may occur KeyError.
# All values are string. Use getboolean or something.
config_path = [Path("k2hr3client.ini"),
               Path(Path.home() / '.k2hr3client.ini'),
               Path('/etc/antpickax/k2hr3client.ini')]
for my_config in config_path:
    if my_config.is_file():
        # Override the value if the key is defined.
        CONFIG.read(my_config.absolute())
        break

#
# Local variables:
# tab-width: 4
# c-basic-offset: 4
# End:
# vim600: expandtab sw=4 ts=4 fdm=marker
# vim<600: expandtab sw=4 ts=4
#
