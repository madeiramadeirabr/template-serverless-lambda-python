"""
Filter Helper Module for Flambda APP
Version: 1.0.0
"""
import re

from flambda_app import helper


def filter_sql_injection(value):
    check_value = str(value).replace('-', '')
    pattern = '(select|insert|drop|update|replace|create|delete|from|where)'
    if re.search(pattern, check_value, re.I):
        value = None
    if str(value).find('--') > -1:
        value = None
    return value


def filter_xss_injection(value):
    check_value = str(value).replace('-', '')
    pattern = '<(\w+)(/)?>'
    if re.search(pattern, check_value, re.I):
        value = None
    return value


def filter_fields(fields):
    filtered = None
    if isinstance(fields, list):
        filtered = []
        for v in fields:
            if v == '*':
                pass
            else:
                filtered_value = filter_sql_injection(v)
                filtered_value = filter_xss_injection(filtered_value)
                if not helper.empty(filtered_value):
                    filtered_value = filtered_value.strip()
                    filtered.append(filtered_value)
        if len(filtered) == 0:
            filtered = None
    return filtered
