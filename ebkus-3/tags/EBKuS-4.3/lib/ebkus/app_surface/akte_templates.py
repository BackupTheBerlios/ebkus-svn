# coding: latin-1
##*************************************************************************
##
## Formular: Akte neu anlegen
##
##*************************************************************************

from ebkus.config import config

class empty(object):
    def __init__(self, **kw):
        self.data = kw
    def __getitem__(self, name):
        try:
            return self.data[name]
        except:
            return ''
            
            # klientendaten_t und anschrift_t wird jetzt ueberall benutzt:
            # akteneu, akteupd, wiederauf, personneu, personupd
klientendaten_t = \
"""              <fieldset><legend class="legendtext">%(legend)s</legend>
              <table width="90%%" border="0" cellpadding="1" height="200">
                <tr>
                  <td width="37%%" align="right"><span class="labeltext">Vorname:</span></td>
                  <td width="63%%" align="left">
                     <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left" colspan=2>
                    <input type="text" size=14 maxlength=35 value="%(vn)s" name="vn" class="textbox" onMouseOver="window.status='Vorname %(bezug_genitiv)s';return true;" onMouseOut="window.status='';return true;" title="Vorname %(bezug_genitiv)s">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle"> <span class="labeltext">Nachname:</span></td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=35 value="%(na)s" name="na" class="textbox" onMouseOver="window.status='Nachname %(bezug_genitiv)s';return true;" onMouseOut="window.status='';return true;" title="Nachname %(bezug_genitiv)s">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Geburtstag:</td>
                  <td align="left" valign="middle" class="labeltext">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=10 value="%(gb)s" name="gb" class="textbox" onBlur="PruefeDatum(gb,1910,2060)" onMouseOver="window.status='Bitte den Geburtstag in der Form (TT.MM.JJJJ) eingeben.';return true;" onMouseOut="window.status='';return true;" title="Bitte den Geburtstag in der Form (TT.MM.JJJJ) eingeben." alt"Bitte den Geburtstag in der Form (TT.MM.JJJJ) eingeben.">
                    </td>
                    </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Telefon
                    1:</td>
                  <td align="left" valign="middle" class="labeltext">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=25 value="%(tl1)s" name="tl1" class="textbox">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Telefon
                    2:</td>
                  <td align="left" valign="middle" class="labeltext">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=25 value="%(tl2)s" name="tl2" class="textbox">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Ausbildung:</td>
                  <td align="left" valign="middle" class="labeltext">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=30 value="%(ber)s" name="ber" class="textbox" onMouseOver="window.status='Bitte die Ausbildung %(bezug_genitiv)s angeben';return true;" onMouseOut="window.status='';return true;" title="Bitte die Ausbildung %(bezug_genitiv)s angeben">
                    </td>
                    </tr>
                    </table>
                  </td>
                </tr>
              </table>
              </fieldset>
"""


anschrift_berlin_t = \
"""              <fieldset><legend class="legendtext">Anschrift</legend>
              <table border="0" cellpadding="1" width="311" height="200">
                <tr>
                  <td align="right" class="labeltext"> <span class="labeltext">Stra&szlig;e
                    in Berlin:</span></td>
                  <td align="left" valign="middle">
                  <table border="0" cellpadding="0" width="201" height="12">
                    <tr valign="middle" height="12">
                      <td>
                    <input type="text" size=14 name="strkat" value="%(str_inner)s" maxlength=35 class="textbox" onMouseOver="window.status='Wohnt %(bezug_nominativ)s innerhalb von Berlin bitte die Stra&szlig;e hier eingeben';return true;" onMouseOut="window.status='';return true;" title="Wohnt %(bezug_nominativ)s innerhalb von Berlin bitte die Stra&szlig;e hier eingeben">
                    </td>
                    <td align="center">
                    <a href=javascript:view_strkat() onMouseOver="window.status='Dr&uuml;cken Sie hier um die Stra&szlig;ensuche zu starten';return true;" onMouseOut="window.status='';return true;" title="Dr&uuml;cken Sie hier um die Stra&szlig;ensuche zu starten"><img border="0" src="/ebkus/ebkus_icons/strkatview_button.jpg"></a>
                    </td>
                  </tr>
                 </table>
                 </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">
                    <span class="labeltext">Au&szlig;erhalb:</span></td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=35 value="%(str_ausser)s" name="str" class="textbox" onMouseOver="window.status='Wohnt %(bezug_nominativ)s au&szlig;erhalb von Berlin bitte die Stra&szlig;e hier eingeben';return true;" onMouseOut="window.status='';return true;" title="Wohnt %(bezug_nominativ)s au&szlig;erhalb von Berlin bitte die Stra&szlig;e hier eingeben">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Hausnummer:</td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=5 maxlength=5 value="%(hsnr)s" name="hsnr" class="textboxmid" onMouseOver="window.status='Hausnummer';return true;" onMouseOut="window.status='';return true;" title="Hausnummer" onBlur="strkat_hausnr('akteform','hsnr');">
                    </td>
                    </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Postleitzahl:</td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=5 maxlength=9 value="%(plz)s" name="plz" class="textboxmid" onMouseOver="window.status='Postleitzahl';return true;" onMouseOut="window.status='';return true;" title="Postleitzahl">
                    </td>
                    </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Ort:</td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=35 value="%(ort)s" name="ort" class="textbox" onMouseOver="window.status='Wohnort';return true;" onMouseOut="window.status='';return true;" title="Wohnort">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">
                    <p>Wohnt bei:</p>
                  </td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <select name="fs" width=20 height=12 class="listbox130" onMouseOver="window.status='Hier k&ouml;nnen Sie eingeben bei wem %(bezug_nominativ)s lebt';return true;" onMouseOut="window.status='';return true;" title="Hier k&ouml;nnen Sie eingeben bei wem %(bezug_nominativ)s lebt">
"""

