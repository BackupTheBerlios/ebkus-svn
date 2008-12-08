//*************************************************************************
//
//  Javascript zum Darstellen eines Hilfebutton auf jeder Anwendungs-
//  seite.
//*************************************************************************

var ebkus_help_top_pos_setting=0
var IE  = (document.all)
var NS6 = (document.getElementById&&!document.all)
var NS  = (navigator.appName=="Netscape" && navigator.appVersion.charAt(0)=="4")

function view_help(url)
  {
  if(url!="nothing")
    {
    var winl = (screen.width-600)/2;
    var wint = (screen.height-400)/2;

    var settings  ='height=400,';
    settings     +='width=600,';
    settings     +='top='+wint+',';
    settings     +='left='+winl+',';
    settings     +='scrollbars=yes,';
    settings     +='resizable=no';
    DetailWindow = window.open(url, "ebkus_help",settings);
    DetailWindow.focus();
    }
  }

function add_ebkus_help()
  {
  var doc_title = document.title;
  while ( doc_title.search(/ /)!=-1  )
    {
    doc_title = doc_title.replace(/ /,"_");
    }
  if (IE||NS6)
    {
    document.write('<div ID="ebkus_help" style="visibility:hidden;Position:Absolute;Left:0px;Top:0;">');
    }
  if (NS)
    {
    document.write('<layer visibility="hide" top="0" name="ebkus_help" bgcolor="#CCCCCC" left="0">');
    }
  if (NS6)
    {
    document.write('<table border="0" cellpadding="0" cellspacing="0" width="39" bgcolor="#CCCCCC"><TR><TD>');
    }
  document.write('<table border="0" cellpadding="0" cellspacing="1" width="39" bgcolor="#CCCCCC">');
  document.write('<tr><td bgcolor="#CCCCCC" onmouseover="bgColor=\'#CCCCCC\'" \
                  onmouseout="bgColor=\'#CCCCCC\'" width="39"> \
                  <ilayer><layer onmouseover="bgColor=\'#CCCCCC\'" \
                  onmouseout="bgColor=\'#CCCCCC\'" width="100%" align="center">\
                  <div class="smalltext" align="center">\
                  <a href="#" onClick="view_help(\'ebkus_help?help_id='+ doc_title + '\')">\
                  <img src="/ebkus/ebkus_icons/help_button.gif" border="0" onMouseOver="window.status=\'F&uuml;r Hilfe zum Thema ' + document.title + ' bitte diese Schaltfl&auml;che bet&auml;tigen.\';return true;" onMouseOut="window.status=\'\';return true;" alt="F&uuml;r Hilfe zum Thema ' + document.title + ' bitte diese Schaltfl&auml;che bet&auml;tigen."></a>\
                  </div></layer></ilayer></td></tr></table>');
  if (NS6)
    {
    document.write('</td></tr></table>');
    }
  if (IE||NS6)
    {
    document.write('</div>');
    }
  if (NS)
    {
    document.write('</layer>');
    }
  if (NS6||IE||NS)
    {
    setTimeout('initialize_ebkus_help_moving();', 100);
    }
  }

function ebkus_help_moving()
  {
  if (NS6)
    {
    winY = window.pageYOffset;
    }
  if (IE)
    {
    winY = document.body.scrollTop;
    var NM = document.all('ebkus_help').style;
    }
  if (NS)
    {
    winY = window.pageYOffset;
    var NM=document.ebkus_help;
    }
  if (NS6||IE||NS)
    {
    if (winY!=ebkus_help_top_pos_setting&&winY>0)
      {
      sliding_range = .2 * (winY - ebkus_help_top_pos_setting);
      }
    else if (ebkus_help_top_pos_setting>0)
      {
      sliding_range = .2 * (winY - ebkus_help_top_pos_setting);
      }
    else
      {
      sliding_range=0;
      }
    if(sliding_range > 0)
      {
      sliding_range = Math.ceil(sliding_range);
      }
    else
      {
      sliding_range = Math.floor(sliding_range);
      }
    if (IE)
      {
      NM.pixelTop+=sliding_range;
      }
    if (NS6)
      {
      ebkus_help.top=parseInt(ebkus_help.top)+sliding_range+"px";
      }
    if (NS)
      {
      NM.top+=sliding_range;
      }
    ebkus_help_top_pos_setting = ebkus_help_top_pos_setting + sliding_range;
    setTimeout('ebkus_help_moving()', 1)
    }
  }

function initialize_ebkus_help_moving()
  {
  if (NS6)
    {
    ebkus_help=document.getElementById("ebkus_help").style
    ebkus_help.visibility="visible";
    ebkus_help.left = 0;
    }
  else if (IE)
    {
    ebkus_help.style.visibility = "visible"
    ebkus_help.style.pixelLeft = 0;
    }
  else if (NS)
    {
    document.ebkus_help.left = 0;
    document.ebkus_help.visibility = "show"
    }
    ebkus_help_moving();
  }


add_ebkus_help()