The `craftr.loaders` module provides a few functions that can be used to
automatically download files from a URL and even unpack downloaded archives
into the build tree automatically.

If you're project provides some examples that depend on huge binary data,
you can download these files when necessary:

```python
from craftr.loaders import external_file

if options.build_examples:
  example_data = external_file("http://url.to/example/data.bin")
  # ... build examples here
```

Many build scripts for projects that are not usually built with Craftr
use the `external_archive()` function to download a source archive and
build from that.

```python
from craftr.loaders import external_archive

source_directory = external_archive(
  "https://curl.haxx.se/download/curl-{}.tar.gz".format(options.version)
)

# ...
```

## Functions

### `external_file(*urls, filename = None, directory = None, copy_file_urls = False, name = None)`

### `external_archive(*urls, directory = None, name = None)`

### `pkg_config(pkg_name)`

Uses `pkg-config` to read the flags for the library specified with *pkg_name*
and returns a Framework object. If `pkg-config` is not available on the platform
or the library can not be found, `pkg_config.Error` is raised.

```python
from craftr.loaders import pkg_config
try:
  cURL = pkg_config('libcurl')
except pkg_config.Error:
  # compile from source or whatever
```

  