_leerfeld_t = \
"""                <tr>
                  <td align="right" valign="middle" class="labeltext"></td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
"""

_planungsraum_t = \
"""                <tr>
                  <td align="right" valign="middle" class="labeltext">Planungsraum:</td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=35 value="%(planungsr)s" name="planungsr" class="textbox" onMouseOver="window.status='Der Planungsraum des Klienten';return true;" onMouseOut="window.status='';return true;" title="Der Planungsraum des Klienten">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
"""

_anschrift_allgemein_t1 = \
"""              <fieldset><legend class="legendtext">Anschrift</legend>
              <table border="0" cellpadding="1" width="311" height="200">
                <tr>
                  <td align="right" valign="middle" class="labeltext">
                    <span class="labeltext">Stra&szlig;e:</span></td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=35 value="%(str)s" name="str" class="textbox" onMouseOver="window.status='Stra&szlig;e';return true;" onMouseOut="window.status='';return true;" title="Stra&szlig;e">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Hausnummer:</td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=5 maxlength=5 value="%(hsnr)s" name="hsnr" class="textboxmid" onMouseOver="window.status='Hausnummer';return true;" onMouseOut="window.status='';return true;" title="Hausnummer" onBlur="strkat_hausnr('akteform','hsnr');">
                    </td>
                    </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Postleitzahl:</td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=5 maxlength=9 value="%(plz)s" name="plz" class="textboxmid" onMouseOver="window.status='Postleitzahl';return true;" onMouseOut="window.status='';return true;" title="Postleitzahl">
                    </td>
                    </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Ort:</td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <input type="text" size=14 maxlength=35 value="%(ort)s" name="ort" class="textbox" onMouseOver="window.status='Wohnort';return true;" onMouseOut="window.status='';return true;" title="Wohnort">
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
"""

_anschrift_allgemein_t2 = \
"""                <tr>
                  <td align="right" valign="middle" class="labeltext">
                    <p>Wohnt bei:</p>
                  </td>
                  <td align="left" valign="middle">
                    <table border="0" cellpadding="0" width="201" height="12">
                     <tr>
                     <td align="left">
                    <select name="fs" width=20 height=12 class="listbox130" onMouseOver="window.status='Hier k&ouml;nnen Sie eingeben bei wem %(bezug_nominativ)s lebt';return true;" onMouseOut="window.status='';return true;" title="Hier k&ouml;nnen Sie eingeben bei wem %(bezug_nominativ)s lebt">
"""


if config.BERLINER_VERSION:
    anschrift_akte_t = anschrift_bezugsperson_t = anschrift_berlin_t
else:
    anschrift_akte_t = _anschrift_allgemein_t1 + _planungsraum_t + _anschrift_allgemein_t2
    anschrift_bezugsperson_t = _anschrift_allgemein_t1 + _leerfeld_t + _anschrift_allgemein_t2
    
