# coding: latin-1

strkat_start_t = """
<HTML>
<HEAD>
<meta http-equiv="expires" content="0">
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles.css">
<script type="text/javascript">
function strkat_hausnr(formname,fieldname)
{
   // 1. ---
   // 2. xa
   // 3. x

   var nr;
   var n_count;
   nr = document.forms[formname].elements[fieldname].value;
   n_count = 0;
   for(n=0;n<nr.length;n++)
   {
      if (nr.charAt(n) >= "a" && nr.charAt(n) <= "z")
      {
         n_count++;
      }
      else if ((nr.charAt(n) < "a" || nr.charAt(n) > "z") && (nr.charAt(n) < "0" || nr.charAt(n) > "9"))
      {
         n_count++;n_count++;
      }
   }

   if (n_count > 1)
   {
      //this.focus();
      alert ("Bitte gültigen Wert eintragen. z.B. 1, 10,100, 1a, 10a, 100a");
      document.forms[formname].elements[fieldname].value = "";
      this.focus();
      document.forms[formname].elements[fieldname].focus();
      return 0;
   }

   if (isNaN(nr))
   {
      n = nr.length;
      while(n < 4){
         nr = "0" + nr;
         n++;
      }
   }
   else
   {
      if (n == "") return 0;
      n = nr.length;
      while(n < 3){
         nr = "0" + nr;
         n++;
      }
   }
   document.forms[formname].elements[fieldname].value = nr;
}
function strkat_submit()
{
   var IE  = (document.all);
   var NS6 = (document.getElementById&&!document.all);
   var NS  = (navigator.appName=="Netscape" && navigator.appVersion.charAt(0)=="4");

   if (NS6)
   {
      index = document.strkat.strkat_list.options.selectedIndex;
      if (index == -1)
      {
         alert("Bitte Eintrag auswählen", "Fehler");
         return 0;
      }
      strasse = document.strkat.strkat_list.options[index].value;
      if (!strasse)
      {
         alert("Bitte Eintrag auswählen", "Fehler");
         return 0;
      }
   }
   else if (IE)
   {
      index = this.strkat.strkat_list.options.selectedIndex;
      if (index == -1)
      {
         alert("Bitte Eintrag auswählen", "Fehler");
         return 0;
      }
      strasse = this.strkat.strkat_list.options[index].value;
      if (!strasse)
      {
         alert("Bitte Eintrag auswählen", "Fehler");
         return 0;
      }
   }
   else if (NS)
   {
      index = document.strkat.strkat_list.options.selectedIndex;
      if (index == -1)
      {
         alert("Bitte Eintrag auswählen", "Fehler");
         return 0;
      }
      strasse = document.strkat.strkat_list.options[index].value;
      if (!strasse)
      {
         alert("Bitte Eintrag auswählen", "Fehler");
         return 0;
      }
   }

   array = strasse.split("#");
   if (opener.document.title == 'Neue Akte anlegen' || opener.document.title == 'Akte aktualisieren' || opener.document.title == 'Wiederaufnahme des Klienten')
   {
      opener.document.akteform.str.value ='';
      opener.document.akteform.strkat.value =array[0];
      opener.document.akteform.hsnr.value =array[1];
      opener.document.akteform.plz.value =array[2];
      opener.document.akteform.ort.value ='Berlin';
      opener.document.akteform.strkat.focus();
   }

   if (opener.document.title == 'Neue Bezugsperson eintragen' || opener.document.title == 'Bezugsperson bearbeiten')
   {
      opener.document.persform.str.value ='';
      opener.document.persform.strkat.value =array[0];
      opener.document.persform.hsnr.value =array[1];
      opener.document.persform.plz.value =array[2];
      opener.document.persform.ort.value ='Berlin';
      opener.document.persform.strkat.focus();
   }
   window.close();
}
</script>"""

