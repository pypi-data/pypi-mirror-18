====

    $ pip install git+https://github.com/jpwagner/django-filepicker-model.git

====

The following settings:

```python
FILEPICKER_API_KEY = 'AaBbCcZZ'
FILEPICKER_APP_SECRET = 'XYZ123'
FILEPICKER_EXPIRES_IN_SECONDS = 60*60 # optional 1 hr is default
```
====

depends on:

django, requests, filepicker

====

usage:

```python
INSTALLED_APPS = [
...
'django_filepicker_model',
...
]
```


```python
from django_filepicker_model.models import FilepickerField, FilepickerModel

class MyModel(FilePickerModel):
	myFile = FilePickerField()
```
====
