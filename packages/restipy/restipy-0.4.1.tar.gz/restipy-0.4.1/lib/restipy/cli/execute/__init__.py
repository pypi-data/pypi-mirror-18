from parse_data import parse_data
from restipy.core import LocalStore
from restipy.core.execution import CookbookExecutor
from pkg_resources import load_entry_point

def do(args):
    input_data = {}
    local_store = LocalStore(
        filename=args.save_filename,
        environment=args.environment)

    input_data = local_store.get_data()

    cli_input_data = parse_data(args.data)
    input_data.update(cli_input_data)

    cookbook_executor = CookbookExecutor(args)

    result_generator = cookbook_executor.execute(
        cookbook_file=args.cookbook_file,
        input_data=input_data)

    list(result_generator)