akte_neu_t1 = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.akteform.vn.focus()">
<table width="735" align="center">
 <tr>
    <td height="465" align="center" valign="top">
      <form name="akteform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="200">
""" + (klientendaten_t % empty(legend='Klientendaten', bezug_nominativ='der Klient', bezug_genitiv='des Klienten')) + \
"""            </td>
            <td valign="top" align="center" class="legendtext" width="55%%" height="200">
""" + (anschrift_akte_t % empty(bezug_nominativ='der Klient', bezug_genitiv='des Klienten'))

akte_neu_t3 = """
                    </select>
                     </td>
                     </tr>
                     </table>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset><legend>Notiz</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="85%%" align="center" height="35" valign="middle">
                    <input type="text" size=50 maxlength=255 name="no" onMouseOver="window.status='Hier k&ouml;nnen Sie einen Notiztext zum Klienten eingeben';return true;" onMouseOut="window.status='';return true;" title="Hier k&ouml;nnen Sie einen Notiztext zum Klienten eingeben">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2" height="63">
              <fieldset><legend>Falldaten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr valign="middle">
                  <td align="right" class="labeltext" width="11%%" height="42">Bearbeiter:</td>
                  <td width="43%%" height="42">
                    <select width=20 name="zumitid" class="listbox130" onMouseOver="window.status='Bitte den Bearbeiter ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;" title="Bitte den Bearbeiter ausw&auml;hlen">"""

akte_neu_t4 = """
                    </select>
                  </td>
                  <td width="32%%" class="labeltext" height="42" align="right">Fallbeginn:</td>
                  <td width="3%%" height="42">
                    <input type="text" maxlength=2  name="zubgd" class="textboxsmall" size="2"
                     onMouseOver="window.status='Tag des Fallbeginns';return true;" onMouseOut="window.status='';return true;" title="Tag des Fallbeginns">
                  </td>
                                  <td height="42" width="1%%">.</td>
                                  <td width="3%%">
                    <input type="text" maxlength=2 name="zubgm" value="%(month)d" class="textboxsmall" size="2" onMouseOver="window.status='Monat des Fallbeginns';return true;" onMouseOut="window.status='';return true;" title="Monat des Fallbeginns">
                  </td>
                                  <td width="1%%">.</td>
                                  <td width="6%%">
                    <input type="text" maxlength=4 name="zubgy" value="%(year)d" class="textboxmid" size="4" onMouseOver="window.status='Jahr des Fallbeginns';return true;" onMouseOut="window.status='';return true;" title="Jahr des Fallbeginns">
                  </td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset><legend class="legendtext"> Leistung</legend>
              <table width="95%%" border="0" cellpadding="1" height="70">
                <tr valign="middle">
                  <td align="right" class="labeltext" width="14%%">Mitarbeiter:</td>
                  <td width="34%%">
                    <select name="lemitid" width=20 class="listbox130"  onMouseOver="window.status='Bitte den Bearbeiter der erbrachten Leistung w&auml;hlen';return true;" onMouseOut="window.status='';return true;" title="Bitte den Bearbeiter der erbrachten Leistung w&auml;hlen">"""
akte_neu_t5 = """
                    </select>
                  </td>
                  <td width="12%%" class="labeltext" align="right">Leistung:</td>
                  <td width="40%%">
                    <select name="le" width=30 class="listbox"  onMouseOver="window.status='Bitte die erbrachte Leistung w&auml;hlen';return true;" onMouseOut="window.status='';return true;" title="Bitte die erbrachte Leistung w&auml;hlen">"""

akte_neu_t6 = """
                    </select>
                  </td>
                </tr>
                <tr valign="middle">
                  <td align="right" class="labeltext" width="14%%" height="42">&nbsp;</td>
                  <td align="left" class="labeltext" width="34%%" height="42">&nbsp;
                  </td>
                  <td align="right" class="labeltext" width="12%%" height="42">Am:</td>
                  <td align="left" class="labeltext" width="40%%" height="42">
                    <table border="0" cellpadding="0" width="20%%" height="12">
                    <tr>
                    <td width="3%%" height="42">
                    <input type="text" class="textboxsmall" size=2  maxlength=2 name="lebgd" onMouseOver="window.status='Tag des Datums';return true;" onMouseOut="window.status='';return true;" title="Tag des Datums">
                    </td>
                    <td width="1%%">.</td>
                    <td width="3%%">
                    <input type="text" class="textboxsmall" size="2" maxlength=2 name="lebgm" value="%(month)d"  onMouseOver="window.status='Monat des Datums';return true;" onMouseOut="window.status='';return true;" title="Monat des Datums">
                    </td>
                    <td width="1%%">.</td>
                    <td width="6%%">
                    <input type="text" class="textboxmid" size="4"  maxlength=4 name="lebgy" value="%(year)d" onMouseOver="window.status='Jahr des Datums';return true;" onMouseOut="window.status='';return true;" title="Jahr des Datums">
                    </td>
                    </tr>
                    </table>
                  </td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button" onMouseOver="window.status='Anlegen der Akte mit den angegebenen Daten';return true;" onMouseOut="window.status='';return true;" title="Anlegen der Akte mit den angegebenen Daten">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button" onMouseOver="window.status='Das Formular zur&uuml;cksetzen';return true;" onMouseOut="window.status='';return true;" title="Das Formular zur&uuml;cksetzen">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" onMouseOver="window.status='Zur&uuml;ck zum vorhergehenden Formular';return true;" onMouseOut="window.status='';return true;" title="Zur&uuml;ck zum vorhergehenden Formular">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
        </table>
        """

akte_neu_t7 = """
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""

