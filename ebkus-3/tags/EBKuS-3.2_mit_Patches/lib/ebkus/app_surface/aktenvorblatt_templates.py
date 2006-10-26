# coding: latin-1
#####################
# Aktenvorblatt
#####################

vkopf_t = """
</head>
<body bgcolor="#FFFFFF">
<table align="center" bgcolor="#CCCCCC" width="95%%">
  <tr>
    <td colspan="3">
      <table border=1 cellpadding="0" cellspacing="0" width=100%% bordercolor="#CCCCCC">
        <tr>
          <td class="legendtext" colspan="9">Aktenvorblatt vom %(day)d.%(month)d.%(year)d</td>
        </tr>
        """

vakten1_t = """
        <tr>
          <th align="center" colspan=9 class="legendtext">Eltern, Geschwister,
            Verwandte</th>
        <tr valign="top">
          <th bgcolor="#FFFFFF" align="left" class="legendtext" width=3%% >Vrw.:</th>
          <th bgcolor="#FFFFFF" align="left" class="legendtext" width=15%% >Vorname:</th>
          <th bgcolor="#FFFFFF" align="left" class="legendtext" width=25%% >Name:</th>
          <th bgcolor="#FFFFFF" align="left" class="legendtext" width=6%% >Geb.:</th>
          <th bgcolor="#FFFFFF" align="left" class="legendtext" width=30%%> Str.:</th>
          <th bgcolor="#FFFFFF" align="left" class="legendtext" width=6%% >Plz.:</th>
          <th bgcolor="#FFFFFF" align="left" class="legendtext" width=5%% >Ort:</th>
          <th bgcolor="#FFFFFF" align="left" class="legendtext" width=8%% >Telefon1:</th>
          <th bgcolor="#FFFFFF" align="left" class="legendtext" width=8%% >Telefon2:</th>
        </tr>
        <tr valign="top">
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="legendtext">Klient</td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;%(vn)s</td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;%(na)s</td>
          <td bgcolor="#FFFFFF" align="center" valign="middle"class="normaltext">&#160; %(gb)s</td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(str)s %(hsnr)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(plz)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(ort)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle"class="normaltext">&#160; %(tl1)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(tl2)s
          </td>
        </tr>
        """

vakten2_t = """
        <tr valign="top">
          <td bgcolor="#FFFFFF" align="left" cellpadding=0>&#160;</td>
          <td bgcolor="#FFFFFF" align="left" valign="middle" class="smalltext" colspan=3>&#160;Ausbildung:%(ber)s</td>
          <td bgcolor="#FFFFFF" align="left" valign="middle" class="smalltext" colspan=2>&#160;bei
            %(fs__name)s</td>
          <td bgcolor="#FFFFFF" align="rigth" valign="middle" class="smalltext" colspan=3>&#160;%(nobedakte)s</td>
        </tr>
        """

vbezugspersonen1_t = """
        <tr valign="top">
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="legendtext">&#160;%(verw__name)s</td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;%(vn)s</td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;%(na)s</td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(gb)s</td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(str)s %(hsnr)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(plz)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(ort)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(tl1)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(tl2)s
          </td>
        </tr>
        """

vbezugspersonen2_t = """
        <tr valign="top">
          <td bgcolor="#FFFFFF" align="left" cellpadding=0>&#160;</td>
          <td bgcolor="#FFFFFF" align="left" valign="middle" class="smalltext" colspan=3>&#160;Beruf/Ausbildung:%(ber)s</td>
          <td bgcolor="#FFFFFF" align="left" valign="middle" class="smalltext" colspan=2>&#160;bei
            %(fs__name)s</td>
          <td bgcolor="#FFFFFF" align="rigth" valign="middle" class="smalltext" colspan=3>&#160;%(nobed__name)s</td>
        </tr>
        """

vbezugspersonenzeile_t = """
        <tr valign="top">
          <td bgcolor="#FFFFFF" colspan="9" align="left">&#160; </td>
        </tr>
        <tr valign="top">
          <td bgcolor="#FFFFFF" colspan="9" align="left">&#160; </td>
        </tr>
        <tr valign="top">
          <td bgcolor="#FFFFFF" colspan="9" align="left">&#160; </td>
        </tr>
        <tr valign="top">
          <td bgcolor="#FFFFFF" colspan="9" align="left">&#160; </td>
        </tr>
        """

veinrichtungs_kopf1_t = """
      </table>
    </td>
  </tr>
  <tr>
    <td colspan="3">
      <table border=1 cellpadding="0" cellspacing="0" width=100%% bordercolor="#CCCCCC">
        <tr bgcolor="#CCCCCC">
          <th align="center" class="legendtext" valign="middle" colspan=5>Einrichtungskontakt</th>
          """

