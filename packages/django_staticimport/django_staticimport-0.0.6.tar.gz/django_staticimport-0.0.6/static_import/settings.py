import os

try:
	from urllib.parse import urlparse
except ImportError:
	from urlparse import urlparse

from django.conf import settings as USER_SETTINGS
from django.core.exceptions import ImproperlyConfigured


HOSTED_LIBS = [
	{
		'name': 'angularjs',
		'url': 'https://ajax.googleapis.com/ajax/libs/angularjs/1.5.9/angular.min.js'
	},
	{
		'name': 'angular_material',
		'url': 'http://ajax.googleapis.com/ajax/libs/angular_material/1.1.1/angular-material.min.js'
	},
	{
		'name': 'angular_material_css',
		'url': 'http://ajax.googleapis.com/ajax/libs/angular_material/1.1.1/angular-material.min.css'
	},
	{
		'name': 'dojo',
		'url': 'https://ajax.googleapis.com/ajax/libs/dojo/1.11.2/dojo/dojo.js'
	},
	{
		'name': 'ext-core',
		'url': 'https://ajax.googleapis.com/ajax/libs/ext-core/3.1.0/ext-core.js'
	},
	{
		'name': 'hammerjs',
		'url': 'https://ajax.googleapis.com/ajax/libs/hammerjs/2.0.8/hammer.min.js'
	},
	{
		'name': 'jquery3',
		'url': 'https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js'
	},
	{
		'name': 'jquery2',
		'url': 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
	},
	{
		'name': 'jquery1',
		'url': 'https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'
	},
	{
		'name': 'jquerymobile_js',
		'url': 'https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.js'
	},
	{
		'name': 'jquerymobile_css',
		'url': 'https://ajax.googleapis.com/ajax/libs/jquerymobile/1.4.5/jquery.mobile.min.css'
	},
	{
		'name': 'jqueryui_js',
		'url': 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js'
	},
	{
		'name': 'jqueryui_css',
		'url': 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css'
	},
	{
		'name': 'mootools',
		'url': 'https://ajax.googleapis.com/ajax/libs/mootools/1.6.0/mootools.min.js'
	},
	{
		'name': 'prototype',
		'url': 'https://ajax.googleapis.com/ajax/libs/prototype/1.7.3.0/prototype.js'
	},
	{
		'name': 'scriptaculous',
		'url': 'https://ajax.googleapis.com/ajax/libs/scriptaculous/1.9.0/scriptaculous.js'
	},
	{
		'name': 'spf',
		'url': 'https://ajax.googleapis.com/ajax/libs/spf/2.4.0/spf.js'
	},
	{
		'name': 'swfobject',
		'url': 'https://ajax.googleapis.com/ajax/libs/swfobject/2.2/swfobject.js'
	},
	{
		'name': 'threejs',
		'url': 'https://ajax.googleapis.com/ajax/libs/threejs/r76/three.min.js'
	},
	{
		'name': 'webfont',
		'url': 'https://ajax.googleapis.com/ajax/libs/webfont/1.6.16/webfont.js'
	},
	{
		'name': 'react',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/react/15.4.1/react.min.js'
	},
	{
		'name': 'react-dom-server',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/react/15.4.1/react-dom-server.min.js'
	},
	{
		'name': 'react-dom',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/react/15.4.1/react-dom.min.js'
	},
	{
		'name': 'react-with-addons',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/react/15.4.1/react-with-addons.min.js'
	},
	{
		'name': 'materialize_js',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/js/materialize.min.js'
	},
	{
		'name': 'materialize_css',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/css/materialize.min.css'
	},
	{
		'name': 'bootstrap_js',
		'url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'
	},
	{
		'name': 'bootstrap_css',
		'url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'
	},
	{
		'name': 'bootstrap_css_theme',
		'url': 'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css'
	},
	{
		'name': 'bulma',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.2.3/css/bulma.min.css'
	},
	{
        'name': 'metro-UI-css',
        'url': 'https://cdn.rawgit.com/olton/Metro-UI-CSS/master/build/css/metro.min.css'
    },
    {
    	'name': 'metro-UI-responsive-css',
    	'url': 'https://cdn.rawgit.com/olton/Metro-UI-CSS/master/build/css/metro-responsive.min.css'
    },
	{
		'name': 'metro-UI-schemes-css',
		'url': 'https://cdn.rawgit.com/olton/Metro-UI-CSS/master/build/css/metro-schemes.min.css'
	},
	{
		'name': 'metro-UI-rtl-css',
		'url': 'https://cdn.rawgit.com/olton/Metro-UI-CSS/master/build/css/metro-rtl.min.css'
	},
	{
		'name': 'metro-UI-icons-css',
		'url': 'https://cdn.rawgit.com/olton/Metro-UI-CSS/master/build/css/metro-icons.min.css'
	},
	{
		'name': 'metro-UI-js',
		'url': 'https://cdn.rawgit.com/olton/Metro-UI-CSS/master/build/js/metro.min.js'
	},
	{
		'name': 'font-awesome',
		'url': 'https://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css'
	},
	{
		'name': 'select2_css',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css'
	},
	{
		'name': 'select2_js',
		'url': 'https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.min.js'
	},
]


def is_valid_url(url):
	"""
	Will test if is a valid url
	"""
	purl = urlparse(url)
	if len(purl.scheme) and \
	   len(purl.netloc) and \
	   len(purl.path):
		return True
	return False


def check_user_hosted_libs(libs):
	"""
	Will test if every lib, at user HOSTED_LIBS,
	is correct, otherwise, will raise a ImproperlyConfigured error.
	
	errors:
		- user set a local staticfile into HOSTED_LIBS
		- user set an invalid or non-existent static file
	"""
	for lib in libs:
		if os.path.exists(lib['url']):
			raise ImproperlyConfigured(\
				"Try not to use local static files at HOSTED_LIBS,"
				" instead use STATICFILES_DIRS")

		if not is_valid_url(lib['url']):
			raise ImproperlyConfigured("Try not to use an invalid url")


def get_config():
	"""
	Return default config plus user config.
	"""
	user_hosted_libs = getattr(USER_SETTINGS, 'HOSTED_LIBS', [])
	check_user_hosted_libs(user_hosted_libs)
	if isinstance(user_hosted_libs, (list, tuple)):
		HOSTED_LIBS.extend(user_hosted_libs)
	else:
		raise ImproperlyConfigured('Libs should be a list of tuple.')
	return HOSTED_LIBS

