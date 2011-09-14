# coding: latin-1

"""
Leider noch nicht gut genug. Beispiel:

bezirk: Friedrichshain-Kreuzberg

Alle, die keinen Strkat-Eintrag haben, weil die Adressangabe nicht richtig stimmt, werden als ausserhalb
klassifiziert, obwohl aufgrund der PLZ vielleicht fast richtig entschieden werden könnt.


bezirk: Friedrichshain-Kreuzberg; plz: 1 2 3

data.bezirk = '', data.plz=2

Es muss ein anders Konzept her:

Das erste Kriterium, wofür data einen Wert aufweist, entscheidet. 
Wenn data keinen Wert für irgendein Kriterium hat, dann gilt "nicht außerhalb". 

Im Beispiel oben zählt also die plz. Wenn ein Bezirk dagewesen wäre, würde die plz gar
nicht betrachtet.

Man sollte also die genaueren Kriterien an den Anfang nehmen, zB die mit Daten aus
dem Straßenkatalog. Zum Schluss dann die plz, evt. Ort, wo das anwendbar ist (in Berlin 
definitiv nicht).


"""

import re

class obj(object):
    def __init__(self, **params):
        for p in params:
            setattr(self, p, params[p])

def _parse_config(spec_str):
    """Liefert Liste [['ort',['Wolfsburg']],['plz',['12345','54321']],...]
    so dass man mit 
    for feld, values in liste:
        do something
    durchgehen kann.
    Jede Inkorrektheit wird mit [] beantwortet.
    >>> _parse_config("ort:Braunschweig;Wolfsburg")
    [['ort', ['Braunschweig', 'Wolfsburg']]]
    >>>
    >>> _parse_config("ort:Braunschweig;Wolfsburg;samtgemeinde:")
    []
    >>>
    """
    def parse_one(elems):
        first, rest = elems[0], elems[1:]
        field, value = [el.strip() for el in first.split(':')]
        assert field and value
        values = [value]
        while rest and ':' not in rest[0]:
            first, rest = rest[0], rest[1:]
            values.append(first)
        return [field, values], rest
    elems = [elem for elem in [el.strip() for el in spec_str.split(';')] if elem]
    try:
        result = []
        rest = elems
        while rest:
            first, rest = parse_one(rest)
            result.append(first)
    except:
        result = []
    return result

def wohnt_ausserhalb(data, spec_str_oder_config):
    """Zum Testen: data ist dict mit Keys: plz,ort,ortsteil,samtgemeinde,bezirk,plraum
                   spec_str ist ein String wie z.B.
                   "ort:Wolfsburg;Braunschweig; plz:12345;54321; samtgemeinde:Oberhausen"
                   Rund um die Trenner ':' und ';' dürfen blanks sein.
                   
                   Oder es wird das config-Objekt übergeben. Dann muss es ein Attribut
                   "WOHNT_NICHT_AUSSERHALB" haben, dessen Wert spec_str ist.

    >>> spec = 'plz:12047'
    >>> data = dict(plz='12048',ort='',ortsteil='',samtgemeinde='',bezirk='',)
    >>> wohnt_ausserhalb(data, spec)
    False
    >>>
    >>> spec = 'plz:12047 ;   12049'
    >>> data = dict(plz='12048',ort='Berlin',ortsteil='',samtgemeinde='',bezirk='',)
    >>> wohnt_ausserhalb(data, spec)
    True
    >>>
    >>> spec = 'ort:Berlin;Klein Machnow;bezirk:Friedrichshain-Kreuzberg'
    >>> data = dict(plz='12048',ort='Berlin',ortsteil='',samtgemeinde='',bezirk='Friedrichshain-Kreuzberg',)
    >>> wohnt_ausserhalb(data, spec)
    False
    >>>
    >>> spec = 'ort:Berlin;Klein Machnow;bezirk:Friedrichshain-Kreuzberg'
    >>> data = dict(plz='12048',ort='Oberhausen',ortsteil='',samtgemeinde='',bezirk='Friedrichshain-Kreuzberg',)
    >>> wohnt_ausserhalb(data, spec)
    True
    >>>
    >>> spec = 'bezirk:Friedrichshain-Kreuzberg;ort:Berlin;Klein Machnow'
    >>> data = dict(plz='12048',ort='Oberhausen',ortsteil='',samtgemeinde='',bezirk='Friedrichshain-Kreuzberg',)
    >>> wohnt_ausserhalb(data, spec)
    False
    >>>
    >>> spec = 'bezirk:Friedrichshain-Kreuzberg;Treptow; ort:Berlin '
    >>> data = dict(plz='12048',ort='Berlin',ortsteil='',samtgemeinde='',bezirk='Treptowx',)
    >>> wohnt_ausserhalb(data, spec)
    True
    >>>
    >>> spec = 'ort:Braunschweig;Gifhorn;Wolfsburg'
    >>> data = dict(plz='12048',ort='Berlin',ortsteil='',samtgemeinde='',bezirk='Treptowx',)
    >>> wohnt_ausserhalb(data, spec)
    True
    >>>
    >>> spec = 'ort:Braunschweig;Gifhorn;Wolfsburg'
    >>> data = dict(plz='12048',ort='Berlin',ortsteil='',samtgemeinde='',bezirk='Treptowx',)
    >>> wohnt_ausserhalb(data, spec)
    True
    >>>
    >>> spec = 'ort: Braunschweig; Gifhorn;Wolfsburg '
    >>> data = dict(plz='12048',ort='Gifhorn',ortsteil='',samtgemeinde='',bezirk='Treptowx',)
    >>> wohnt_ausserhalb(data, spec)
    False
    >>>
    >>> spec = 'plraum:204,206;plz: 12048;12047 '
    >>> data = dict(plz='12048',ort='Gifhorn',ortsteil='',samtgemeinde='adfafa',bezirk='Treptowx',plraum='')
    >>> wohnt_ausserhalb(data, spec)
    False
    >>>
    >>> spec = 'plraum:204;206;plz: 12048;12047 '
    >>> data = dict(plz='12058',ort='Gifhorn',ortsteil='',samtgemeinde='adfafa',bezirk='Treptowx',plraum='206')
    >>> wohnt_ausserhalb(data, spec)
    False
    >>>
    >>> spec = 'plraum:204;206;plz: 12048;12047 '
    >>> data = dict(plz='12058',ort='Gifhorn',ortsteil='',samtgemeinde='adfafa',bezirk='Treptowx',plraum='207')
    >>> wohnt_ausserhalb(data, spec)
    True
    >>>
    """                
    try: spec_str = spec_str_oder_config.WOHNT_NICHT_AUSSERHALB
    except: spec_str = spec_str_oder_config
    felder = ('ort', 'plz', 'ortsteil','samtgemeinde','bezirk','plraum')
    if not re.match(r'^\d{5,5}$', data['plz']): # Nur korrekt geformte plz verwenden.
        data['plz'] = ''
    if not data['plz'] or not data['ort']: # Ohne korrekte plz und ort kann 'wohnt ausserhalb' nicht bestätigt werden.
        return False
    spec = _parse_config(spec_str)
    if not spec:
        return False
    for feld, values in spec:
        assert feld in felder
        assert values
        if data[feld]:
            return data[feld] not in values
    return False

if __name__ == "__main__":
    import doctest
    doctest.testmod()
