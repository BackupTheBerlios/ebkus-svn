# coding: latin-1
from ebkus.app_surface.standard_templates import *

pass_change_t = """
</HEAD>
<BODY bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.passwort_daten.old_pass.focus()">
  <form name="passwort_daten" method="post" action="pw_make_change">
  <table width="375" border="0" height="305" align="center">
    <tr>
      <td height="188" class="legendtext">
        <fieldset><legend>Passwort &Auml;nderung</legend>
        <table width="315" border="0" height="142" align="center" valign="middle">
          <tr>
            <td align="right" valign="middle" height="32" width="163" class="labeltext">
              Benutzername: </td>
            <td align="left" valign="middle" height="32" width="135" class="labeltext">
              %(ben)s
            </td>
          </tr>
          <tr>
            <td align="right" valign="middle" height="37" width="163" class="labeltext">
              Vorname: </td>
            <td align="left" valign="middle" height="37" width="135" class="labeltext">
              %(vn)s
            </td>
          </tr>
          <tr>
            <td align="right" valign="middle" height="37" width="163" class="labeltext">
              Nachname: </td>
            <td align="left" valign="middle" height="37" width="135" class="labeltext">
              %(na)s
            </td>
          </tr>
          <tr>
            <td align="right" valign="middle" height="37" width="163" class="labeltext">
              Vorheriges Passwort:</td>
            <td align="left" valign="middle" height="37" width="135">
              <input type="password" name="old_pass" maxlength="20" class="textbox">
            </td>
          </tr>
          <tr>
            <td align="right" valign="middle" height="37" width="163" class="labeltext">
              Neues Passwort:</td>
            <td align="left" valign="middle" height="37" width="135">
              <input type="password" name="new_pass" maxlength="20" class="textbox">
            </td>
          </tr>
          <tr>
            <td align="right" valign="middle" height="37" width="163" class="labeltext">
              Wiederh. Neues Passwort:</td>
            <td align="left" valign="middle" height="37" width="135">
              <input type="password" name="repeat_pass" maxlength="20" class="textbox">
            </td>
          </tr>
          <tr align="center" background="">
              <td valign="middle" height="46">
                 <input type="submit" name="speichern" value="Speichern" class="button">
              </td>
              <td valign="middle" height="46">
                 <input type=button onClick="go_to_url('menu')" name="cancelbutton" value="&nbsp;&nbsp;&nbsp;Zur&uuml;ck&nbsp;&nbsp;&nbsp;"  class="button">
              </td>
          </tr>
        </table>
        </fieldset>
        </td>
    </tr>
</table>
</form>
</body>
</html>
"""