# Perf Django Agent

`perf_agent` is a middleware that will record timing and status codes of the connections in the Django framework and send the data to Perf. We then run analytics on that data to generate metrics and alerts.

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

* Add Perf to your list of Middleware classes

  ```python
  MIDDLEWARE_CLASSES = (
    'perf.middleware.PerfMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
  )
  ```
