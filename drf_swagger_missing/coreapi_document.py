import coreapi


class BetterDocument(coreapi.Document):
    _base_path = ''
    _definitions = []
    _version = ''

coreapi.Document = BetterDocument