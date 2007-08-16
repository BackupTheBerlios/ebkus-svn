# coding: latin-1

#äöü

from ebkus.app.ebapih import get_codes, make_option_list


class options(object):
    """Klasse zur Generierung von Option-Listen
    """
    def for_mitarbeiter(self, sel=None):
        return make_option_list(self.getMitarbeiterliste(),
                                'id', 'na',
                                selected=sel)

    def for_kat(self, kat, sel=None):
        if sel in ('', ' ',):
            empty_option = True
        else:
            empty_option = False
        # das ist ein hack. Eigentlich müsste ein multi-kat Feld eine List von Integern liefern.
        # Ist aber ein String von Zahlen, zB "233 44 444"
        if isinstance(sel, basestring):
            sel = [int(x) for x in sel.split()]
        return  make_option_list(get_codes(kat),
                                 'id', 'name',
                                 selected=sel,
                                 empty_option=empty_option)

    
