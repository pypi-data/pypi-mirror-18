import os
import csv
import logging

import itertools
import requests
import tabulator

from jsontableschema import Schema

from datapackage_pipelines.wrapper import ingest, spew


def _reader(opener, _url):
    yield None
    filename = os.path.basename(_url)
    _schema, _headers, _reader = opener()
    num_headers = len(_headers)
    i = 0
    for i, row in enumerate(_reader):

        row = [x.strip() for x in row]
        values = set(row)
        if len(values) == 1 and '' in values:
            # In case of empty rows, just skip them
            continue
        output = dict(zip(_headers, _schema.cast_row(row[:num_headers])))
        yield output

        i += 1
        if i % 10000 == 0:
            logging.info('%s: %d rows', filename, i)
            # break

    logging.info('%s: TOTAL %d rows', filename, i)


def dedupe(headers):
    _dedupped_headers = []
    for hdr in headers:
        if len(hdr.strip()) == 0:
            continue
        if hdr in _dedupped_headers:
            i = 0
            deduped_hdr = hdr
            while deduped_hdr in _dedupped_headers:
                i += 1
                deduped_hdr = '%s_%s' % (hdr, i)
            hdr = deduped_hdr
        _dedupped_headers.append(hdr)
    return _dedupped_headers


def stream_reader(_resource, _url, _encoding=None):
    def get_opener(__url, __encoding):
        def opener():
            _stream = tabulator.Stream(__url, headers=1, encoding=__encoding)
            _stream.open()
            _headers = dedupe(_stream.headers)
            _schema = _resource.get('schema')
            if _schema is not None:
                _schema = Schema(_schema)
            return _schema, _headers, _stream
        return opener

    schema, headers, stream = get_opener(url, _encoding)()
    if schema is None:
        schema = {
            'fields': [
                {'name': header, 'type': 'string'}
                for header in headers
                ]
        }
        _resource['schema'] = schema

    stream.close()
    del stream

    return itertools\
        .islice(
            _reader(
                get_opener(_url, _encoding),
                _url),
            1, None)


params, datapackage, res_iter = ingest()

new_resource_iterators = []
for resource in datapackage['resources']:
    if 'path' in resource:
        new_resource_iterators.append(next(res_iter))
    elif 'url' in resource:
        url = resource['url']
        basename = os.path.basename(resource['url'])
        path = os.path.join('data', basename)
        del resource['url']
        resource['path'] = path
        encoding = resource.get('encoding')
        rows = stream_reader(resource, url, encoding)
        new_resource_iterators.append(rows)

spew(datapackage, new_resource_iterators)
