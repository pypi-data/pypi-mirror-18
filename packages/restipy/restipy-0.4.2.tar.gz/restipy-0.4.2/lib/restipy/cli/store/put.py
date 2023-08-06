from restipy.core import LocalStore

def do(args):
    local_store = LocalStore(
        filename=args.save_filename,
        environment=args.environment)

    data = local_store.get_data()
    data[args.key] = args.value

    local_store.dump()
