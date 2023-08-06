from restipy.renderer import RecipeRenderer
from restipy.core.components import SaveComponent
from models import ExecutionResult

from pkg_resources import iter_entry_points

core_component_keys = ['id', 'name', 'save']

class CookbookExecutor:
    def __init__(self, args):
        self.saveComponent = SaveComponent(args)

        self.modules = {}
        for entry_point in iter_entry_points(group='restipy.plugins.modules', name=None):
            Executor = entry_point.load()
            self.modules[entry_point.name] = Executor(args)

    def execute(self, cookbook_file, input_data):
        recipe_renderer = RecipeRenderer(cookbook_file)

        index = 0
        while True:
            recipes = self.render_recipes(recipe_renderer, input_data)

            if index >= len(recipes):
                break

            recipe = recipes[index]

            if not ('id' in recipe):
                raise Exception('Each recipe must have an ID')

            id = recipe['id']

            if 'name' in recipe:
                name = recipe['name']
            else:
                name = index

            components = {
                key: component
                for key, component in recipe.items()
                if not (key in core_component_keys)
            }

            if len(components) > 1:
                raise Exception('More than one module found for recipe.', components.keys())
            elif len(components) == 0:
                raise Exception('No modules found for recipe.')

            module_name, module_params = components.items()[0]

            if not (module_name in self.modules):
                raise Exception('No module found for "{}"'.format(module_name))

            module = self.modules[module_name]
            output = module.execute(
                recipe=recipe,
                module_params=module_params)

            result = ExecutionResult(
                recipe=recipe,
                output=output,
                data=input_data
            )

            self.saveComponent.process(
                recipe=recipe,
                result=result,
                input_data=input_data)

            yield result
            index += 1

    def render_recipes(self, recipe_renderer, input_data):
        cookbook = recipe_renderer.render(input_data)
        recipes = cookbook['recipes']
        return recipes
