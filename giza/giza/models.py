from persistent.mapping import PersistentMapping


class Context(PersistentMapping):
    __parent__ = __name__ = None

class Application(Context):
    pass

class Plugin(Context):
    pass

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Application()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
