# coding: latin-1
formkopfdokneu_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<FORM ACTION="dokkarte" METHOD="post">
<table width="735" align="center">
 <tr>
 <td height="465" align="center" valign="top">
  <table border="0" cellpadding="1" width="95%%">
    <tr>
      <td width="95%%" align="center" class="legendtext" valign="top">
        <fieldset><legend class="legendtext">Klientendaten</legend>
          <table width="95%%" border="0" cellpadding="1">
            <tr>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Name:</td>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Geburtsdatum:</td>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Fallnummer:</td>
            <tr>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(akte_id__vn)s %(akte_id__na)s</td>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(akte_id__gb)s</td>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(fn)s</td>
              <input type="hidden" value="%(akte_id)d" name="akid">
              <input type="hidden" value="%(id)d" name="fallid">
            </tr>
            <tr><td colspan="3">&nbsp;</td></tr>
          </table>
        </fieldset>
       </td>
     </tr>
"""

formkopfdokgrneu_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<FORM ACTION="gruppenkarte" METHOD="post">
<table width="735" align="center">
 <tr>
    <td height="465" align="center" valign="top">
  <table border="0" cellpadding="1" width="95%%">
    <tr>
      <td width="95%%" class="legendtext" align="center" valign="top">
        <fieldset><legend class="legendtext">Gruppendaten</legend>
          <table width="95%%" border="0" cellpadding="1">
            <tr>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Gruppenname:</td>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Gruppenid:</td>
            </tr>
            <tr>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(name)s </td>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(gn)s</td>
              <input type="hidden" value="%(id)d" name="gruppeid">
            </tr>
            <tr><td colspan="2">&nbsp;</td></tr>
           </table>
        </fieldset>
       </td>
     </tr>
"""

vermneu_t = """
     <tr>
       <td width="95%%" class="legendtext" align="center" valign="top">
       <fieldset><legend class="legendtext">Betreff</legend>
          <table width="95%%" border="0" cellpadding="1">
            <tr>
              <td align="right" bgcolor="#CCCCCC" class="labeltext">Betreff:</td>
              <td align="left"  bgcolor="#CCCCCC"><input type="text" class="textboxlarge" maxlength=255 name="betr"></td>
              <td align="right" bgcolor="#CCCCCC" class="labeltext">Datum:</td>
              <td align="left"  bgcolor="#CCCCCC">
                <input type="text" class="textboxsmall" maxlength=2 size=2 value="%(day)d" name="vd">
              </td>
              <td align="left"  bgcolor="#CCCCCC">
              <B>.</B>
              </td>
              <td align="left"  bgcolor="#CCCCCC">
                <input type="text" class="textboxsmall" maxlength=2 size=2 value="%(month)d" name="vm">
              </td>
              <td align="left"  bgcolor="#CCCCCC">
              <B>.</B>
              </td>
              <td align="left"  bgcolor="#CCCCCC">
                <input type="text" class="textboxmid" maxlength=4 size=4 value="%(year)d" name="vy">
              </td>
           </tr>
         </table>
         </fieldset>
       </td>
     </tr>
     <tr>
       <td width="45%%" class="legendtext" align="center" valign="top">
       <fieldset><legend class="legendtext">Textinhalt</legend>
         <table width="95%%" border="0" cellpadding="1">
           <tr>
             <td align="center">
             <textarea class="textbox" style="width:400pt" wrap="off" rows="10" cols="70" name="text"></textarea>
              </td>
           </tr>
         </table>
         </fieldset>
       </td>
     </tr>"""

vermneu2_t = """
 <tr>
   <td width="45%%" class="legendtext" align="center" valign="top">
     <fieldset><legend class="legendtext">Festlegung des Texttyps</legend>
        <table width="95%%" border="0" cellpadding="1">
           <tr>
           <input type="hidden" name="mitid" value="%(id)s">
           <td align="center"><select name="art" class="listbox" style="width:400pt">"""

vermneu3_t = """
           </select></td>
           </tr>
        </table>
     </fieldset>
   </td>
 </tr>
  <tr>
    <td align="center" class="legendtext" valign="middle" colspan="2">
      <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="" value="Speichern" class="button">
             </td>
             <td align="center" valign="middle" width="33%%">
               <input type="reset" value="Zur&uuml;cksetzen" class="button">
              </td>
              <td align="center" valign="middle" width="34%%">
                <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
               </td>
             </tr>
           </table>
        </fieldset>
      </td>
    </tr>
 </table>
    </td>
    </tr>
  </table>
 </form>
 </body>
 </html>
"""

