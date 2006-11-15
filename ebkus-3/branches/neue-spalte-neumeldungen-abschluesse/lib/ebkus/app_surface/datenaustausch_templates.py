# coding: latin-1
jghexportfeedback_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td align="center" valign="top">
      <table border="0" cellpadding="1" width="95%%">
        <tr>
          <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Exportdatei
            der Bundesjugendhilfestatistik %(jahr)s</legend>
            <table width="90%%" border="0" cellpadding="1" height="50">
              <tr>
                <td align="center"> <A class="legendtext" HREF="%(jgh_url)s">%(jgh_filename)s</A>
                </td>
              </tr>
            </table>
            </fieldset> </td>
        </tr>
        <tr>
          <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Protokolldatei
            der Bundesjugendhilfestatistik %(jahr)s</legend>
            <table width="90%%" border="0" cellpadding="1" height="50">
              <tr>
                <td align="center"> <A class="legendtext" HREF="%(jgh_log_url)s">%(jgh_log_filename)s</A>
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
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
      </table>
  </tr>
</table>
"""


thjghexportliste_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td align="center" valign="top">
      <table border="0" cellpadding="1" width="95%%">
        <tr>
          <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Liste aller Exportdateien</legend>
            <table width="90%%" border="0" cellpadding="1" height="50">"""

jghexportliste_t = """
              <tr>
                <td align="center" width="95%%" class="normaltext" bgcolor="#FFFFFF"><A HREF="%s">%s</A></td>
              </tr>"""

jghexportliste_ende_t = """
            <tr><td>&nbsp;</td></tr>
            </table>
          </td>
        </tr>
        <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
     </table>
   </td>
 </tr>
</table>
</body>
</html>"""

formexport_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td align="center" valign="top" height="155">
      <form action="stellenabgleich" method="post">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="55">
              <fieldset><legend class="legendtext">Auswahl der Export- oder Importfunktion</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="21%" align="right" class="labeltext">Protokoll:</td>
                  <td width="4%">
                    <input type="radio" value="l" name="dbexport" checked>
                  </td>
                  <td width="25%" align="right" class="labeltext">Import:</td>
                  <td width="5%">
                    <input type="radio" value="i" name="dbexport">
                  </td>
                  <td width="27%" align="right" class="labeltext">Export:</td>
                  <td width="18%">
                    <input type="radio" value="e" name="dbexport">
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td align="center" valign="middle" width="50%%">
                    <input type="submit" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
                  </td>
                  <td align="center" valign="middle" width="50%%">
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
</html>"""



thexport_start_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td align="center" valign="top">
      <table border="0" cellpadding="1" width="95%%">"""

thexport_t = """
        <tr>
          <td width="45%%" class="legendtext" align="center" valign="top"><fieldset><legend class="legendtext">%s</legend>
            <table width="95%%" border="0" cellpadding="1" height="50">
              <tr>
                <td class="labeltext">Am:</td>
                <td class="labeltext">Von:</td>
                <td class="labeltext">Stelle:</td>
              </tr>
              """

export_t = """
              <tr>
                <td class="normaltext" bgcolor="#FFFFFF"> %(datum)s </td>
                <td class="normaltext" bgcolor="#FFFFFF"> %(mit_id__na)s </td>
                <td class="normaltext" bgcolor="#FFFFFF"> %(dbsite__name)s </td>
              </tr>
              """

thexport_ende_t = """
            <tr><td>&nbsp;</td></tr>
            </table>
          </td>
        </tr>
        <tr>
          <td align="center" class="legendtext" valign="middle" colspan="2"> <fieldset>
            <table width="95%" border="0" cellpadding="1">
              <tr height="40">
                <td align="center" valign="middle" width="100%">
                  <input type="button" value="Hauptmen&uuml;" class="button" onClick="go_to_url('menu')" name="button">
                </td>
              </tr>
            </table>
            </fieldset> </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
"""
