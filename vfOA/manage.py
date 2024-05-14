#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:test
# datetime:2023-4-8
# software: PyCharm


import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
