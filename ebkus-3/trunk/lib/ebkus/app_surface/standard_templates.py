# coding: latin-1
type_t = "Content-type: text/html\n"


head_normal_t = """
<HTML>
<HEAD>
<TITLE> %s </TITLE>
<meta http-equiv="expires" content="0">
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
<script src="/ebkus/ebkus_javascripte/ebkus_help.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles.css">"""

head_normal_ohne_help_t = """
<HTML>
<HEAD>
<TITLE> %s </TITLE>
<meta http-equiv="expires" content="0">
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles.css">"""


head_weiterleitung_t = """
<HTML>
<HEAD>
<TITLE> %s </TITLE>
<meta http-equiv="expires" content="0">
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
<meta http-equiv="refresh" content="%s; URL=%s">
<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles.css">
"""

meldung_t = """
<HTML>
<HEAD>
<TITLE> %(titel)s </TITLE>
<!-- <meta http-equiv="expires" content="0"> //-->
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles.css">
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
  <table width="50%%" border="0" height="215" align="center">
    <tr>
      <td height="223" align="center" class="legendtext">
      <fieldset><b><legend>%(legende)s</legend></b>
        <table width="89%%" border="0" height="120">
          <tr><td>&nbsp;</td></tr>
          <tr>
            <td height="67" class="normaltext">%(zeile1)s</td>
          </tr>
          <tr>
            <td height="65" class="normaltext">%(zeile2)s</td>
          </tr>
        </table>
        <form name="form1" method="post" action="">
          <input type="button" class="button" name="zurueck" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" onClick="javascript:history.back()"  onMouseOver="window.status='Zur&uuml;ck';return true;" onMouseOut="window.status='';return true;" title="Zur&uuml;ck">
        </form>
        </fieldset>
      </td>
    </tr>
  </table>
</body>
</html>"""

meldung_weiterleitung_t = """
<HTML>
<HEAD>
<TITLE> %(titel)s </TITLE>
<!-- <meta http-equiv="expires" content="0"> //-->
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles.css">
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
  <table width="50%%" border="0" height="215" align="center">
    <tr>
      <td height="223" align="center" class="legendtext">
      <fieldset><b><legend class="legendtext">%(legende)s</legend></b>
        <table width="89%%" border="0" height="120">
          <tr><td>&nbsp;</td></tr>
          <tr>
            <td height="67" class="normaltext">%(zeile1)s</td>
          </tr>
          <tr>
            <td height="65" class="normaltext">%(zeile2)s</td>
          </tr>
        </table>
        <form name="form1" method="post" action="">
          <input type="button" class="button" name="zurueck" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" onClick="go_to_url('%(url)s')">
        </form>
        </fieldset>
      </td>
    </tr>
  </table>
</body>
</html>"""


bestaetigung_t = """
<html>
<head>
<TITLE>%(titel)s</TITLE>
<!-- <meta http-equiv="expires" content="0"> //-->
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
<!--<script src="/ebkus/ebkus_javascripte/ebkus_help.js" type="text/javascript"></script>-->
<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles.css">
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
  <table width="50%%" border="0" height="215" align="center">
    <tr>
      <td height="223" align="center" class="legendtext">
      <fieldset><b><legend class="legendtext">%(legende)s</legend></b>
        <table width="89%%" border="0" height="120">
          <tr>
            <td height="67" class="normaltext" align="center">%(zeile)s</td>
          </tr>
        </td>        
        <form name="form1" method="post" action="jghexportfeedback">
        <tr>
        <td class="labeltext" align="center">Exportjahr: <input type="text" class="textboxmid" size="4" maxlength="4" value="%(jahr)s" name="jahr"></td>
        </tr>        
        <tr>
        <td align="center">
        &nbsp;
        </td>
        </tr>
        </table>
          <input type="submit" class="button"  value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;">
          <input type="button" class="button" name="zurueck" value="Abbrechen" onClick="javascript:history.back()">
        </form>
        </fieldset>
      </td>
    </tr>
  </table>
</body>
</html>"""

formhiddenvalues_t = """
<input type="hidden" value="%(file)s" name="file">
"""
formhiddennamevalues_t = """
<input type="hidden" value="%(value)s" name="%(name)s">"""

hiddenakte_id = """
<input type="hidden" value="%(akte_id)d" name="akid">
<input type="hidden" value="%(id)d" name="fallid">
"""

radio_t = """
<input type="radio" value="%(id)d" name="%(kat_code)s" > """

radiocheck_t = """
<input type="radio" value="%(id)d" name="%(kat_code)s" checked > """

strassenliste_t = """
      <option value="%(strvalue)s" >%(strvalue)s"""

