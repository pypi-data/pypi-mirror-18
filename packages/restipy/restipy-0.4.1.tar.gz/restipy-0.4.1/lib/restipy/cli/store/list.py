import json

from restipy.core import LocalStore

def do(args):
    local_store = LocalStore(
        filename=args.save_filename,
        environment=args.environment)

    if args.pretty:
        print json.dumps(local_store.get_data(), indent=2)
    else:
        print json.dumps(local_store.get_data())
