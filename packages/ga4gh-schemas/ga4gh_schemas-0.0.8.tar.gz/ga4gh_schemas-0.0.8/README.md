# ga4gh-schemas
Temporary schemas python package repository

To generate new pb files from the schemas:
```
python scripts/process_schemas.py 0.6.0a8 ../schemas/
```

To generate an installable wheel:
```
rm dist/* && python setup.py bdist_wheel --universal
```