##*************************************************************************
##
## Formular: Akte bearbeiten
##
##*************************************************************************

akte_update_t1 = """
</HEAD>
<body bgcolor="#CCCCCC" text="#000000" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.akteform.vn.focus()">
<table width="735" align="center">
 <tr>
    <td align="center" valign="top">
      <form name="akteform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="200">
""" + klientendaten_t + \
"""            </td>
            <td valign="top" align="center" class="legendtext" width="55%%" height="200">
""" + anschrift_akte_t

akte_update_t3 = """
                    </select>
                      </td>
                      </tr>
                      </table>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset><legend>Notiz</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="85%%" align="center" height="35" valign="middle">
                    <input type="text" size=50 maxlength=255 value="%(no)s" name="no"  onMouseOver="window.status='Hier k&ouml;nnen Sie einen Notiztext zum Klienten eingeben';return true;" onMouseOut="window.status='';return true;" title="Hier k&ouml;nnen Sie einen Notiztext zum Klienten eingeben">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button" onMouseOver="window.status='&Auml;nderungen speichern';return true;" onMouseOut="window.status='';return true;" title="&Auml;nderungen speichern">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button" onMouseOver="window.status='Zur&uuml;cksetzen des Formulars';return true;" onMouseOut="window.status='';return true;" title="Zur&uuml;cksetzen des Formulars">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" onMouseOver="window.status='Zur&uuml;ck zum vorhergehenden Formular';return true;" onMouseOut="window.status='';return true;" title="Zur&uuml;ck zum vorhergehenden Formular">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
        </table>
        """

akte_update_t7 = """
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""

##*************************************************************************
##
## Formular: Wiederaufnahme eines Falles
##
##*************************************************************************

wiederaufnahme_t1 = """
</HEAD>
<body bgcolor="#CCCCCC" text="#000000" onLoad="javascript:document.akteform.vn.focus()">
<table width="735" align="center">
 <tr>
    <td height="465" align="center" valign="top">
      <form name="akteform" method="post" action="klkarte">
      <input type="hidden" value="%(id)d" name="akid">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="200">
""" + klientendaten_t + \
"""            </td>
            <td valign="top" align="center" class="legendtext" width="55%%" height="200">
