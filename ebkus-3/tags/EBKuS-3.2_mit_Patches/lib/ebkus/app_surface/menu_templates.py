# coding: latin-1
from ebkus.app_surface.standard_templates import *

main_menu_t = """
</HEAD>
<BODY bgcolor=#CCCCCC link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="window.setTimeout('ZeitAnzeigen()',0)">
<FORM ACTION="klkarte" METHOD="post">
<table width="735" align="center">
<tr>
<td>
  <table width="95%%" border="0" align="center" height="374">
    <tr>
      <td colspan="2" align="center" height="20">
      <table width="100%%" height="20">
        <tr>
        <td align="center" colspan="2">
        <a href="%(index_url)s"><img border="0" src="/ebkus/ebkus_icons/ebkus_logo.gif"></a>
        </td>
        </tr
        <tr>
          <td align="left" width="50%%" class="normaltext">Angemeldet als: %(na)s, %(vn)s (%(ben)s)</td>
          <td align="right" width="50%%"><div id="Uhr" class="normaltext">&nbsp;</div></td>
        </tr>
      </table>
      </td>
    </tr>
    <tr>
      <td width="45%%" align="center" valign="top" height="294">
        <table width="326" border="0" height="291">
          <tr>
            <td align="center" valign="top" height="112" width="155" legend class="legendtext"><fieldset><legend class="legendtext"><b>Neu</b></legend>
              <table width="140" height="81">
                <tr>
                  <td align="left" class="labeltext">
                    <input type="radio" value="akteneu" name="file" title="Neue Akte anlegen."  onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Anlegen einer neuen Akte';return true;" onMouseOut="window.status='';return true;">
                    Neuaufnahme </td>
                </tr>
                <tr>
                  <td align="left" class="labeltext">
                    <input type="radio" value="fsneu" name="file" title="Neue Fachstatistik anlegen." onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Anlegen einer neuen Fachstatistik.. Bitte ebenfalls einen Klienten ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;">
                    Fachstatistik </td>
                </tr>
                <tr>
                  <td align="left" class="labeltext">
                    <input type="radio" value="jghneu" name="file"  title="Neue Bundesstatistik anlegen." onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Anlegen einer neuen Bundesstatistik. Bitte ebenfalls einen Klienten ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;">
                    Bundesstatistik </td>
                </tr>
                <tr>
                  <td align="left" class="labeltext" height="8">
                    <input type="radio" value="gruppeneu" name="file" title="Neue Gruppe anlegen." onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Anlegen einer neuen Gruppe.';return true;" onMouseOut="window.status='';return true;">
                    Gruppe </td>
                </tr>
              </table>
              </fieldset> </td>
            <td align="center" valign="top" height="112" width="153" legend class="legendtext"><fieldset><legend class="legendtext"><b>Ansicht</b></legend>
              <table width="140" border="0" height="81">
                <tr>
                  <td class="labeltext">
                    <input type="radio" value="klkarte" name="file"  title="Klientenkarte ansehen." onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Ansehen einer Klientenkarte. Bitte ebenfalls einen Klienten ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;">
                    Klientenkarte</td>
                </tr>
                <tr>
                  <td class="labeltext">
                    <input type="radio" value="vorblatt" name="file" title="Aktenvorblatt ansehen." onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Ansehen eines Aktenvorblattes. Bitte ebenfalls einen Klienten ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;">
                    Aktenvorblatt</td>
                </tr>
                <tr>
                  <td class="labeltext" height="16">
                    <input type="radio" value="dokkarte" name="file" title="Akte ansehen." onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Ansehen einer Klientenakte. Bitte ebenfalls einen Klienten ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;">
                    Akte</td>
                </tr>
                <tr>
                  <td class="labeltext" height="21">
                    <input type="radio" value="menugruppe" name="file" title="Gruppe ansehen." onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Wechseln in das Gruppenmen&uuml;';return true;" onMouseOut="window.status='';return true;">
                    Gruppenmen&uuml;</td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
          <tr>
            <td align="center" valign="top" height="76" width="155" legend class="legendtext"><fieldset><legend class="legendtext"><b>Suche</b></legend>
              <table width="140" border="0">
                <tr>
                  <td class="labeltext" align="left">
                    <input type="radio" value="formabfr3" name="file" title="Suchen einer Klientenkarte" onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Suchen einer Klientenkarte';return true;" onMouseOut="window.status='';return true;">
                    Klientenkarte</td>
                </tr>
                <tr>
                  <td class="labeltext" align="left" height="2">
                    <input type="radio" value="formabfr3" name="file" title="Suchen einer Gruppenkarte" onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum Suchen einer Gruppenkarte';return true;" onMouseOut="window.status='';return true;">
                    Gruppenkarte</td>
                </tr>
              </table>
              </fieldset> </td>
            <td align="center" valign="top" height="76" width="153" legend class="legendtext"><fieldset><legend class="legendtext"><b>&Auml;ndern</b></legend>
              <table width="140" height="46">
                <tr>
                  <td align="left" class="labeltext" width="144">
                    <input type="radio" value="updfsform" name="file"  title="&Auml;ndern einer Fachstatistik" onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum &Auml;ndern einer Fachstatistik. Bitte ebenfalls einen Klienten ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;">
                    Fachstatistik</td>
                </tr>
                <tr>
                  <td align="left" class="labeltext" width="144" height="2">
                    <input type="radio" value="updjghform" name="file" title="&Auml;ndern einer Bundesstatistik" onMouseOver="window.status='Bitte w&auml;hlen Sie diesen Men&uuml;punkt zum &Auml;ndern einer Bundesstatistik. Bitte ebenfalls einen Klienten ausw&auml;hlen';return true;" onMouseOut="window.status='';return true;">
                    Bundesstatistik</td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
          <tr>
            <td align="center" valign="top" height="61" colspan="2" legend class="legendtext"><fieldset><legend class="legendtext"><b>Statistische
              Abfragen</b></legend>
              <table cellpadding=2 valign="top" border="0" height="36">
                <tr>
                  <td valign="top" align="center" height="35">
                    <select size=1 name="Auswahl" onChange=
 "go_to_url(this.form.Auswahl.options[this.form.Auswahl.options.selectedIndex].value)" class="listbox" onMouseOver="window.status='In dieser Auswahlliste finden Sie die möglichen statistischen Abfragen';return true;" onMouseOut="window.status='';return true;">
                      <option value="nothing">[ Beratungen ]
                      <option value="abfr1?o=alle&ed=0">- alle Beratungen
                      <option value="abfr1?o=laufend&ed=0">- laufende Beratungen
                      <option value="abfr1?o=zda&ed=0">- abgeschlossene Beratungen
                      <option value="formabfr2">- ab Fallnummer?
                      <option value="nothing">
                      <option value="nothing">[ Klientenzahl ]
                      <option value="formabfr4">- Neumeldungen u. Abschl&uuml;sse
                      <option value="formabfr5">- Klienten pro Mitarbeiter
                      <option value="nothing">
                      <option value="nothing">[ Bundesstatistik ]
                      <option value="jghabfr">- Bundesstatistik
                      <option value="nothing">
                      <option value="nothing">[ Fachstatistik ]
                      <option value="fsabfr">- Fachstatistik
                      <option value="formabfr6?file=abfritem">- Itemauswahl
                      <option value="formabfr6?file=abfrkat">- Kategorienauswahl
                      <option value="fsabfr_plraum">- Planungs- und Sozialraum
                      <option value="formabfr10a">- Konsultationszahl
                      <option value="formabfr9a">- Konsultationssumme
                      <option value="formabfr11a">- Beratungsdauer
                      <option value="formabfr12a">- Beratungsdauer - Leistung
<!-----               <option value="formabfr13a">- Eltern - Merkmal x gleich
                      <option value="formabfr14a">- Elternteil - Merkmal x gleich //--->
                      <option value="nothing">
                      <option value="nothing">[ Gruppen ]
                      <option value="formabfr8a">- Gruppen&uuml;berblick
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
        </table>
      </td>
      <td width="55%%" height="294" align="center" valign="top">
        <table width="100%%" border="0" height="311">
          <tr>
            <td height="291" valign="top" align="center" legend class="legendtext"><fieldset><legend class="legendtext"><b>Klient</b></legend>
              <table cellpadding=5 width="333" border="0" height="259" align="center">
                <tr>
                  <td align="center" valign="top">
                    <select style="width:330" size="10" name="fallid" class="listbox" onMouseOver="window.status='In diesem Auswahlfeld werden alle Klienten aufgelistet, auf die Sie die entsprechenden Zugriffsrechte haben';return true;" onMouseOut="window.status='';return true;">"""

