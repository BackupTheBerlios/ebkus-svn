# coding: latin-1
from ebkus.app_surface.standard_templates import *

wordauswahl_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
 <tr>
    <td height="465" align="center" valign="top">
      <form name="wordvorlagenauswahl" method="post" action="wordexport" accept="application/msword">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="200">
              <fieldset><legend class="legendtext">Auswahl der Dokumentenvorlage</legend>
              <table width="90%%" border="0" cellpadding="1" height="200">
                <tr>
                <input type="hidden" name="akid" value="%s">
                  <td align="center" class="labeltext">
                    MSWord - Vorlagedatei (*.doc, *.rtf):
                  </td>
                </tr>
                <tr>
                  <td align="center">
                    <input name="wordvorlage" type="file" size="50">
                  </td>
                </tr>
                <tr>
                  <td colspan="2" align="center">
                  <input type="submit" name="Exportieren" value="Exportieren" class="button">&nbsp;&nbsp;&nbsp;
                  <input type=button onClick="go_to_url('klkarte?akid=%s')" name="cancelbutton" value="Zur&uuml;ck"  class="button">
</td>
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
"""

wordexport_top_t = """
<HTML>
<HEAD>
<meta http-equiv="refresh" content="5; URL=klkarte?akid=%s">

<SCRIPT LANGUAGE="JScript">
function makeWord()
{
//++++EBKuS Insert Start++++

var pfad_zu_vorlage="%s";
var klient = new ActiveXObject("Scripting.Dictionary");
var bzperson = new ActiveXObject("Scripting.Dictionary");
var leistungen = new ActiveXObject("Scripting.Dictionary");
var stand = new ActiveXObject("Scripting.Dictionary");
var bearbeiter = new ActiveXObject("Scripting.Dictionary");
var anmkontakte = new ActiveXObject("Scripting.Dictionary");
var einkontakte = new ActiveXObject("Scripting.Dictionary");
var fachstat = new ActiveXObject("Scripting.Dictionary");
var jghstat = new ActiveXObject("Scripting.Dictionary");
var gkfall = new ActiveXObject("Scripting.Dictionary");
var gkbzp = new ActiveXObject("Scripting.Dictionary");
var notizen = new ActiveXObject("Scripting.Dictionary");
var jetzt = new Date();
var tag = jetzt.getDay();
var monat =  jetzt.getMonth();
var jahr = jetzt.getYear();
datum = tag + "." + monat + "." + jahr;
klient.add ("%%akt_dat", datum);
"""

wordexport_bot_t = """
//++++EBKuS Insert Ende++++

var WordObj;
WordObj = new ActiveXObject("Word.Application");
WordObj.DisplayAlerts = false;
WordObj.Documents.Open(pfad_zu_vorlage);
WordObj.Visible = true;

for (i = 1; i <= WordObj.ActiveDocument.Shapes.Count; i++) {
 var str_tester = WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text;
 str_tester = str_tester.substr(0, (str_tester.length - 1));
 i_founded = 0;
 if (klient.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = klient.Item(str_tester);
  i_founded = 1;
 }
 if (bzperson.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = bzperson.Item(str_tester);
  i_founded = 1;
 }
 if (leistungen.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = leistungen.Item(str_tester);
  i_founded = 1;
 }
 if (stand.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = stand.Item(str_tester);
  i_founded = 1;
 }
 if (bearbeiter.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = bearbeiter.Item(str_tester);
  i_founded = 1;
 }
 if (anmkontakte.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = anmkontakte.Item(str_tester);
  i_founded = 1;
 }
 if (einkontakte.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = einkontakte.Item(str_tester);
  i_founded = 1;
 }
 if (fachstat.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = fachstat.Item(str_tester);
  i_founded = 1;
 }
 if (jghstat.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = jghstat.Item(str_tester);
  i_founded = 1;
 }
 if (jghstat.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = jghstat.Item(str_tester);
  i_founded = 1;
 }
 if (gkfall.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = gkfall.Item(str_tester);
  i_founded = 1;
 }
 if (notizen.Exists(str_tester)){
  WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = notizen.Item(str_tester);
  i_founded = 1;
 }
 if (i_founded != 1){
  n_res = 0;
  n_res2 = 0;
  n_res2 = str_tester.search("%kl_");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%bzp");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%lst");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%std");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%brb");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%amd");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%einr");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%fst");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%jgh");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%gkf");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%gkb");
  n_res = n_res + n_res2;
  n_res2 = str_tester.search("%ntz");
  n_res = n_res + n_res2;
  if (n_res != -12) {
     WordObj.Application.ActiveDocument.Shapes.Item(i).TextFrame.TextRange.Text = "";
  }
  i_founded = 1;
 }
}
WordObj.Application.ActiveDocument.Saved = true;
//WordSheet.Application.Quit();

}
</SCRIPT>

