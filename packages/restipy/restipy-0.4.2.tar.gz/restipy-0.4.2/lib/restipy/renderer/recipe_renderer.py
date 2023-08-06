import yaml

from pkg_resources import iter_entry_points
from jinja2 import Environment, FileSystemLoader, Undefined, DebugUndefined

def silently(*args, **kwargs):
    return u''

return_new = lambda *args, **kwargs: SilentUndefined()

class SilentUndefined(Undefined):
    __unicode__ = silently
    __str__ = silently
    __call__ = return_new
    __getattr__ = return_new

class RecipeRenderer:
    def __init__(self, template_filename):
        jinja_env = Environment(
            loader=FileSystemLoader(''),
            undefined=SilentUndefined)

        jinja2_globals = {}
        for entry_point in iter_entry_points(group='restipy.plugins.jinja2.globals', name=None):
            jinja2_globals[entry_point.name] = entry_point.load()

        jinja_env.globals.update(jinja2_globals)

        jinja2_filters = {}
        for entry_point in iter_entry_points(group='restipy.plugins.jinja2.filters', name=None):
            jinja2_filters[entry_point.name] = entry_point.load()

        jinja_env.filters.update(jinja2_filters)

        self.template = jinja_env.get_template(template_filename)

    def render(self, params):
        recipe_str = self.template.render(params)
        # TODO add debug logging
        return yaml.load(recipe_str)
