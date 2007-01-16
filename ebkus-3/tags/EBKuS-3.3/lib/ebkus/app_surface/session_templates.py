# coding: latin-1
from ebkus.app_surface.standard_templates import *

login_interface_t = """
</head>
<body bgcolor="#CCCCCC" onLoad="set_focus_login()" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="310" border="0" height="170" align="center">
  <tr>
    <td align="center" height="80">
    <a href="%(index_url)s"><img border="0" src="/ebkus/ebkus_icons/ebkus_logo.gif"></a>
    </td>
  </tr>
  <form name="logindaten" method="post" action="login">
    <tr>
      <td height="153" class="legendtext"><fieldset><b><legend>Benutzeranmeldung</legend></b>
        <table width="239" border="0" height="99" align="center">
          <tr>
            <td align="right" valign="middle" height="30" class="labeltext" width="132">
              Benutzername: </td>
            <td align="left" valign="middle" height="30" width="130">
              <input type="text" name="username" class="textbox" style="width:150px" size="18" maxlength=25 onMouseOver="window.status='Geben Sie hier bitte Ihren Benutzernamen ein.';return true;" onMouseOut="window.status='';return true;" title="Geben Sie hier bitte Ihren Benutzernamen ein.">
            </td>
          </tr>
          <tr>
            <td align="right" valign="middle" height="27" width="132" class="labeltext">
              Passwort: </td>
            <td align="left" valign="middle" height="27" width="130">
              <input type="password" name="pass" class="textbox" style="width:150px" size="18" maxlength=20 onMouseOver="window.status='Geben Sie hier bitte Ihr Benutzerpasswort ein.';return true;" onMouseOut="window.status='';return true;" title="Geben Sie hier bitte Ihr Benutzerpasswort ein.">
            </td>
          </tr>
          <tr align="center">
            <td valign="middle" height="38" colspan="2">
              <input type="submit" name="anmeldebutton" value="Anmelden" class="button">
            </td>
          </tr>
        </table>
        </fieldset> </td>
    </tr>
  </form>
</table>
</body>
</html>
"""

login_meldung_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="299" border="0" height="227" align="center">
  <tr>
    <td height="188"  class="legendtext" align="center"><fieldset><legend>Herzlich Willkommen!</legend>
        <table width="239" border="0" height="142" align="center">
          <tr>
            <td align="center" valign="middle" height="60" width="239" class="normaltext">
              Sie wurden als<br><br>
              %(na)s, %(vn)s<br><br>
              identifiziert.
          </td>
          </tr>
        </table>
        </fieldset>
     </td>
  </tr>
</table>
</body>
</html>
"""

























