# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Release logic:
 1. Remove ".devX" from __version__ (below)
 2. git add blogit/__init__.py
 3. git commit -m 'Bump to <version>'
 4. git tag v<version>
 5. git push && git push --tags
 6. python setup.py sdist
 7. twine upload dist/djangocms-blogit-<version>.tar.gz
 8. bump the __version__, append ".dev0"
 9. git add blogit/__init__.py
10. git commit -m 'Start with <version>'
11. git push
"""
__version__ = '0.4.9'

default_app_config = 'blogit.apps.BlogitConfig'
