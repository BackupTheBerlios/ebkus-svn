# coding: latin-1

formhiddenvalues_t = """
<input type="hidden" value="%(file)s" name="file">
"""

formkopfv_t = """
<form action="%s">
"""

dokausgabe7_t = """
<div align="center">
<table width="80%%">
<tr>
<th align="left">%s</th>
</tr><tr>
<td><p>
<B>Suche</B> <input type="text" width="15" maxlength="60" value="%s" name="expr">
&#160;&#160;&#160;&#160;<input type="submit" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;">
</form>
</td></table>"""

dokausgabe1_t = """
<div align="center">
<table width="80%%">
<tr>
<th align="left">%s</th>
</tr><tr>
<td><p>
<dl>"""

dokausgabe2b_t = """
<dt> <A HREF="dokview?gruppeid=%(gruppe_id)d&dokid=%(id)d" target="_new">%(vd)d.%(vm)d.%(vy)d</A>:</dt>
<dd><B>%(art__name)s:</B> %(betr)s (%(mit_id__na)s)</dd>
"""

dokausgabe8_t = """
<dd>Zeile %s</dd>"""

dokausgabe2_t = """
<dt> <A HREF="dokview?fallid=%(fall_id)d&dokid=%(id)d" target="_new">%(vd)d.%(vm)d.%(vy)d</A>:</dt>
<dd><B>%(art__name)s:</B> %(betr)s (%(mit_id__na)s)</dd>
"""
dokausgabe3_t = """
</dl></p>
<p>
<hr>
</p></td>
"""