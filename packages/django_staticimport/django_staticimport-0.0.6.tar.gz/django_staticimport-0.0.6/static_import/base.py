import re
import os
import copy
import itertools

from django.contrib.staticfiles.finders import get_finders
from django.core.exceptions import ImproperlyConfigured
from django.utils.lru_cache import lru_cache

from static_import.settings import get_config


equal = lambda o, o2: o == o2
basename = lambda p: os.path.basename(p)

REMOTE = 'remote'
LOCAL = 'local'
is_remote = lambda o: equal(o, REMOTE)
is_local = lambda o: equal(o, LOCAL)

is_css = lambda name: bool(re.match(r'.*\.(css|min\.css)$', name))
is_js = lambda name: bool(re.match(r'.*\.(js|min\.js)$', name))
is_img = lambda name: bool(re.match(r'.*\.(jpg|jpeg|png|tif|gif)$', name))


global_attrs = [
    'accesskey', 'class', 'contenteditable',
    'contextmenu', 'dir', 'draggable', 'dropzone',
    'hidden', 'id', 'lang', 'spellcheck', 'style',
    'tabindex', 'title', 'translate'
]

img_attrs = [
    'align', 'alt', 'border', 'crossorigin', 
    'height', 'hspace', 'ismap', 'longdesc', 
    'src', 'usemap', 'vspace', 'width'
]

script_attrs = [
    'async', 'charset', 'defer', 'src', 'type'
]

style_attrs = [
    'media', 'scoped', 'type'
]

tags = {
    'style': list(itertools.chain(style_attrs, global_attrs)),
    'script': list(itertools.chain(script_attrs, global_attrs)),
    'img': list(itertools.chain(img_attrs, global_attrs))
}

attrs_regx = re.compile(r'(?:(\w+|\w+-\w+)(?==\".*\"|\s+|\s*$))')


def guess_tag(fn):
    """
    Return a specific tag, depending on fn(filename)
    """
    if is_css(fn):
        return 'style'
    elif is_js(fn):
        return 'script'
    else:
        return 'img'


def parse_attrs(attrs):
    r = "attrs=' "
    for k, v in attrs.items():
        r += k + '="' + v + '"'
    r += " '"
    return r


def validate_attrs(attrs, type):
    """
    Validate all attributes that the user want to use in the template.

    example:
        
        correct!
        {% import 'main.js' id='data' attrs='data-js="first_js"'"%}

        bad!
        {% import 'main.js' id='data' data-js='first_js' "%}

        bad!
        {% import 'main.js' id='data' attrs='height="300px"' "%}
    """
    str_attrs = ""
    attrs = copy.deepcopy(attrs)

    if attrs.get('css', None):
        del attrs['css']

    if attrs.get('id', None):
        del attrs['id']

    if attrs.get('style', None):
        del attrs['style'] 

    if attrs.get('attrs', None):
        str_attrs = attrs['attrs']
        del attrs['attrs']

    # if attrs is not empty, user try to add extra attributes.
    if len(attrs):
        raise ImproperlyConfigured("Wrong way to declare extra attributes, try %s" % parse_attrs(attrs))

    # putting into a list, all attribute names.
    _attrs = [attr for attr in attrs_regx.split(str_attrs) \
              if not attr.startswith("=") and len(attr) \
              and not attr.isspace() and not attr.startswith("data-")]

    for attr in _attrs:
        if attr not in tags[type]:
            raise ImproperlyConfigured("Tag <%s> does not support html attribute \"%s\"" % (type, attr))
    
    return True


def get_libs():
    """
    Yield all libs from config, if lib url or name, have not been set,
    an error is raised.
    """
    libs = get_config()
    for lib in libs:
        try:
            lib['name']
            lib['url']
        except KeyError as e:
            raise ImproperlyConfigured("Library %s have not been set." % e)
        
        yield lib


@lru_cache(maxsize=None)
def get_static_file(name):
    """
    Return staticfile path and if is a local or remote path, otherwise
    an error is raised.
    """
    for finder in get_finders():
        for path, _ in finder.list('none'):
            if equal(path, name) or \
               equal(basename(path), name):
                return path, LOCAL

    for lib in get_libs():
        remote_lib_name = lib['name']
        remote_lib_location = lib['url']

        if equal(remote_lib_name, name):
            return remote_lib_location, REMOTE

    raise FileNotFoundError('File %s does not exists' % name)
