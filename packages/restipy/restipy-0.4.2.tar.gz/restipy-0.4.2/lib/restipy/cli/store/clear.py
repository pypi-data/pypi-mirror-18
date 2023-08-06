from restipy.core import LocalStore

def do(args):
    local_store = LocalStore(
        filename=args.save_filename,
        environment=args.environment)

    local_store.set_data({})
    local_store.dump()
