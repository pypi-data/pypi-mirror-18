"""
Provides the main structure of a yacms site with a hierarchical tree
of pages, each subclassing the Page model to create a content structure.
"""
from __future__ import unicode_literals

from yacms import __version__  # noqa


default_app_config = 'yacms.pages.apps.PagesConfig'
