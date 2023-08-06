import os
from logging import getLogger

from pylons import request
from genshi.input import HTML
from genshi.filters.transform import Transformer

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckan.plugins import IGenshiStreamFilter
from ckan.plugins import IRoutes
from ckan.plugins import ITemplateHelpers

log = getLogger(__name__)



def smartstreets_base_url():
    return 'http://hub.urbanopus.net'

def logout_all_url():
    return '#'

def wotkit_url():
    return 'http://hub.urbanopus.net/wotkit'

def url_for(c, a, i):
    return '#'

class UrbanOpusThemePlugin(SingletonPlugin):
    """This plugin demonstrates how a theme packaged as a CKAN
    extension might extend CKAN behaviour.

    In this case, we implement three extension interfaces:

      - ``IConfigurer`` allows us to override configuration normally
        found in the ``ini``-file.  Here we use it to specify the site
        title, and to tell CKAN to look in this package for templates
        and resources that customise the core look and feel.

      - ``IRoutes`` allows us to add new URLs, or override existing
        URLs.  In this example we use it to override the default
        ``/register`` behaviour with a custom controller
    """
    implements(IConfigurer, inherit=True)
    implements(IRoutes, inherit=True)
    implements(ITemplateHelpers)

    def update_config(self, config):
        """This IConfigurer implementation causes CKAN to look in the
        ```public``` and ```templates``` directories present in this
        package for any customisations.

        It also shows how to set the site title here (rather than in
        the main site .ini file), and causes CKAN to use the
        customised package form defined in ``package_form.py`` in this
        directory.
        """
        log.debug("Initializing Urban Opus Theme")

        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))
        our_public_dir = os.path.join(rootdir, 'ckanext',
                                      'themeUrbanOpus', 'theme', 'public')
        template_dir = os.path.join(rootdir, 'ckanext',
                                    'themeUrbanOpus', 'theme', 'templates')
        # set our local template and resource overrides
        config['extra_public_paths'] = ','.join([our_public_dir,
                config.get('extra_public_paths', '')])
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])

        config['ckan.template_head_end'] = config.get('ckan.template_head_end', '')
        
        # set the title
        config['ckan.site_title'] = "Urban Opus Datahub"
        # set the customised package form (see ``setup.py`` for entry point)
        config['package_form'] = "example_form"


    def get_helpers(self):
        '''Register the most_popular_groups() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'smartstreets_base_url': smartstreets_base_url,
            'logout_all_url': logout_all_url,
            'wotkit_url': wotkit_url
            # 'url_for': url_for
        }

