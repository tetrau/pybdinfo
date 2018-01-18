# pybdinfo
Get media info from bluray with pure python (using ctypes). Since ffmpeg and
mediainfo can't gather some information like languages of subtitle stream or
audio stream.

## Requirement
`pybdinfo` requires `libbluray` to analyze bluray structure.

Install `libbluray` on Debian-based linux distribution.
```shell
sudo apt install libbluray-dev
```

## Usage
```python
from pybdinfo import get_bdinfo

print(get_bdinfo('/path/to/bluray'))
# {'video':[{'coding_type': ...,
#            'format': ...,
#            'rate': ...,
#            'aspect': ...}, ...],
#  'audio':[{'coding_type': ...,
#            'rate': ...,
#            'format': ...,
#            'lang': ...}, ...],
#  'subtitle':[{'coding_type': ...,
#               'lang': ...}, ...]}
```