vermausw_t = """
    <tr>
      <td width="95%%" class="legendtext" align="center" valign="top">
        <fieldset><legend class="legendtext">Textauswahl</legend>
          <table width="95%%" border="0" cellpadding="1">
            <tr>
              <td align="center" bgcolor="#CCCCCC"><select class="listbox" style="width:400" width=400 name="dokid" size=15>"""

vermausw2_t = """
<option value="%(id)d"> %(vd)d.%(vm)d.%(vy)d | %(art__name)s | %(betr)s
"""

vermausw3_t = """ </select></td>
            </tr>
            <tr><td>&nbsp;</td></tr>
           </table>
        </fieldset>
       </td>
     </tr>
    <tr>
    <td align="center" class="legendtext" valign="middle" colspan="2">
      <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="" value="Bearbeiten" class="button">
             </td>
             <td align="center" valign="middle" width="33%%">
               <input type="reset" value="Zur&uuml;cksetzen" class="button">
              </td>
              <td align="center" valign="middle" width="34%%">
                <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
               </td>
             </tr>
           </table>
        </fieldset>
      </td>
    </tr>
    </table>
   </td>
  </tr>
 </table>
 </form>
 </body>
 </html>"""

vermupd_t = """
      <tr>
       <td width="95%%" class="legendtext" align="center" valign="top">
       <fieldset><legend class="legendtext">Betreff</legend>
          <table width="95%%" border="0" cellpadding="1">
            <tr>
              <td align="right" bgcolor="#CCCCCC" class="labeltext">Betreff:</td>
              <td align="left"  bgcolor="#CCCCCC"><input type="text" value="%(betr)s" class="textboxlarge" maxlength=255 name="betr"></td>
              <td align="right" bgcolor="#CCCCCC" class="labeltext">Datum:</td>
              <td align="left"  bgcolor="#CCCCCC" pre>
                <input type="text" class="textboxsmall" maxlength=2 size=2 value="%(vd)d" name="vd">
              </td>
              <td align="left"  bgcolor="#CCCCCC">
              <B>.</B>
              </td>
              <td align="left"  bgcolor="#CCCCCC" pre>
                <input type="text" class="textboxsmall" maxlength=2 size=2 value="%(vm)d" name="vm">
              </td>
              <td align="left"  bgcolor="#CCCCCC">
              <B>.</B>
              </td>
              <td align="left"  bgcolor="#CCCCCC" pre>
                <input type="text" class="textboxmid" maxlength=4 size=4 value="%(vy)d" name="vy">
              </td>
           </tr>
         </table>
         </fieldset>
       </td>
     </tr>
     <tr>
       <td width="45%%" class="legendtext" align="center" valign="top">
       <fieldset><legend class="legendtext">Textinhalt</legend>
         <table width="95%%" border="0" cellpadding="1">
           <tr>
             <td align="center">
             <textarea class="textbox" style="width:400pt" wrap="off" rows="10" cols="70" name="text">%(text)s</textarea>
              </td>
           </tr>
         </table>
         </fieldset>
       </td>
     </tr>"""

##*************************************************************************
## Upload



uploadformh_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<form action="%s" method="POST" enctype="multipart/form-data">
<table width="735" align="center">
 <tr>
   <td height="465" align="center" valign="top">
     <table border="0" cellpadding="1" width="95%%">
"""

formularh_t = """
       <tr>
         <td width="95%%" class="legendtext" align="center" valign="top">
         <fieldset><legend class="legendtext">Falldaten</legend>
         <table width="95%%" border="0" cellpadding="1">
            <tr>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Name:</td>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Geburtsdatum:</td>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Fallnummer:</td>
            <tr>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(akte_id__vn)s %(akte_id__na)s</td>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(akte_id__gb)s</td>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(fn)s</td>
              <input type="hidden" value="%(akte_id)d" name="akid">
              <input type="hidden" value="%(id)d" name="fallid">
            </tr>
            <tr><td colspan="3">&nbsp;</td></tr>
          </table>
         </fieldset>
         </td>
       </tr>
"""

formulargrh_t = """
 <tr>
         <td width="95%%" class="legendtext" align="center" valign="top">
         <fieldset><legend class="legendtext">Gruppendaten</legend>
         <table width="95%%" border="0" cellpadding="1">
            <tr>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Gruppenname:</td>
              <td align="left" bgcolor="#CCCCCC" class="labeltext">Gruppennummer:</td>
            <tr>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(name)s</td>
              <td align="center" bgcolor="#FFFFFF" class="normaltext">%(gn)s</td>
              <input type="hidden" value="%(id)d" name="gruppeid">
            </tr>
            <tr><td colspan="3">&nbsp;</td></tr>
          </table>
         </fieldset>
         </td>
       </tr>
