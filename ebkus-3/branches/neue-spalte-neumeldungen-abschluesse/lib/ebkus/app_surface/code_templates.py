# coding: latin-1
katuebersichtstart_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
<tr>
  <td align="center" valign="middle" width="34%%" class="legendtext">
    <fieldset>
    <table width="95%%">
      <tr height="40"><td align="center">
      <input type="button" value="Hauptmen&uuml;" class="button" onClick="go_to_url('menu')"></td></tr>
    </table>
    </fieldset>
  </td>
</tr>
  <tr>
    <td colspan="2" align="center"  class="legendtext"> <fieldset><legend class="legendtext">Gesamt&uuml;bersicht Kategorien</legend>
      <table width="95%">
        <tr align="left" bgcolor="#CCCCCC">
          <td width="20%" class="labeltext">Kategorie:</td>
          <td width="50%" class="labeltext">Dokumentation:</td>
          <td width="30%" class="labeltext">DB - Tabelle:</td>
        </tr>
        """
katuebersichtitem_t = """
        <tr>
          <td align="center"  class="normaltext" bgcolor="#FFFFFF"><A HREF="codelist#%(id)s">
            %(name)s</A></td>
          <td align="center"  class="normaltext" bgcolor="#FFFFFF">%(doku)s</td>
          <td align="center"  class="normaltext" bgcolor="#FFFFFF">"""

katuebersichtdbtabellen_t = """%(tab_id__name)s<br>"""

katuebersichtende_t = """
          </td>
        </tr>
      """

katuebersichtgesamtende_t = """
         <tr><td colspan="6">&nbsp;</td></tr>
         </table>
         </fieldset>
       </td>
     </tr>
"""

thkat_t = """
  <tr><a name="%(id)s">
    <td align="center" class="legendtext">
    <fieldset><legend class="legendtext">%(name)s</legend>
    <table width="95%%">
    <tr align="left" bgcolor="#CCCCCC">
      <td width="20%%" colspan="6" class="labeltext"><A HREF="codeneu?katid=%(id)s">
      <img border="0" src="/ebkus/ebkus_icons/neu_button.gif"></A></td>
    </tr>
    """

thcodeliste_t = """
    <tr>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Code:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Merkmal:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Sort:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Off:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Ab:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Dokumentation:</td>
    </tr>
    """

codelisten_t = """
    <tr>
      <td align="center"  class="normaltext" bgcolor="#FFFFFF"><A HREF="updcode?codeid=%(id)s"> %(code)s</A> </td>
      <td align="center"  class="normaltext" bgcolor="#FFFFFF"> %(name)s </td>
      <td align="center"  class="normaltext" bgcolor="#FFFFFF"> %(sort)s </td>
      <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(off)s </td>
      <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(dm)s%(sep)s%(dy)s </td>
      <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(dok)s </td>
    </tr>
    """

code_liste_ende = """
  <tr><td colspan="6">&nbsp;</td></tr>
  </table>
  </fieldset>
  </td></tr>
"""

hreftop_t = """
<tr>
  <td><A HREF="%s"><img border="0" src="/ebkus/ebkus_icons/button_go_top.gif"></A></td>
</tr>

"""

katuebersichtende2_t = """
</table>
</body>
</html>
"""

##############################
# Neuen Code eintragen
##############################

code_neu_start = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<form action="admin" method="post">
<table width="735" align="center">
"""

thcodeneu_t = """
  <tr>
    <td colspan="2" align="center" class="legendtext"> <fieldset><legend class="legendtext">Neuen Code f&uuml;r %(name)s anlegen</legend>
      <table width="95%%">"""

codeneu1_t = """
    <tr align="left" bgcolor="#CCCCCC">
    <td align="left" class="labeltext">Code:</td>
    <td align="left" class="labeltext">Merkmal:</td>
    <td align="left" class="labeltext">sort:</td>
    <td align="left" class="labeltext">Minimum:</td>
    <td align="left" class="labeltext">Maximum:</td>
    </tr>
    <tr>
    <td align="left"><input type="text" class="textboxmid" maxlength=8 name="code"></td>
    <td align="left"><input type="text" class="textboxlarge" maxlength=60 name="name"></td>
    <td align="left"><select name="sort" class="listbox30"> """

codeneu2_t = """
    <option value="%d" %s > %d """

codeneu3_t = """
    </select></td>
    <td align="left"><input type="text" class="textboxmid" maxlength=8 name="mini"></td>
    <td align="left"><input type="text" class="textboxmid" maxlength=8 name="maxi"></td>
    </tr>
    """
codeneu4_t = """
    <tr>
    <td colspan="5" align="left" class="labeltext">Dokumentation:</td>
    </tr>
    <tr><td colspan="5" align="left"><input type="text" class="textboxlarge" maxlength=255 name="dok"></td></tr>
    <tr><td colspan="5">&nbsp;</td></tr>
    </table>
    </td>
    </tr>
    """

thkat1_t = """
    <tr>
    <td align="center" class="legendtext">
    <fieldset><legend class="legendtext">Aktuelle Codeliste der Kategorie %(name)s</legend>
    <table width="95%%">
    """

thcodeliste1_t = """
     <tr>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Code:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Merkmal:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Sort:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Mini:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Maxi:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Off:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Ab:</td>
      <td align="left" class="labeltext" bgcolor="#CCCCCC">Dokumentation:</td>
    </tr>"""