</HEAD>
<BODY>
<SCRIPT>
makeWord();
</SCRIPT>
</BODY>
</HTML>
"""

wordexport_kldaten_t = """
//Klientendaten
klient.add ("%%kl_vn", "%(vn)s");
klient.add ("%%kl_na", "%(na)s");
klient.add ("%%kl_gb", "%(gb)s");
klient.add ("%%kl_str", "%(str)s");
klient.add ("%%kl_plz", "%(plz)s");
klient.add ("%%kl_ort", "%(ort)s");
klient.add ("%%kl_tl1", "%(tl1)s");
klient.add ("%%kl_tl2", "%(tl2)s");
klient.add ("%%kl_ber", "%(ber)s");
klient.add ("%%kl_bei", "%(fs__name)s");
"""

wordexport_bzperson_t = """
//Bezugsperson Nr. %(lfdnr)s
bzperson.add("%%bzp%(lfdnr)s_vn", "%(vn)s");
bzperson.add("%%bzp%(lfdnr)s_na", "%(na)s");
bzperson.add("%%bzp%(lfdnr)s_gb", "%(gb)s");
bzperson.add("%%bzp%(lfdnr)s_str", "%(str)s");
bzperson.add("%%bzp%(lfdnr)s_plz", "%(plz)s");
bzperson.add("%%bzp%(lfdnr)s_ort", "%(ort)s");
bzperson.add("%%bzp%(lfdnr)s_tl1", "%(tl1)s");
bzperson.add("%%bzp%(lfdnr)s_tl2", "%(tl2)s");
bzperson.add("%%bzp%(lfdnr)s_ber", "%(ber)s");
bzperson.add("%%bzp%(lfdnr)s_bei", "%(fs__name)s");
"""

wordexport_leistungen_t = """
//Leistungen Nr. %(lfdnr)s
leistungen.add ("%%lst%(lfdnr)s_bea", "%(mit_id__na)s");
leistungen.add ("%%lst%(lfdnr)s_lst", "%(le__name)s");
leistungen.add ("%%lst%(lfdnr)s_beg", "%(bgd)d.%(bgm)d.%(bgy)d");
leistungen.add ("%%lst%(lfdnr)s_end", "%(ed)d.%(em)d.%(ey)d");
"""

wordexport_stand_t = """
//Stand Nr. %(lfdnr)s
stand.add ("%%std%(lfdnr)s_fnr", "%(fn)s");
stand.add ("%%std%(lfdnr)s_beg", "%(bgd)d.%(bgm)d.%(bgy)d");
stand.add ("%%std%(lfdnr)s_end", "%(zdad)d.%(zdam)d.%(zday)d");
"""

wordexport_bearbeiter_t = """
//Bearbeiter Nr. %(lfdnr)s
bearbeiter.add ("%%brb%(lfdnr)s_bea", "%(mit_id__na)s");
bearbeiter.add ("%%brb%(lfdnr)s_beg", "%(bgd)d.%(bgm)d.%(bgy)d");
bearbeiter.add ("%%brb%(lfdnr)s_end", "%(ed)d.%(em)d.%(ey)d");
"""

wordexport_anmkontakte_t = """
//Anmeldungskontake Nr. %(lfdnr)s
anmkontakte.add ("%%amd%(lfdnr)s_von", "%(von)s");
anmkontakte.add ("%%amd%(lfdnr)s_am",  "%(ad)d.%(am)d.%(ay)d");
anmkontakte.add ("%%amd%(lfdnr)s_tel", "%(mtl)s");
anmkontakte.add ("%%amd%(lfdnr)s_zgs", "%(zm__name)s");
anmkontakte.add ("%%amd%(lfdnr)s_epf", "%(me)s");
anmkontakte.add ("%%amd%(lfdnr)s_grd", "%(mg)s");
anmkontakte.add ("%%amd%(lfdnr)s_ntz", "%(no)s");
"""

wordexport_einkontakte_t = """
//Einrichtungskontakte Nr. %(lfdnr)s
einkontakte.add ("%%einr%(lfdnr)s_art", "%(insta__name)s");
einkontakte.add ("%%einr%(lfdnr)s_na",  "%(na)s");
einkontakte.add ("%%einr%(lfdnr)s_tl1", "%(tl1)s");
einkontakte.add ("%%einr%(lfdnr)s_tl2", "%(tl2)s");
einkontakte.add ("%%einr%(lfdnr)s_ntz", "%(no)s");
einkontakte.add ("%%einr%(lfdnr)s_wtg", "%(status__code)s");
"""

wordexport_fachstat_t = """
//Fachstatistiken Nr. %(lfdnr)s
fachstat.add ("%%fst%(lfdnr)s_jhr", "%(jahr)s");
"""

wordexport_jghstat_t = """
//Jugenhilfestatistiken Nr. %(lfdnr)s
jghstat.add ("%%jgh%(lfdnr)s_jhr", "%(ey)s");
"""

wordexport_gkfall_t1 = """
//Gruppenkarten des Falls Nr. %(lfdnr)s
gkfall.add ("%%gkf%(lfdnr)s_nr", "%(gruppe_id__gn)s");
"""

wordexport_gkfall_t2 = """
gkfall.add ("%%gkf%(lfdnr)s_na", "%(akte_id__vn)s %(akte_id__na)s");
"""

wordexport_gkbzp_t1 = """
//Gruppenkarten der Bezugspersonen Nr. %(lfdnr)s
gkbzp.add ("%%gkb%(lfdnr)s_nr", "%(gruppe_id__gn)s");
"""

wordexport_gkbzp_t2 = """
gkbzp.add ("%%gkb%(lfdnr)s_na", "%(vn)s %(na)s");
"""

wordexport_notiz_kldaten_t =  """
notizen.add ("%%ntz0", "%(vn)s %(na)s : %(no)s");
"""

wordexport_notiz_bzperson_t =  """
notizen.add ("%%ntz%(lfdnr)s", "%(vn)s %(na)s : %(no)s");
"""

wordexport_notiz_einkontakte_t =  """
notizen.add ("%%ntz%(lfdnr)s", "%(insta__name)s %(na)s : %(no)s");
"""

wordexport_notiz_anmkontakte_t =  """
notizen.add ("%%ntz%(lfdnr)s", "Anmeldungskontakt : %(no)s");
"""