strassenlisteupd_t = """
      <option value="%(strvalue)s" %(sel)s > %(strvalue)s"""

codelisteos_t = """
      <option value="%(id)d" > %(name)s """

codeliste_t = """
      <option value="%(id)d" %(sel)s > %(name)s """

codelistecode_t = """
      <option value="%(id)d" %(sel)s > %(code)s """

mitarbeiterliste_t = """
      <option value="%(id)d" %(sel)s > %(na)s """

selectbg_t = """
      <select name="%(name)s" class="listbox" size=%(size)s style="width:300pt">
      """
selectmbg_t = """
      <select multiple class="listbox" name="%(name)s" size=%(size)s style="width:300pt">
      """
checkbox_t = """
      <input type="checkbox" value="%(id)d" name="%(name)s" %(check)s >"""

gruppe_menu_t = """
<tr>
  <td align="center" height="30" class="legendtext"> <fieldset><legend class="legendtext">Steuerung</legend>
    <table border="0" cellpadding="1" width="50%%" height="30">
      <form>
      <tr valign="top">
        <td align="center" height="30">
          <input type="button" name="Schaltfl&auml;che" onClick="go_to_url('menu')" value="Hauptmen&uuml;" class="button">
        </td>
        <td align="center" height="30">
          <input type="button" name="Schaltfl&auml;che"
            onClick="go_to_url('menugruppe')" value="Gruppenmen&uuml;" class="button">
        </td>
      </tr>
      </form>
    </table>
    </fieldset> </td>
  <td align="center" height="30" class="legendtext"> <fieldset><legend class="legendtext">Gruppe</legend>
    <table border="0" cellpadding="1" height="30">
      <tr>
        <td align="center" class="smalltext" height="30"> <A HREF="gruppeneu" onMouseOver="window.status='Neue Gruppe anlegen';return true;" onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/grp_button.gif" width="21" height="19" alt="Neue Gruppe anlegen">
          </A> </td>
        <td align="center" height="30"> <A HREF="updgruppe?gruppeid=%(id)d" onMouseOver="window.status='Gruppe bearbeiten';return true;" onMouseOut="window.status='';return true;">
        <img border="0" src="/ebkus/ebkus_icons/edit_grp_button.gif" width="21" height="19" alt="Gruppe bearbeiten.">
          </A> </td>
        <td align="center" height="30"> <A HREF="gruppeteilnausw?gruppeid=%(id)d" onMouseOver="window.status='Neuen Teilnehmer hinzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/teilnehmer_neu_button.gif" width="21" height="19" alt="Neuen Teilnehmer hinzuf&uuml;gen">
          </A> </td>
        <td align="center" height="30"> <A HREF="rmteiln?gruppeid=%(id)d" onMouseOver="window.status='Teilnehmer entfernen';return true;" onMouseOut="window.status='';return true;">
         <img border="0" src="/ebkus/ebkus_icons/teilnehmer_del_button.gif" width="21" height="19" alt="Teilnehmer entfernen." title="Teilnehmer entfernen">
          </A> </td>
        <td align="center" height="30">
        <A HREF="gruppeteiln?gruppeid=%(id)d" onMouseOver="window.status='Teilnehmerliste anzeigen';return true;" onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/teilnehmer_view_button.gif" width="21" height="19" alt="Teilnehmerliste anzeigen.">
          </A> </td>
        <td align="center" height="30"> <A HREF="vermneu?gruppeid=%(id)d" onMouseOver="window.status='Neuen Vermerk anf&uuml;gen';return true;" onMouseOut="window.status='';return true;"> <img border="0" src="/ebkus/ebkus_icons/new_text_button.gif" width="21" height="19" alt="Neuen Vermerk anf&uuml;gen.">
          </A> </td>
        <td align="center" height="30"> <A HREF="updvermausw?gruppeid=%(id)d" onMouseOver="window.status='Vermerk zum Bearbeiten ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/edit_text_button.gif" width="21" height="19" alt="Vermerk zum Bearbeiten ausw&auml;hlen.">
          </A> </td>
        <td align="center" height="30"> <A HREF="rmdok?gruppeid=%(id)d" onMouseOver="window.status='Vermerk entfernen';return true;" onMouseOut="window.status='';return true;"> <img border="0" src="/ebkus/ebkus_icons/del_text_button.gif" width="21" height="19" alt="Vermerk entfernen.">
          </A> </td>
        <td align="center" height="30"> <A HREF="upload?gruppeid=%(id)d" onMouseOver="window.status='Datei hochladen';return true;" onMouseOut="window.status='';return true;">
        <img border="0" src="/ebkus/ebkus_icons/upload_button.gif" width="21" height="19" alt="Datei hochladen.">
          </A> </td>
      </tr>
    </table>
    </fieldset> </td>
</tr>"""