""" + anschrift_akte_t

wiederaufnahme_t3 = """
                    </select>
                      </td>
                      </tr>
                      </table>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset><legend>Notiz</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="85%%" align="center" height="35" valign="middle">
                    <input type="text" size=50 maxlength=255 value="%(no)s" name="no" onMouseOver="window.status='Hier k&ouml;nnen Sie einen Notiztext zum Klienten eingeben';return true;" onMouseOut="window.status='';return true;" title="Hier k&ouml;nnen Sie einen Notiztext zum Klienten eingeben">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2" height="63">
              <fieldset><legend>Falldaten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr valign="middle">
                  <td align="right" class="labeltext" width="14%%" height="42">Bearbeiter:</td>
                  <td width="34%%" height="42">
                    <select name="zumitid" class="listbox130" onMouseOver="window.status='Bitte den Bearbeiter ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;" title="Bitte den Bearbeiter ausw&auml;hlen">"""

wiederaufnahme_t4 = """
                    </select>
                  </td>
                  <td width="12%%" class="labeltext" height="42">Fallbeginn:</td>
                  <td width="40%%" height="42">
                    <table border="0" cellpadding="0">
                      <tr valign="middle" height="12">
                        <td>
                          <input type="text" size=2 maxlength=2 name="zubgd" class="textboxsmall" onMouseOver="window.status='Tag des Fallbeginns';return true;" onMouseOut="window.status='';return true;" title="Tag des Fallbeginns">
                        </td>
                        <td>.</td>
                        <td>
                    <input type="text" size=2 maxlength=2 name="zubgm" value="%(month)d" class="textboxsmall" onMouseOver="window.status='Monat des Fallbeginns';return true;" onMouseOut="window.status='';return true;" title="Monat des Fallbeginns">
                        </td>
                        <td>.</td>
                        <td>
                    <input type="text" size=4 maxlength=4 name="zubgy" value="%(year)d" class="textboxmid" onMouseOver="window.status='Jahr des Fallbeginns';return true;" onMouseOut="window.status='';return true;" title="Jahr des Fallbeginns">
                        </td>
                     </tr>
                    </table>
                  </td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset><legend class="legendtext"> Leistung</legend>
              <table width="95%%" border="0" cellpadding="1" height="70">
                <tr valign="middle">
                  <td align="right" class="labeltext" width="14%%">Mitarbeiter:</td>
                  <td width="34%%">
                    <select name="lemitid" class="listbox130" onMouseOver="window.status='Bitte den Bearbeiter der erbrachten Leistung w&auml;hlen';return true;" onMouseOut="window.status='';return true;" title="Bitte den Bearbeiter der erbrachten Leistung w&auml;hlen">"""
wiederaufnahme_t5 = """
                    </select>
                  </td>
                  <td width="12%" class="labeltext" align="right">Leistung:</td>
                  <td width="40%">
                    <select name="le" class="listbox" onMouseOver="window.status='Bitte die erbrachte Leistung w&auml;hlen';return true;" onMouseOut="window.status='';return true;" title="Bitte die erbrachte Leistung w&auml;hlen">"""

wiederaufnahme_t6 = """
                    </select>
                  </td>
                </tr>
                <tr valign="middle">
                  <td align="right" class="labeltext" width="14%%" height="42">&nbsp;</td>
                  <td align="left" class="labeltext" width="34%%" height="42">&nbsp;
                  </td>
                  <td align="right" class="labeltext" width="12%%" height="42">Am:</td>
                  <td align="left" class="labeltext" width="40%%" height="42">
                    <table border="0" cellpadding="0">
                      <tr valign="middle" height="12">
                        <td>
                    <input type="text" name="lebgd" size=2 maxlength=2 class="textboxsmall" onMouseOver="window.status='Tag des Datums';return true;" onMouseOut="window.status='';return true;" title="Tag des Datums">
                        </td>
                        <td>.</td>
                        <td>
                    <input type="text" name="lebgm" size=2 maxlength=2 value="%(month)d" class="textboxsmall" onMouseOver="window.status='Monat des Datums';return true;" onMouseOut="window.status='';return true;" title="Monat des Datums">
                        </td>
                        <td>.</td>
                        <td>
                    <input type="text" name="lebgy" size=4 maxlength=4 value="%(year)d" class="textboxmid" onMouseOver="window.status='Jahr des Datums';return true;" onMouseOut="window.status='';return true;" title="Jahr des Datums">
                        </td>
                       </tr>
                     </table>
                  </td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Wiederaufnehmen" class="button" onMouseOver="window.status='Den Fall mit den eingegeben Daten wiederaufnehmen';return true;" onMouseOut="window.status='';return true;" title="Den Fall mit den eingegebenen Daten wiederaufnehmen">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
        </table>
        """

wiederaufnahme_t7 = """
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""

##*************************************************************************
##
## Formular: Update eines Falles
##
##*************************************************************************

