# coding: latin-1
gruppenkarte_t1 = """
</HEAD>
<body bgcolor="#CCCCCC" text="#000000" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
 <tr>
   <td align="center">
   <table width="95%" align="center">
"""


dokausgabe1_t = """
<tr>
<td class="legendtext" align="center" colspan="2">
<fieldset><legend class="legendtext">%s</legend>
<table width="95%%">
<tr>
<td class="legendtext" align="center" valign="middle">
"""

dokausgabe2b_ohne_edit_t = """
<table width="95%%">
  <tr>
    <td width="5%%" align="center"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv.gif"></td>
    <td width="5%%" align="center"><A HREF="dokview?gruppeid=%(gruppe_id)d&dokid=%(id)d" target="_new">
    <img border="0" src="/ebkus/ebkus_icons/view_details.gif"></A></td>
    <td  width="20%%" class="normaltext" bgcolor="#FFFFFF" align="center">%(vd)d.%(vm)d.%(vy)d</td>
    <td width="40%%" class="normaltext" bgcolor="#FFFFFF" align="center">%(art__name)s: %(betr)s</td>
    <td width="30%%" class="normaltext" bgcolor="#FFFFFF" align="center">%(mit_id__na)s</td>
  </tr>
</table>
"""

dokausgabe2b_mit_edit_t = """
<table width="95%%">
  <tr>
    <td width="5%%" align="center">
    <A HREF="gruppenkarte?gruppeid=%(gruppe_id)d&dokid=%(id)d&file=updgrverm">
    <img border="0" src="/ebkus/ebkus_icons/edit_button.gif"></A></td>
    <td width="5%%" align="center"><A HREF="dokview?gruppeid=%(gruppe_id)d&dokid=%(id)d" target="_new">
    <img border="0" src="/ebkus/ebkus_icons/view_details.gif"></A></td>
    <td  width="20%%" class="normaltext" bgcolor="#FFFFFF" align="center">%(vd)d.%(vm)d.%(vy)d</td>
    <td width="40%%" class="normaltext" bgcolor="#FFFFFF" align="center">%(art__name)s: %(betr)s</td>
    <td width="30%%" class="normaltext" bgcolor="#FFFFFF" align="center">%(mit_id__na)s</td>
  </tr>
</table>
"""

dokausgabe3_t = """
</td>
</tr>
<tr>
<td colspan="5">
&nbsp;
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""

dokausgabe4b_t = """
<table width="95%%">
  <tr>
    <td align="left" width="33%%" class="legendtext">Beraternotizen:</td>
    <td class="normaltext" width="16%%" align="right">TXT - Format </td>
    <td class="normaltext" width="17%%" align="left"><a href="dokview2?gruppeid=%(id)d&art=bnotiz" target="_new"><img  border="0" src="/ebkus/ebkus_icons/new_text_button.gif" width="19" height="19"></a></td>
    <td class="normaltext" width="17%%" align="right">PDF - Format </td>
    <td class="normaltext" width="17%%" align="left"><a href="printgr_pdf?gruppeid=%(id)d&art=bnotiz" target="_new"><img  border="0" src="/ebkus/ebkus_icons/show_pdf_button.gif" width="19" height="19"></a></td>
  </tr>
</table>
"""

dokausgabe5b_t = """
<table width="95%%">
  <tr>
    <td align="left" width="33%%" class="legendtext">Aktentexte:</td>
    <td class="normaltext" width="16%%" align="right">TXT - Format </td>
    <td class="normaltext" width="17%%" align="left"><a href="dokview2?gruppeid=%(id)d&art=anotiz" target="_new"><img  border="0" src="/ebkus/ebkus_icons/new_text_button.gif" width="19" height="19"></a></td>
    <td class="normaltext" width="17%%" align="right">PDF - Format </td>
    <td class="normaltext" width="17%%" align="left"><a href="printgr_pdf?gruppeid=%(id)d&art=anotiz" target="_new"><img border="0" src="/ebkus/ebkus_icons/show_pdf_button.gif" width="19" height="19"></a></td>
  </tr>
</table>

"""

dokausgabe6_t = """
</td>
</tr>
<tr>
<td colspan="2">
&nbsp;
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""
dokausgabe7_t = """
<tr>
<td class="legendtext" colspan="2">
<fieldset><legend class="legendtext">%s</legend>
  <table width="95%%" cellpadding="0" cellspacing="0">
    <form action="suchetxt" method="post">
    <tr>
      <td align="center" class="normaltext" valign="middle">
        <input type="text" class="textboxlarge" width="15" maxlength="60" value="%s" name="expr">
      </td>
      <td align="center" valign="middle">
      <input class="button" type="submit" value="Suchen">
      <td>
    </tr>
    <tr>
    <td>
    &nbsp;
    </td>
    </tr>
    </form>
  </table>
</fieldset>
</td>
</tr>
"""

teiln1_t = """
<table width="95%%" cellspacing="1" cellpadding="0">
<tr>
<td width="200" class="normaltext" align="center" bgcolor="#FFFFFF">
<A HREF="klkarte?akid=%(id)d">%(vn)s %(na)s</A></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF">%(str)s %(hsnr)s, %(plz)s, %(ort)s</td>
"""
teiln2_t = """
<td  width="150" class="normaltext" align="right" bgcolor="#FFFFFF">%(bgd)s.%(bgm)s.%(bgy)s-
%(ed)s.%(em)s.%(ey)s</td>
<td width="20">
<A HREF="updteiln?id=%(id)d&fallid=%(fall_id)d&gruppeid=%(gruppe_id)d">
<img border="0" src="/ebkus/ebkus_icons/teilnehmer_edit_button.gif"></A></td>
</tr>
</table>"""

teiln1b_t = """
<table width="95%%" cellspacing="1" cellpadding="0">
<tr>
<td width="200" bgcolor="#FFFFFF" align="center">
<A HREF="klkarte?akid=%(akte_id)d" class="normaltext">%(vn)s %(na)s</A></td>
<td class="normaltext" bgcolor="#FFFFFF">%(str)s %(hsnr)s, %(plz)s, %(ort)s</td>"""

teiln2b_t = """
<td  width="150" class="normaltext" bgcolor="#FFFFFF" align="right">%(bgd)s.%(bgm)s.%(bgy)s-
%(ed)s.%(em)s.%(ey)s
</td>
<td width="20">
<A HREF="updteiln?id=%(id)d&bezugspid=%(bezugsp_id)d&gruppeid=%(gruppe_id)d">
<img border="0" src="/ebkus/ebkus_icons/teilnehmer_edit_button.gif"></A></td>
</tr>
</table>"""

teiln3_t = """
</td>
</tr>
<tr>
<td>
&nbsp;
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""

gruppenkarte_ende_t = """
  </table>
  </td>
  </tr>
</table>
</body>
</html>"""