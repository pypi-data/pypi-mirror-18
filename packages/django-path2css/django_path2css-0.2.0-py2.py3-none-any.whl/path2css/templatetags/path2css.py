# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from django import template
from django.contrib.staticfiles.finders import find as find_staticfile
from django.contrib.staticfiles.storage import staticfiles_storage

from path2css import request_path_to_css_names, Output, LinkOutput

register = template.Library()

@register.simple_tag(takes_context=False)
def path2css(path, prefix='', suffix='', midpoint='-'):
    variations = request_path_to_css_names(item=path, prefix=prefix, suffix=suffix,
                                           midpoint=midpoint)
    return Output(variations)



@register.simple_tag(takes_context=False)
def css4path(path, prefix='', suffix='', midpoint='-', directory='css'):
    variations = request_path_to_css_names(item=path, prefix=prefix, suffix=suffix,
                                           midpoint=midpoint)
    found_files = []
    for variation in variations:
        filename = os.path.join(directory, '{}.css'.format(variation))
        found = find_staticfile(path=filename)
        if found is not None:
            # import pdb; pdb.set_trace()
            found_file = staticfiles_storage.url(filename)
            found_files.append(found_file)
    return LinkOutput(found_files)