klientauswahl_t = """
<option value="%(fall_id)s" >%(mit_id__na)s | %(fall_id__akte_id__vn)s %(fall_id__akte_id__na)s, %(fall_id__akte_id__gb)s | %(fall_id__fn)s """

menusubmit_t = """
     </select>
                  </td>
                </tr>
                <tr>
                <td align="center" valign="top">
                <table width="100%">
                  <tr>
                  <td align="center"><input type="submit" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button" name="submit" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che zum Best&auml;tigen Ihrer Men&uuml;auswahl';return true;" onMouseOut="window.status='';return true;"></td>
                  <td align="center"><input type="reset"  value="&nbsp;Zur&uuml;cksetzen&nbsp;" class="button" name="reset" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um das Men&uuml; zur&uuml;ckzusetzen';return true;" onMouseOut="window.status='';return true;"></td>
                  </tr>
                  <tr>
                  <td align="center"><input type="button"  value="Passwort &auml;ndern" onClick="go_to_url('pwchange')" title="Passwort &auml;ndern." class="button" name="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che zum &Auml;ndern Ihres Benutzerpasswortes';return true;" onMouseOut="window.status='';return true;"></td>
                  <td align="center"><input type="button"  value="&nbsp;&nbsp;&nbsp;&nbsp;Abmelden&nbsp;&nbsp;&nbsp;" onClick="go_to_url('logout')" class="button" name="button2" title="Von EBKuS abmelden." onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che zum Abmelden von der EBKuS - Anwendung';return true;" onMouseOut="window.status='';return true;"></td>
                  </tr>
                </table
                </tr>
              </table>
              </fieldset></td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</td>
</tr>
</table>
</form>
</BODY>
</HTML> """