strkat_main1_t = """
<title>EBKuS-Stra&szlig;enauswahl</title>
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.strkat.suche_strasse.focus()">
<table width="735" height="340" align="center">
 <tr>
    <td height="330" align="center" valign="top">
      <form name="strkat" method="post" action="strkat">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="200">
              <fieldset><legend class="legendtext">Suchangaben</legend>
              <table width="90%%" border="0" cellpadding="1" height="200">
                <tr>
                  <td width="37%%" align="right"> <span class="labeltext">Stra&szlig;e:</span></td>
                  <td width="63%%" align="left">
                    <input type="text" value="%s" size=10 maxlength=35 name="suche_strasse" class="textbox" onMouseOver="window.status='Bitte das Suchmuster f&uuml;r die Stra&szlig;e eintragen.';return true;" onMouseOut="window.status='';return true;" title="Bitte das Suchmuster f&uuml;r die Stra&szlig;e eintragen.">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle"> <span class="labeltext">Hausnummer:</span></td>
                  <td align="left" valign="middle">
                    <input type="text" value="%s" size=10 maxlength=5 name="suche_hausnr" class="textbox" onBlur="strkat_hausnr('strkat','suche_hausnr');" onMouseOver="window.status='Bitte das Suchmuster f&uuml;r die Hausnummer eintragen.';return true;" onMouseOut="window.status='';return true;" title="Bitte das Suchmuster f&uuml;r die Hausnummer eintragen.">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Postleitzahl:</td>
                  <td align="left" valign="middle" class="labeltext">
                    <input type="text" value="%s" size=10 maxlength=10 name="suche_plz" class="textbox" onMouseOver="window.status='Bitte das Suchmuster f&uuml;r die Postleitzahl eintragen.';return true;" onMouseOut="window.status='';return true;" title="Bitte das Suchmuster f&uuml;r die Postleitzahl eintragen.">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
            <td valign="top" align="center" class="legendtext" width="55%%" height="200">
              <fieldset><legend class="legendtext">Ergebnis der Abfrage</legend>
              <table border="0" cellpadding="0" width="311" height="200">
                <tr>
                <td class="labeltext" colspan=2>&nbsp;&nbsp;Stra&szlig;enname&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;HNr.&nbsp;&nbsp;&nbsp;&nbsp;Plz.&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Plr.
                </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext">&nbsp;</td>
                  <td align="left" valign="top">
                    <FONT FACE="courier" SIZE="2">
                    <select style="width:330" size="12" width=280 name="strkat_list" class="listbox2"  onMouseOver="window.status='In diesem Auswahlfeld werden alle Klienten aufgelistet, auf die Sie die entsprechenden Zugriffsrechte haben';return true;" onMouseOut="window.status='';return true;">"""

strkat_element_t = """
<option value="%(str_name)s#%(hausnr)s#%(plz)s#%(Plraum)s" >%(str_name2)s %(hausnr2)s %(plz2)s %(Plraum2)s
"""

strkat_main2_t = """
                </select>
                 </font>
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
                  <td width="50%%" align="center" valign="middle">
                    <input type="submit" name="" value="Stra&szlig;e suchen" class="button" onMouseOver="window.status='Stra&szlig;e suchen';return true;" onMouseOut="window.status='';return true;" title="Stra&szlig;e suchen">
                  </td>
                  <td align="center" valign="middle" width="25%%">
                    <input type="button" value="&Uuml;bernehmen" class="button" onClick="javascript:strkat_submit()" onMouseOver="window.status='Daten &uuml;bernehmen';return true;" onMouseOut="window.status='';return true;" title="Daten &uuml;bernehmen">
                  </td>
                  <td align="center" valign="middle" width="25%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:window.close()" onMouseOver="window.status='Schlie&szlig;en des Formulars';return true;" onMouseOut="window.status='';return true;" title="Schlie&szlig;en des Formulars">
                  </td>
                </tr>
              </table>
              </fieldset>
            </td>
          </tr>
        </table>"""

strkat_end_t = """
      </form>
    </td>
  </tr>
</table>
</body>
</html>"""