updzda_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.akteform.bgd.focus()">
<table width="735" align="center">
 <tr>
    <td height="200" align="center" valign="top">
      <form name="akteform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset><legend>Beginndatum</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="85%%" align="center" height="35" valign="middle">
                  <table>
                    <tr>
                      <td>
                  <input type="text" size=2 maxlength=2 value="%(bgd)d" class="textboxsmall" name="bgd" >
                      </td><td>.</td>
                      <td>
                  <input type="text" size=2 maxlength=2 value="%(bgm)d" class="textboxsmall" name="bgm">
                      </td><td>.</td>
                      <td>
                  <input type="text" size=4 maxlength=4 value="%(bgy)d" class="textboxmid" name="bgy">
                      </td>
                    </tr>
                  </table>
                  </td>
                </tr>
              </table>
              </fieldset>
            </td>
          </tr>"""

thzustaendigkeiten_t="""
          <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset><legend>Zust&auml;ndigkeiten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="33%%" align="left" valign="middle" class="labeltext">
                  Bearbeiter:
                  </td>
                  <td align="left" valign="middle" width="33%%" class="labeltext">
                  Beginn:
                  </td>
                  <td align="left" valign="middle" width="34%%" class="labeltext">
                  Ende:
                  </td>
                </tr>"""

zustaendigkeiten_t = """
                <tr>
                  <td width="33%%" align="center" valign="middle" class="normaltext"" bgcolor="#FFFFFF">
                  &#160;%(mit_id__na)s
                  </td>
                  <td align="center" valign="middle" width="33%%" class="normaltext" bgcolor="#FFFFFF">
                  &#160;%(bgd)d.%(bgm)d.%(bgy)d
                  </td>
                  <td align="center" valign="middle" width="34%%" class="normaltext" bgcolor="#FFFFFF">
                  &#160;%(ed)d.%(em)d.%(ey)d
                  </td>
                </tr>"""

zustaendigkeiten_ende_t = """
              <tr>
              <td colspan="3">&nbsp;</td>
              </tr>
              </table>
              </fieldset> </td>
          </tr>"""

updzda_t2 = """
          <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
        </table>
      </form>
    </td>
 </tr>
</table>
</body>
</html>
"""

##*************************************************************************
##
## Formular: Zu den Akten legen (Fall abschliessen)
##
##*************************************************************************

zda_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.zdaform.bgd.focus()">
<table width="735" align="center">
 <tr>
    <td height="200" align="center" valign="top">
      <form name="zdaform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset><legend>Falldaten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="50%%" align="center" height="35" valign="middle" class="labeltext">
                  Beginndatum:
                  </td>
                  <td width="50%%" align="center" height="35" valign="middle" class="labeltext">
                  Abschlussdatum:
                  </td>
                </tr>
                <tr>
                  <td width="50%%" align="center" height="35" valign="middle">
                    <table>
                      <tr>
                        <td>
                  <input type="text" size=2 maxlength=2 value="%(bgd)d" class="textboxsmall" name="bgd" >
                        </td><td>.</td>
                        <td>
                  <input type="text" size=2 maxlength=2 value="%(bgm)d" class="textboxsmall" name="bgm">
                        </td><td>.</td>
                        <td>
                  <input type="text" size=4 maxlength=4 value="%(bgy)d" class="textboxmid" name="bgy">
                        </td>
                       </tr>
                     </table>
                  </td>"""

zda_t2 = """
                  <td width="50%%" align="center" height="35" valign="middle">
                    <table>
                      <tr>
                        <td>
                  <input type="text" size=2 maxlength=2 value="%(day)d" class="textboxsmall" name="zdad" >
                        </td><td>.</td>
                        <td>
                  <input type="text" size=2 maxlength=2 value="%(month)d" class="textboxsmall" name="zdam">
                        </td><td>.</td>
                        <td>
                  <input type="text" size=4 maxlength=4 value="%(year)d" class="textboxmid" name="zday">
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
              </fieldset>
            </td>
          </tr>"""

zda_t3 = """
          <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset><legend>Bisherige Zust&auml;ndigkeit wird ausgetragen</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="77%%" align="left" valign="middle" class="labeltext" colspan="2">
                  Bearbeiter:
                  </td>
                  <td align="left" valign="middle" width="33%%" class="labeltext">
                  Beginn:
                  </td>
                </tr>
                 <tr>
                  <td width="33%%" align="center" valign="middle" class="normaltext"" bgcolor="#FFFFFF">
                  &#160;%(mit_id__vn)s
                  </td>
                  <td width="33%%" align="center" valign="middle" class="normaltext"" bgcolor="#FFFFFF">
                  &#160;%(mit_id__na)s
                  </td>
                  <td align="center" valign="middle" width="33%%" class="normaltext" bgcolor="#FFFFFF">
                  &#160;%(bgd)d.%(bgm)d.%(bgy)d
                  </td>
                </tr>
                <tr>
                  <td colspan="3">&nbsp;</td>
                </tr>
             </table>
              </fieldset></td>
              <input type="hidden" value="%(mit_id__id)d" name="aktuellmitid">
              <input type="hidden" value="%(id)d" name="aktuellzustid">
          </tr>"""