administration_t="""
<BODY bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<form>
<table width="420" border="0" height="101" align="center">
  <tr>
    <td width="202" height="101" align="center" valign="middle" legend class="legendtext">
    <fieldset><legend class="legendtext">Mitarbeiter</legend>
      <table width="64%%" height="70" border="0">
        <tr>
          <td align="center" valign="middle" width="102">
            <input type="button" value="&nbsp;&nbsp;&nbsp;&nbsp;Neueintrag&nbsp;&nbsp;&nbsp;&nbsp;" class="button" onClick="go_to_url('mitneu')">
          </td>
        </tr>
        <tr>
          <td height="24" align="center" valign="middle" width="102">
            <input type="button" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&Auml;nderung&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button" onClick="go_to_url('mitausw')">
          </td>
        </tr>
      </table>
    </fieldset>
    </td>
    <td width="205" height="101" align="center" valign="middle" legend class="legendtext">
    <fieldset><legend class="legendtext">Akten</legend>
      <table width="55%%" border="0" height="70">
        <tr>
          <td height="28" align="center" valign="middle">
            <input type="button" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;L&ouml;schen&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button" onClick="go_to_url('rmakten')">
          </td>
        </tr>
      </table>
    </fieldset>
    </td>
  </tr>
  <tr>
    <td colspan="3" align="center" height="35" valign="middle" legend class="legendtext">
     <fieldset><legend class="legendtext">Bundesstatistik</legend>
      <table width="83%%" height="35" border="0">
        <tr>
          <td align="center" valign="middle" width="174">
             <input type="button"  value="&nbsp;&nbsp;&nbsp;&nbsp;Exportieren&nbsp;&nbsp;&nbsp;&nbsp;" class="button" onClick="go_to_url('formabfrjghexport')">
          </td>
          <td align="center" valign="middle" width="174">
            <input type="button" value="&nbsp;&nbsp;Downloadliste&nbsp;&nbsp;" class="button" onClick="go_to_url('jghexportlist')">
          </td>
        </tr>
      </table>
      </fieldset>
    </td>
  </tr>
  <tr>
    <td colspan="3" align="center" height="101" valign="middle" legend class="legendtext">
    <fieldset><legend class="legendtext">Kategorien</legend>
      <table width="83%%" height="70" border="0">
        <tr>
          <td align="center" valign="middle" width="174">
            <input type="button" name="Schaltfl&auml;che62" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Alle&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button" onClick="go_to_url('codelist')">
          </td>
          <td align="center" valign="middle" width="170">
          <input type="button"  value="&nbsp;&nbsp;Fachstatistik&nbsp;&nbsp;" class="button" onClick="go_to_url('codetab?tabelle=Fachstatistik')">
          </td>
        </tr>
        <tr>
          <td height="24" align="center" valign="middle" width="174">
      <input type="button" value="&nbsp;&nbsp;&nbsp;Leistungen&nbsp;&nbsp;&nbsp;" class="button" onClick="go_to_url('codetab?tabelle=Fachstatistikleistung')">
          </td>
          <td height="24" align="center" valign="middle" width="170">
            <input type="button"  value="&nbsp;&nbsp;&nbsp;&nbsp;Mitarbeiter&nbsp;&nbsp;&nbsp;&nbsp;" class="button" onClick="go_to_url('codetab?tabelle=Mitarbeiter')">
          </td>
        </tr>
      </table>
      </fieldset>
    </td>
  </tr>
  <tr>
    <td colspan="3" align="center" height="101" valign="middle" legend class="legendtext">
    <fieldset><legend class="legendtext">Protokoll</legend>
      <table width="83%%" height="70" border="0">
        <tr>
          <td align="center" valign="middle" width="174">
            <input type="button" name="Schaltfl&auml;che62" value="&nbsp;&nbsp;&nbsp;&nbsp;Archivieren&nbsp;&nbsp;&nbsp;&nbsp;" class="button" onClick="go_to_url('admin_protocol?auswahl=archiv')">
          </td>
</form>
          <td align="center" valign="middle" width="170">
          <form name="fuellgrenze" method="post" action="admin_protocol">
          <input type="text" value="%s" size="8" maxlength=9 name="grenze" class="textbox">
          <input type="hidden" name="auswahl" value="pgrenze">
          <input type="submit" name="Setzen" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Setzen&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
          </form>
          </td>
        </tr>
      </table>
      </fieldset>
    </td>
  </tr>
   <tr>
    <td colspan="3" align="center" height="53" valign="middle" legend class="legendtext">
      <fieldset>
      <form>
      <table width="83%%" height="35" border="0">
        <tr>
          <td align="center" valign="middle" width="174">
            <input type="button"  value="Passwort &auml;ndern" class="button" onClick="go_to_url('pwchange')">
          </td>
          <td align="center" valign="middle" width="174">
            <input type="button"  value="&nbsp;&nbsp;&nbsp;&nbsp;Abmelden&nbsp;&nbsp;&nbsp;&nbsp;" class="button" onClick="go_to_url('logout')">
          </td>
        </tr>
      </table>
      </form>
      </fieldset>
    </td>
  </tr>
</table>
</form>
</BODY>
"""

#dokumentation_t = """
#<th valign="top"><table><td>&#160;&#160;&#160;</td></tr></table>
#<th valign="top"><table>
#   <th align="center" bgcolor=#FFFFBB>
#   <big> <A name="Doc"> Dokumentation</A></big></th>
#   </tr><tr>
#   <td></td>
#   </tr><tr>
#   <td align="left"><B> ICD 10 </B> </td>
#   </tr><tr>
#   <td align="left" >&#160;&#160;&#160;
#   <A HREF="%sdoc/icd-10/index.html" target="_new">ICD-10 SGB V</A></td>
#    </tr><tr>
#   <td align="left"><B> EBKuS </B> </td>
#   </tr><tr>
#   <td align="left" >&#160;&#160;&#160;
#   <A HREF="%sdoc/ebkus/index.html" target="_new">Beschreibung</A></td>
#     </tr><tr>
#   </table></th>
#  <P>
#   """