veinrichtungs_kopf2_t = """
        <tr>
          <th bgcolor="#FFFFFF" class="legendtext" valign="middle" align="left">Art:</th>
          <th bgcolor="#FFFFFF" class="legendtext" valign="middle" align="left">Name, Adresse,
            Ansprechperson:</th>
          <th bgcolor="#FFFFFF" class="legendtext" valign="middle" align="left">Telefon1:</th>
          <th bgcolor="#FFFFFF" class="legendtext" valign="middle" align="left">Telefon2:</th>
          <th bgcolor="#FFFFFF" class="legendtext" valign="middle" align="left">Aktuell:</th>
        </tr>
        """

veinrichtung_t = """
        <tr>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext"> %(insta__name)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(na)s
            &#160;&#160;&#160;&#160;&#160;&#160;%(nobed__name)s </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(tl1)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(tl2)s
          </td>
          <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160; %(status__code)s
          </td>
        </tr>
        """

veinrichtungszeile_t = """
        <tr>
          <td align="center" colspan="5" class="normaltext" bgcolor="#FFFFFF">&#160;
          </td>
        </tr>
         <tr>
          <td align="center" colspan="5" class="normaltext" bgcolor="#FFFFFF">&#160;
          </td>
        </tr>
        <tr>
          <td align="center" colspan="5" class="normaltext" bgcolor="#FFFFFF">&#160;
          </td>
        </tr>
        """

vanmeldung_kopf_t = """
      </table>
    </td>
  </tr>
  <tr>
    <td colspan="3">
      <table border=1 cellpadding="0" cellspacing="0" width=100%% bordercolor="#CCCCCC">
        <tr bgcolor="#CCCCCC">
          <th align="center" class="legendtext" valign="middle" colspan=2 >Anmeldeinformation</th>
          """

vanmeldung_t = """
        <tr bgcolor="#FFFFFF">
          <td align="right" valign="middle" class="legendtext">Gemeldet von:</td>
          <td align="left" valign="middle" width=100%% class="normaltext">&#160; %(von)s am&#160;
            %(ad)d.%(am)d.%(ay)d. Telefon:&#160; %(mtl)s &#160;&#160;&#160;&#160;&#160;
            %(nobedanm)s </td>
        </tr>
        <tr bgcolor="#FFFFFF">
          <td align="right" valign="middle" class="legendtext">&#160;Zugangsmodus:</td>
          <td align="left" valign="middle" class="normaltext">&#160; %(zm__name)s&#160; auf Empfehlung
            von %(me)s</td>
        </tr>
        <tr bgcolor="#FFFFFF">
          <td align="right" valign="middle" class="legendtext">&#160;Anmeldegrund:</td>
          <td align="left" valign="middle" class="normaltext">&#160; %(mg)s </td>
        </tr>
        """

vleistungs_kopf_t = """
      </table>
    </td>
  </tr>
  <tr valign="top">
  <td width="34%%" align="center">
    <table border=1 cellpadding="0" cellspacing="0" width=100%% bordercolor="#CCCCCC">
      <tr bgcolor="#CCCCCC">
        <th align="center" colspan="4" valign="middle" class="legendtext"> Leistung
        </th>
      <tr bgcolor="#FFFFFF">
        <td align="left" class="legendtext" valign="middle" width="30%%">Mitarbeiter:</td>
        <td align="left" class="legendtext" valign="middle" width="26%%">Leistung:</td>
        <td align="left" class="legendtext" valign="middle" width="35%%">Am:</td>
        <td align="left" class="legendtext" valign="middle" width="9%%">Bis:</td>
      </tr>
      """

vleistungs_t = """
      <tr bgcolor="#FFFFFF">
        <td align="center" class="normaltext" valign="middle" width="30%%">&#160;
          %(mit_id__na)s </td>
        <td align="center" class="normaltext" valign="middle" width="26%%">&#160;
          %(le__name)s </td>
        <td align="center" class="normaltext" valign="middle" width="35%%">&#160;
          %(bgd)d.%(bgm)d. %(bgy)d </td>
        """

vleistungsendeleer_t = """
        <td align="left" class="normaltext" width="9%%">&#160; </td>
      </tr>
      """

vleistungsendedatum_t = """
      <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext" width="30%%">&#160;
        %(ed)d.%(em)d. %(ey)d </td>
      </tr>
      """

vleistungszeile_t = """
      <tr>
        <td bgcolor="#FFFFFF" colspan="4" valign="middle" align="center" class="legendtext">&#160;
        </td>
      </tr>
      <tr>
        <td bgcolor="#FFFFFF" colspan="4" valign="middle" align="center" class="legendtext">&#160;
        </td>
      </tr>
      <tr>
        <td bgcolor="#FFFFFF" colspan="4" valign="middle" align="center" class="legendtext">&#160;
        </td>
      </tr>
      """