zda_t4 = """
          <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
        </table>
      </form>
    </td>
 </tr>
</table>
</body>
</html>
"""

##*************************************************************************
##
## Formular: Zu den Akten rueckgaengig machen
##
##*************************************************************************

zdarzust1_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.zdarform.zumitid.focus()">
<table width="735" align="center">
 <tr>
    <td height="200" align="center" valign="top">
      <form name="zdarform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%">
          <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset><legend>Beginndatum</legend>
              <table width="95%" border="0" cellpadding="1">
                <tr>
                  <td width="50%" align="center" valign="middle" class="legendtext">Mitarbeiter:</td>
                  <td width="50%" align="center" valign="middle" class="legendtext">Beginn:</td>
                </tr>
                <tr>
                  <td align="center" height="35" valign="middle">
                  <select class="listbox130" name="zumitid">"""

zdarzust2_t = """ </select>
                  </td>
                  <td valign="middle" align="center">
                    <table>
                      <tr>
                      <td>
                    <input type="text" size=2 maxlength=2 class="textboxsmall" name="bgd"  value="%(day)d">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" size=2 maxlength=2 class="textboxsmall" name="bgm" value="%(month)d">
                      </td><td>.</td>
                      <td>
                    <input type="text" size=4 maxlength=4 class="textboxsmid" name="bgy" value="%(year)d">
                      </td>
                      </tr>
                    </table
                  </td>
                </tr>
              </table>
              </fieldset>
            </td>
         </tr>"""

zdarzust3_t = """
         <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
       </table>
     </form>
   </td>
  </tr>
</table>
</bod>
</html>"""

##*************************************************************************
##
## Formular: Akten loeschen 1
##
##*************************************************************************

rmakten_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
 <tr>
    <td height="200" align="center" valign="top">
      <form name="zdarform" method="post" action="rmakten2">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="50%%" align="center" class="legendtext" valign="middle">
              <fieldset><legend>Ab&auml;nderung der Voreinstellung der L&ouml;schfrist</legend>
              <table width="95%%" border="0" cellpadding="1">
              <tr>
                <td width="50%%" align="right" class="labeltext">
                  L&ouml;schfrist:
                </td>
                <td align="left" class="labeltext">
                  <input type="text"  size=2 maxlength="2" class="textboxsmall" name="frist" value="%d">
                </td>
                <td width="50%%" align="left" class="labeltext">
                  Monate
                </td>
              </tr>
              </table>
              </fieldset>
            </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Weiter" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset>
            </td>
          </tr>
        </table>
      </form>
    </td>
 </tr>
</table>
</body>
</html>
"""

##*************************************************************************
##
## Formular: Akten loeschen 2
##
##*************************************************************************

rmakten2a_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
 <tr>
    <td height="200" align="center" valign="top">
      <form name="zdarform" method="post" action="admin">"""

rmakten2b_t = """
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="50%%" align="center" class="legendtext" valign="middle">
              <fieldset><legend>Sicherheitsabfrage</legend>
              <table width="95%%" border="0" cellpadding="1">
              <tr>
                <td align="center" class="labeltext">
                  Sollen alle Akten und Gruppen, die vor
                </td>
              </tr>
              <tr>
                <td align="center" class="labeltext">
                  <b>%s Monaten (d.h. vor dem %s.%s)</b>
                </td>
              </tr>
              <tr>
                <td align="center" class="labeltext">
                   geschlossen wurden, jetzt gel&ouml;scht werden?
                </td>
              </table>
              </fieldset>
            </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="L&ouml;schen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset>
            </td>
          </tr>
        </table>
      </form>
    </td>
 </tr>
</table>
</body>
</html>
"""

##*****************************************************************
## Bodys fuer Bezugsperson
## wenn Stra&szlig;e in Berlin, dann Body mit Hinweis
## 13.11.2001 HeS
##*****************************************************************
body_pers_start = """
</HEAD>
<BODY bgcolor=#CCCCCC>
<P>"""

body_pers_start_js = """
</HEAD>
<BODY bgcolor=#CCCCCC onLoad="hinweis()">
<P>"""
