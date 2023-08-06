import json

from flask import current_app

exporters = {}


def exporter(mediatype):
    """
    Decorater for register exporter

    Args:
        mediatype: mediatype, eg: `application/json`
    """
    def wraper(fn):
        register_exporter(mediatype, fn)
        return fn
    return wraper


def register_exporter(mediatype, fn):
    """
    Register exporter

    Args:
        mediatype: mediatype, eg: `application/json`
        fn: exporter function
    """
    exporters[mediatype] = fn


@exporter('application/json')
def export_json(data, status, headers):
    """
    Creates a JSON response

    JSON content is encoded by utf-8, not unicode escape.

    Args:
        data: any type object that can dump to json
        status (int): http status code
        headers (dict): http headers
    """
    dumped = json.dumps(data, ensure_ascii=False)
    resp = current_app.response_class(
        dumped, status=status, headers=headers,
        content_type='application/json; charset=utf-8')
    return resp
