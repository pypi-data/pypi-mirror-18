from datapackage_pipelines.wrapper import ingest, spew

params, datapackage, res_iter = ingest()

splits = params['splits']

for resource in datapackage['resources']:
    fields = resource.get('schema', {}).get('fields')
    if fields is not None:
        new_fields = []
        for field in fields:
            if field['name'] in splits.keys():
                new_columns = splits[field['name']]['columns']
                for column in new_columns:
                    new_fields.append({
                        'name': column,
                        ''
                    })
        fields = [
            field for field in fields
            if field['name'] not in columns
        ]
        resource['schema']['fields'] = fields


def process_resources(_res_iter):
    for rows in _res_iter:
        def process_rows(_rows):
            for row in _rows:
                for column in columns:
                    if column in row:
                        del row[column]
                yield row
        yield process_rows(rows)

spew(datapackage, process_resources(res_iter))
