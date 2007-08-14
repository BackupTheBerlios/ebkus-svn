# coding: latin-1

#äöü

from ebkus.app.ebapih import get_codes, make_option_list


class OptionMixin(object):
    """Klasse zur Generierung von Option-Listen

    Wird der Request-Klasse als Attribut gegeben, so dass auf session, user, etc
    zugegriffen werden kann.
    
    """
##     _options = {
##         'wohntbei': 'fsfs',

##         }
    def __init__(self, request):
        self.request = request
    def __getattr__(self, attr):
        kat = self._options.get(attr)
        if kat:
            return self.get_kategorie_options
        else:
            raise AttributeError()

    
    def for_mitarbeiter(self, sel=None):
        return make_option_list(self.request.getMitarbeiterliste(),
                                'id', 'na',
                                selected=sel)

##     def wohntbei_options(self, selected):
##         return  make_option_list(get_codes('fsfs'),
##                                  'id', 'name',
##                                  selected)

    def for_kat(self, kat, sel=None):
        return  make_option_list(get_codes(kat),
                                 'id', 'name',
                                 selected=sel)

    