codelisten1_t = """
    <tr>
    <td align="center"  class="normaltext" bgcolor="#FFFFFF"> %(code)s </td>
    <td align="center"  class="normaltext" bgcolor="#FFFFFF"> %(name)s </td>
    <td align="center"  class="normaltext" bgcolor="#FFFFFF"> %(sort)s </td>
    <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(mini)s </td>
    <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(maxi)s </td>
    <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(off)s </td>
    <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(dm)s%(sep)s%(dy)s </td>
    <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(dok)s </td>
    </tr> """

code_neu_ende = """
     <tr><td colspan="8">&nbsp;</td></tr>
     </table>
     </td>
     </tr>
     <tr>
        <td align="center" class="legendtext" valign="middle">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Hinzuf&uuml;gen" class="button">
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

##############################
# Code bearbeitern
##############################

code_bearb_start = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<form action="admin" method="post">
<table width="735" align="center">"""

thupdcode_t = """
  <tr>
    <td colspan="2" align="center" class="legendtext"> <fieldset><legend class="legendtext">Code
      aus %(name)s &auml;ndern</legend>
      <table width="95%%">
        """

updcode1_t = """
        <tr>
          <td align="left" class="labeltext" bgcolor="#CCCCCC">Code:</td>
          <td align="left" class="labeltext" bgcolor="#CCCCCC">Merkmal:</td>
          <td align="left" class="labeltext" bgcolor="#CCCCCC">Sort:</td>
          <td align="left" class="labeltext" bgcolor="#CCCCCC">Mini:</td>
          <td align="left" class="labeltext" bgcolor="#CCCCCC">Maxi:</td>
          <td align="left" class="labeltext" bgcolor="#CCCCCC">Off:</td>
          <td align="left" class="labeltext" bgcolor="#CCCCCC">Mon:</td>
          <td align="left" class="labeltext" bgcolor="#CCCCCC">Jahr:</td>
        </tr>
        <tr>
          <td align="left" class="normaltext"> %(code)s </td>
          <td align="left" class="normaltext">
            <input type="text" maxlength=60 value="%(name)s" name="name" class="textboxlarge">
          </td>
          <td align="left" class="normaltext">
            <select name="sort" class="listbox30">"""

updcode2_t = """
              <option value="%(sort)s" %(sel)s > %(sort)s """

updcode3_t = """
            </select>
          </td>
          <td align="left" class="normaltext">
            <input type="text" class="textboxmid" maxlength=8
    value="%(mini)s" name="mini">
          </td>
          <td align="left" class="normaltext">
            <input type="text" class="textboxmid" maxlength=8
    value="%(maxi)s" name="maxi">
          </td>
          """

updcode4_t = """
          <td align="left" class="normaltext"> Ja
            <input type="checkbox" value="1"  name="off"
    %(check)s >
          </td>
          """

updcode5_t = """
          <td align="left" class="normaltext">
            <input type="text" class="textboxsmall" size=2 maxlength=2 value="%(dm)s" name="dm">
          </td>
          <td align="left" class="normaltext">
            <input type="text" class="textboxmid" size=4 maxlength=4 value="%(dy)s" name="dy">
          </td>
        </tr>
        """

updcode6_t = """
        <tr>
          <td colspan="8" align="left" class="labeltext">Dokumentation:</td>
        </tr>
        <tr>
          <td colspan="8" align="left">
            <input class="textboxlarge" type="text" maxlength=255 value="%(dok)s" name="dok">
          </td>
        </tr>
      <tr><td colspan="8">&nbsp;</td></tr>
      </table>
      </td>
      </tr>
      """

thupdkat1_t = """
     <tr>
    <td align="center" class="legendtext">
    <fieldset><legend class="legendtext">Aktuelle Codeliste der Kategorie %(name)s</legend>
    <table width="95%%">"""

thupdcodeliste_t = """
          <tr>
            <td align="left" class="labeltext">Code:</td>
            <td align="left" class="labeltext">Merkmal:</td>
            <td align="left" class="labeltext">Sort:</td>
            <td align="left" class="labeltext">Mini:</td>
            <td align="left" class="labeltext">Maxi:</td>
            <td align="left" class="labeltext">Off:</td>
            <td align="left" class="labeltext">Ab:</td>
            <td align="left" class="labeltext">Dokumentation:</td>
          </tr>
          """

updcodeliste_t = """
          <tr>
            <td align="center"  class="normaltext" bgcolor="#FFFFFF"><A HREF="updcode?codeid=%(id)s"> %(code)s</A></td>
            <td align="center"  class="normaltext" bgcolor="#FFFFFF">%(name)s </td>
            <td align="center"  class="normaltext" bgcolor="#FFFFFF">%(sort)s </td>
            <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(mini)s </td>
            <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(maxi)s </td>
            <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(off)s </td>
            <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(dm)s%(sep)s%(dy)s </td>
            <td align="center"  class="normaltext" bgcolor="#FFFFFF">&#160; %(dok)s </td>
          </tr>"""

code_bearb_ende = """
     <tr><td colspan="8">&nbsp;</td></tr>
     </table>
     </td>
     </tr>
     <tr>
        <td align="center" class="legendtext" valign="middle">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Aktualisieren" class="button">
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

code_tab_start_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
<tr>
  <td align="center" valign="middle" width="34%%" class="legendtext">
    <fieldset>
    <table width="95%%">
      <tr height="40"><td align="center">
      <input type="button" value="Hauptmen&uuml;" class="button" onClick="go_to_url('menu')"></td></tr>
    </table>
    </fieldset>
  </td>
</tr>
"""
