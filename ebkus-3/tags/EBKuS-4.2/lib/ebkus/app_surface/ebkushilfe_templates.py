# coding: latin-1

help_frameset_t = """
<html>
<head>
<title>EBKuS-Hilfe</title>
</head>
<frameset cols="210,*" frameborder="yes" border="1" framespacing="0">
    <frame name="leftFrame" scrolling="yes" noresize src="ebkus_help_tree">
    <frame name="mainFrame" scrolling="yes" noresize src="ebkus_help_document?help_id=%s">
</frameset>
</html>
"""

help_tree_start_t = """
<HTML>
<HEAD>
<meta http-equiv="expires" content="0">
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
<script type="text/javascript" language="javascript">
    <!--
    var isDOM      = (typeof(document.getElementsByTagName) != 'undefined') ? 1 : 0;
    var isIE4      = ((typeof(document.all) != 'undefined') && (parseInt(navigator.appVersion) >= 4)) ? 1 : 0;
    var isNS4      = (typeof(document.layers) != 'undefined') ? 1 : 0;
    var capable    = (isDOM || isIE4 || isNS4) ? 1 : 0;
    // Uggly fix for Konqueror and Opera that are not fully DOM compliant
    if (capable && typeof(navigator.userAgent) != 'undefined') {
        var browserName = ' ' + navigator.userAgent.toLowerCase();
        if (browserName.indexOf('opera') > 0 || browserName.indexOf('konqueror') > 0) {
            capable = 0;
        }
    }
    var browserName = ' ' + navigator.userAgent.toLowerCase();
    if (browserName.indexOf('netscape6') > 0) {
            capable = 0;
    }
    var fontFamily = 'arial,verdana, helvetica, geneva, sans-serif';
    var isServer   = true;
    //-->
    </script>
    <script src="/ebkus/ebkus_javascripte/left.js" type="text/javascript" language="javascript1.2"></script>
</head>
<body bgcolor="#CCCCCC">
<div id="el1Parent" class="parent" style="margin-bottom: 5px">
    <a class="item" target="mainFrame" href="ebkus_help_document?help_id=start_seite">
      <font color="black" class="heada">
       <b>EBKuS-Hilfe</b>
      </font>
    </a>
  </div>
"""

help_tree_item_parent_t = """
  <div id="el%(p_nr)sParent" class="parent">
    <a class="item" href="#"
      onclick="if (capable) {expandBase('el%(p_nr)s', true); return false;}">
      <img border="0" name="imEx" id="el%(p_nr)sImg" src="/ebkus/ebkus_helppics/plus.gif" border="0" width="15" height="15"/>
    </a>
    <a class="item" target="mainFrame" href="ebkus_help_document?help_id=%(p_link)s" onclick="if (capable) {expandBase('el%(p_nr)s', false)}">
      <font color="black" class="heada">
       %(p_text)s
      </font>
    </a>
  </div>"""

help_tree_child_start_t = """
<div id="el%sChild" class="child" style="margin-bottom: 5px">
"""

help_tree_item_child_t = """
    <img border="0" src="/ebkus/ebkus_helppics/spacer.gif" border="0" width="12" height="15" alt=""/>
    <a target="mainFrame" href="ebkus_help_document?help_id=%(c_link)s">
      <img border="0" src="/ebkus/ebkus_helppics/browse.gif" border="0"/></a>
    <a class="tblItem" target="mainFrame" href="ebkus_help_document?help_id=%(c_link)s">
      %(c_text)s
    </a><br>"""

help_tree_child_end_t = """
</div>"""

help_tree_end_t = """
<script type="text/javascript" language="javascript1.2">
    <!--
    if (isNS4)
      {
      firstEl  = 'el1Parent';
      firstInd = nsGetIndex(firstEl);
      nsShowAll();
      nsArrangeList();
      }
    expandedDb = '';
    //-->
</script>
</body>
</html>
"""

help_document_start_t = """
<HTML>
<HEAD>
<meta http-equiv="expires" content="0">
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles_doc.css">
</head>
<body bgcolor="#FFFFFF">
<table width="100%% align="center">
 <tr>
   <td align="center" valign="top">
     <table width="95%%">"""

help_document_theme_t = """
        <tr>
          <td class="labeltext" height="2" bgcolor="#CCCCCC"><b>%s</b></td>
        </tr>
        <tr><td>&nbsp;</td></tr>"""

help_document_grafix_t = """
        <tr>
          <td align="center"><img border="0" src="/ebkus/ebkus_helppics/%s"></td>
        </tr>
        <tr><td align="center" class="smalltext">Grafische Darstellung</td></tr>
        <tr><td>&nbsp;</td></tr>"""

help_document_text_t = """
        <tr>
          <td class="normaltext"><p align=justify>%s</p></td>
        </tr>"""

help_document_back_t = """
        <tr>
          <td class="normaltext" align="center">
            <form>
              <input type="button" onClick="javascript:history.back()" class="button" value="Zur&uuml;ck">
            </form>
          </td>
        </tr>"""

help_document_end_t = """
      </table>
    </td>
  </tr>
</table>
</body>
</html>"""