vbearbeiter_kopf_t = """
    </table>
  </td>
</tr>
<tr>
  <td>
    <table border=1 cellpadding="0" cellspacing="0" width=100%% bordercolor="#CCCCCC">
      <tr bgcolor="#CCCCCC">
        <td align="center" class="legendtext" valign="middle" colspan="3">Bearbeiter
      </tr>
      <tr>
        <th bgcolor="#FFFFFF" align="left" valign="middle" class="legendtext">Bearbeiter:</th>
        <td bgcolor="#FFFFFF" align="left" valign="middle" class="legendtext">Beginn:
        <td bgcolor="#FFFFFF" align="left" valign="middle" class="legendtext">Ende:
      </tr>
      """

vbearbeiter_t = """
      <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;
          %(mit_id__na)s </td>
        <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;
          %(bgd)d.%(bgm)d. %(bgy)d </td>
        """

vbearbeiterendeoffen_t = """
        <td bgcolor="#FFFFFF" align="center" class="normaltext">&#160; </td>
      </tr>
      """
vbearbeiterendedatum_t = """
      <td bgcolor="#FFFFFF" align="center" cvalign="middle" class="normaltext">&#160;
        %(ed)d.%(em)d. %(ey)d </td>
      </tr>
      """

vbearbeiterzeile_t = """
      <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" colspan="3" class="normaltext">&#160;
        </td>
      </tr>
       <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" colspan="3" class="normaltext">&#160;
        </td>
      </tr>
       <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" colspan="3" class="normaltext">&#160;
        </td>
      </tr>
      """

vfall_kopf_t = """
    </table>
  </td>
</tr>
<tr>
  <td>
    <table border=1 cellpadding="0" cellspacing="0" width=100%% bordercolor="#CCCCCC">
      <th align="center" colspan=3 width=100%% class="legendtext"> Stand </th>
      </tr>
      <tr>
        <th bgcolor="#FFFFFF" align="left" valign="middle" class="legendtext">Fallnr.:</th>
        <th bgcolor="#FFFFFF" align="left" valign="middle" class="legendtext">Beginn:</th>
        <th bgcolor="#FFFFFF" align="left" valign="middle" class="legendtext">z.d.A.:</th>
      </tr>
      """

vfall_t = """
      <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;
          %(fn)s </td>
        <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;
          %(bgd)d.%(bgm)d. %(bgy)d </td>
        """

vfalloffen_t = """
        <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;</td>
      </tr>
      """

vfallendedatum_t = """
      <td bgcolor="#FFFFFF" align="center" valign="middle" class="normaltext">&#160;
        %(zdad)d.%(zdam)d. %(zday)d </td>
      </tr>
      """

vfallzeile_t = """
      <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" colspan="3" class="normaltext">&#160;
        </td>
      </tr>
      <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" colspan="3" class="normaltext">&#160;
        </td>
      </tr>
      <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" colspan="3" class="normaltext">&#160;
        </td>
      </tr>
      """

vtabende_t = """
    </table>
  </td>
</tr>"""


vnotiz_t = """
  <tr>
    <td colspan="3">
    <table border=1 cellpadding="0" cellspacing="0" width=100%% bordercolor="#CCCCCC">
      <th bgcolor="#CCCCCC" align="center" class="legendtext">Notizen</th>
"""
vnotizakte_t = """
<tr>
<td bgcolor="#FFFFFF" align="left" class="normaltext">%(vn)s %(na)s:%(no)s
</tr>"""

vnotizbperson_t ="""
<tr>
<td bgcolor="#FFFFFF" align="left" class="normaltext">%(vn)s %(na)s:%(no)s
</tr>"""
vnotizeinr_t ="""
<tr>
<td bgcolor="#FFFFFF" align="left" class="normaltext">%(insta__name)s %(na)s: %(no)s</td>
</tr>"""
vnotizanm_t ="""
<tr>
<td bgcolor="#FFFFFF" align="left" class="normaltext">Anmeldung: %(no)s</td>
</tr>"""
klkartegruppef_t = """
<tr>
<td bgcolor="#FFFFFF" align="left" class="normaltext">%(akte_id__vn)s %(akte_id__na)s:"""
klkartegruppe_t = """
 Gruppenkarte-Nr.: %(gruppe_id__gn)s</td></tr>"""
klkartegruppeb_t = """
<tr>
<td bgcolor="#FFFFFF" align="left" class="normaltext">%(vn)s %(na)s:"""

vnotizende_t = """
     <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" colspan="3" class="normaltext">&#160;
        </td>
      </tr>
      <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" colspan="3" class="normaltext">&#160;
        </td>
      </tr>
      <tr>
        <td bgcolor="#FFFFFF" align="center" valign="middle" colspan="3" class="normaltext">&#160;
        </td>
      </tr>
     </table>
   </td>
  </tr>
  <tr>
  <form>
   <td bgcolor="#FFFFFF" align="center">
    &nbsp;<!--<input type="button" class="button" value="Zur&uuml;ck" onClick="javascript:history.back()">-->
   </td>
  </form>
  </tr>
</table>
</body>
</html>"""