menuefs_t = """
  <tr>
    <td align="center" width="364" class="legendtext"><fieldset><legend class="legendtext">Steuerung</legend>
      <table border="0" cellpadding="1" width="50%%" height="30">
        <form>
        <tr valign="top">
          <td align="center" height="30">
            <input type="button" name="Schaltfl&auml;che" onClick="go_to_url('menu')" value="Hauptmen&uuml;" class="button" onMouseOver="window.status='Zum Hauptmen&uuml;';return true;" onMouseOut="window.status='';return true;" alt="Zum Hauptmen&uuml;">
          </td>
          <td align="center" height="30">
            <input type="button" name="Schaltfl&auml;che"
            onClick="go_to_url('menugruppe')" value="Gruppenmen&uuml;" class="button" onMouseOver="window.status='Zum Gruppenmen&uuml;';return true;" onMouseOut="window.status='';return true;" alt="Zum Gruppenmen&uuml;">
          </td>
        </tr>
        </form>
      </table>
      </fieldset> </td>
    <td align="center" width="359" class="legendtext"><fieldset><legend class="legendtext">Statistik</legend>
      <table width="95%" border="0">
        <tr valign="top" height="40">
          <td align="center" height="30"><A HREF="fsabfr" onMouseOver="window.status='Fachstatistik Abfrage';return                true;" onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/abfr_stat_fs_button.gif" alt="Fachstatistik Abfrage"></A></td>
          <td align="center" height="30"><A HREF="formabfr6?file=abfritem" onMouseOver="window.status='Abfrage nach Kategorieauswahl';return true;" onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/abfr_stat_i_button.gif" alt="Abfrage nach Kategorieauswahl"></A></td>
          <td align="center" height="30"><A HREF="formabfr6?file=abfrkat" onMouseOver="window.status='Abfrage nach Kategorienauswahl';return true;" onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/abfr_stat_k_button.gif" alt="Abfrage nach Kategorienauswahl"></A>
          </td>
          <td align="center" height="30"><A HREF="jghabfr" onMouseOver="window.status='Jugendhilfestatistik Abfrage';return true;" onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/abfr_stat_jgh_button.gif" alt="Jugendhilfestatistik Abfrage"></A></td>
          <td align="center" height="30"><A HREF="formabfr3" onMouseOver="window.status='Suche in der Kartei';return                true;" onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/abfr_stat_suche_button.gif" alt="Suche in der Kartei"></A></td>
        </tr>
      </table>
      </fieldset> </td>
  </tr>"""

##*************************************************************************
## Templates für Formabfragen
##*************************************************************************

thformabfr_kopf_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
<form action="%s" method="post">"""

formabfr_ende_t = """
 <tr>
   <td align="center" class="legendtext">
      <fieldset>
      <table width="95%">
      <tr height="40">
      <td align="center"><input type="submit" name="" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button"></td>
      <td align="center"><input type="button" name="" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()"></td>
      </tr>
      </table>
      </fieldset>
    </td>
  </tr>
</form>
</table>
</body>
</html>
"""

formabfr_jahr_t = """
   <tr>
    <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>%s</b></legend>
      <table border=0 cellspacing=1 width="95%%">
        <tr height="19">
        <td class="labeltext" align="center">F&uuml;r das Jahr:</td>
        </tr>
        <tr>
        <td align="center">
        <input type="text" class="textboxmid" size="4" maxlength="4" value="%s" name="jahr">
        </td>
        </tr>
        <tr><td>&nbsp;</td></tr>
        </table>
       </fieldset>
       </td>
       </tr>"""

sprungmarke_t = """
<tr>
<td>
<a name="%s">&nbsp;</a>
</tr>
</td>
"""

jghstat_menue_t = """
<option value="#%s">%s
"""
jghstat_menue_head_t = """
<tr>
<td align="center" valign="top" height="61" colspan="2" legend class="legendtext">
<fieldset><legend class="legendtext"><b>Auswahlmenue</b></legend>
<table cellpadding=2 valign="top" border="0" height="36">
<tr>
<td valign="top" align="center" height="35">
<form>
<select size=1 name="Auswahl" onChange="go_to_url(this.form.Auswahl.options[this.form.Auswahl.options.selectedIndex].value)" class="listbox">
"""
jghstat_menue_end_t = """
</select>
</form>
</td>
</tr>
</table>
</fieldset></td>
</tr>
"""
