from collections import OrderedDict

import coreapi


class BetterDocument(coreapi.Document):
    _base_path = ''
    _definitions = OrderedDict()
    _version = ''

coreapi.Document = BetterDocument