"""

uploadform_t = """
<tr>
   <td width="95%%" class="legendtext" align="center" valign="top">
      <fieldset><legend class="legendtext">Betreff</legend>
          <table width="95%%" border="0" cellpadding="1">
            <tr>
              <td align="right" bgcolor="#CCCCCC" class="labeltext">Betreff:</td>
              <td align="left"  bgcolor="#CCCCCC"><input type="text" class="textboxlarge" maxlength=255 name="betr"></td>
              <td align="right" bgcolor="#CCCCCC" class="labeltext">Datum:</td>
              <td align="left"  bgcolor="#CCCCCC">
                <input type="text" class="textboxsmall" maxlength=2 size=2 value="%(day)d" name="vd">
              </td>
              <td align="left"  bgcolor="#CCCCCC">
              <B>.</B>
              </td>
              <td align="left"  bgcolor="#CCCCCC">
                <input type="text" class="textboxsmall" maxlength=2 size=2 value="%(month)d" name="vm">
              </td>
              <td align="left"  bgcolor="#CCCCCC">
              <B>.</B>
              </td>
              <td align="left"  bgcolor="#CCCCCC">
                <input type="text" class="textboxmid" maxlength=4 size=4 value="%(year)d" name="vy">
              </td>
           </tr>
           <tr><td colspan="8">&nbsp;</td></tr>
       </table>
    </fieldset>
  </td>
</tr>
<tr>
  <td width="95%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Hochzuladende Datei</legend>
    <table width="95%%" border="0" cellpadding="1">
      <tr>
        <td align="center" bgcolor="#CCCCCC" class="labeltext">
          Datei:<input name="datei" maxlength="1000000" type="file" size="30">
        </td>
      </tr>
      <tr><td>&nbsp;</td></tr>
    </table>
    </fieldset> </td>
</tr>
"""

uploadform2_t = """
<tr>
   <td width="45%%" class="legendtext" align="center" valign="top">
     <fieldset><legend class="legendtext">Festlegung des Dateityps</legend>
        <table width="95%%" border="0" cellpadding="1">
           <tr>
           <input type="hidden" name="mitid" value="%(id)s">
           <td align="center">
           <select name="art" class="listbox" style="width:400pt">
"""

uploadform3_t = """
           </select></td>
           </tr>
           <tr><td>&nbsp;</td></tr>
         </table>
      </fieldset>
   </td>
</tr>
 <tr>
    <td align="center" class="legendtext" valign="middle" colspan="2">
      <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="" value="Hochladen" class="button">
             </td>
             <td align="center" valign="middle" width="33%%">
               <input type="reset" value="Zur&uuml;cksetzen" class="button">
              </td>
              <td align="center" valign="middle" width="34%%">
                <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
               </td>
             </tr>
           </table>
        </fieldset>
      </td>
    </tr>
    </table>
   </td>
  </tr>
 </table>
 </form>
 </body>
 </html>
"""

##*************************************************************************
## Remove


rmverm_t = """
   <tr>
      <td width="95%%" class="legendtext" align="center" valign="top">
        <fieldset><legend class="legendtext">Vermerkauswahl</legend>
          <table width="95%%" border="0" cellpadding="1">
            <tr>
              <td align="center" bgcolor="#CCCCCC"><select class="listbox" style="width:400" name="dokids" size=15 multiple>"""

rmverm2_t = """
<option value="%(id)d"> %(vd)d.%(vm)d.%(vd)d | %(art__name)s | %(betr)s
"""

rmverm3_t = """ </select></td>
            </tr>
            <tr><td>&nbsp;</td></tr>
           </table>
        </fieldset>
       </td>
     </tr>
    <tr>
    <td align="center" class="legendtext" valign="middle" colspan="2">
      <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="" value="L&ouml;schen" class="button">
             </td>
             <td align="center" valign="middle" width="33%%">
               <input type="reset" value="Zur&uuml;cksetzen" class="button">
              </td>
              <td align="center" valign="middle" width="34%%">
                <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
               </td>
             </tr>
           </table>
        </fieldset>
      </td>
    </tr>
    </table>
   </td>
  </tr>
 </table>
 </form>
 </body>
 </html>"""