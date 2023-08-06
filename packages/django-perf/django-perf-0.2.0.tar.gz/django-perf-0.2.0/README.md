[![PyPI version](https://badge.fury.io/py/django-perf.svg)](https://badge.fury.io/py/django-perf) [![circle.ci builds](https://circleci.com/gh/perflabs/django-perf/tree/master.svg?style=shield&circle-token=21f056185e48e4d08cc62909f972ae235affacd8)](https://circleci.com/gh/perflabs/django-perf)

# Perf Django Agent

`perf` is a middleware that will record timing and status codes of the connections in the Django framework and send the data to Perf. We then run analytics on that data to generate metrics and alerts.

## Installation

* Easily install Perf via pip

  ```bash
  pip install django-perf
  ```

* Add Perf configuration to your settings

  ```python
  PERF_CONFIG = {
      "api_key": "PERF_API_KEY"
  }
  ```

* Add Perf to your list of installed apps and middleware classes

  ```python
  INSTALLED_APPS = (
    'perf',
    ...
  )

  MIDDLEWARE_CLASSES = (
    'perf.middleware.PerfMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
  )
  ```
