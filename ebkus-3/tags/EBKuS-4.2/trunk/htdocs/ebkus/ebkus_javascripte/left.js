var isExpanded   = false;

var imgOpened    = new Image(9,9);
imgOpened.src    = '/ebkus/ebkus_helppics/minus.gif';
var imgClosed    = new Image(9,9);
imgClosed.src    = '/ebkus/ebkus_helppics/plus.gif';


/**
 * Do reloads the frame if the window has been resized under Netscape4+
 *
 * @access  private
 */
function reDo() {
  if (innerWidth != origWidth || innerHeight != origHeight)
    location.reload(true);
} // end of the 'reDo()' function

/**
 * Positioned element resize bug under NS4+
 */
if (isNS4) {
  var origWidth  = innerWidth;
  var origHeight = innerHeight;
  onresize       = reDo;
}


/**
 * Gets the id of the first collapsible room
 *
 * @param  string  the name of the first collapsible room
 *
 * @return  integer  the index number corresponding to this room
 *
 * @access  public
 */
function nsGetIndex(el) {
  var ind       = null;
  var theLayers = document.layers;
  var layersCnt = theLayers.length;
  for (var i = 0; i < layersCnt; i++) {
    if (theLayers[i].id == el) {
      ind = i;
      break;
    }
  }
  return ind;
} // end of the 'nsGetIndex()' function


/**
 * Positions layers under NS4+
 *
 * @access  public
 */
function nsArrangeList() {
  if (firstInd != null) {
    var theLayers = document.layers;
    var layersCnt = theLayers.length;
    var nextY     = theLayers[firstInd].pageY + theLayers[firstInd].document.height;
    for (var i = firstInd + 1; i < layersCnt; i++) {
      if (theLayers[i].visibility != 'hide') {
        theLayers[i].pageY = nextY;
        nextY              += theLayers[i].document.height;
      }
    }
  }
} // end of the 'nsArrangeList()' function


/**
 * Expand databases at startup
 *
 * @access  public
 */
function nsShowAll() {
  var theLayers = document.layers;
  var layersCnt = theLayers.length;
  for (i = firstInd; i < layersCnt; i++) {
    theLayers[i].visibility = 'show';
  }
} // end of the 'nsShowAll()' function


/**
 * Collapses databases at startup
 *
 * @access  public
 */
function initIt()
{
  if (!capable || !isServer)
    return;

  else if (isIE4) {
    tempColl        = document.all.tags('DIV');
    var tempCollCnt = tempColl.length;
    for (var i = 0; i < tempCollCnt; i++) {
      if (tempColl(i).id == expandedDb)
        tempColl(i).style.display = 'block';
      else if (tempColl(i).className == 'child')
        tempColl(i).style.display = 'none';
    }
  } // end of the IE4 case
  else if (isNS4) {
    var theLayers  = document.layers;
    var layersCnt  = theLayers.length;
    for (var i = 0; i < layersCnt; i++) {
      if (theLayers[i].id == expandedDb)
        theLayers[i].visibility   = 'show';
      else if (theLayers[i].id.indexOf('Child') != -1)
        theLayers[i].visibility   = 'hide';
      else
        theLayers[i].visibility   = 'show';
    }
    nsArrangeList();
  } // end of the NS4 case
} // end of the 'initIt()' function


/**
 * Collapses/expands a database when the user require this to be done
 *
 * @param  string  the  name of the room to act on
 * @param  boolean whether to expand or to collapse the database content
 *
 * @access  public
 */
function expandBase(el, unexpand)
{
  if (!capable)
    return;


  else if (isIE4) {
    var whichEl = document.all(el + 'Child');
    var whichIm = document.images.item(el + 'Img');
    if (whichEl.style.display == 'none') {
      whichEl.style.display  = 'block';
      whichIm.src            = imgOpened.src;
    }
    else if (unexpand) {
      whichEl.style.display  = 'none';
      whichIm.src            = imgClosed.src;
    }
  } // end of the IE4 case
  else if (isNS4) {
    var whichEl = document.layers[el + 'Child'];
    var whichIm = document.layers[el + 'Parent'].document.images['imEx'];
    if (whichEl.visibility == 'hide') {
      whichEl.visibility  = 'show';
      whichIm.src         = imgOpened.src;
    }
    else if (unexpand) {
      whichEl.visibility  = 'hide';
      whichIm.src         = imgClosed.src;
    }
    nsArrangeList();
  } // end of the NS4 case
} // end of the 'expandBase()' function


/**
 * Add styles for positioned layers
 */
if (capable) {
  with (document) {
    // Brian Birtles : This is not the ideal method of doing this
    // but under the 7th June '00 Mozilla build (and many before
    // it) Mozilla did not treat text between <style> tags as
    // style information unless it was written with the one call
    // to write().
    if (isDOM) {
      var lstyle = '<style type="text\/css">'
                 + '<!--'
                 + 'div {color: #000000;}'
                 + '.heada {font-family: ' + fontFamily + '; font-size: 10pt}'
                 + '.heada_cnt {font-family: ' + fontFamily + '; font-size: 8pt}'
                 + '.parent {font-family: ' + fontFamily + '; color: #000000; text-decoration:none; display: block}'
                 + '.child {font-family: ' + fontFamily + '; font-size: 8pt; color: #000000; text-decoration:none; display: none}'
                 + '.item, .item:active, .item:hover, .tblItem, .tblItem:active {color: #000000; text-decoration: none; font-size: 8pt;}'
                 + '.tblItem:hover {color: #000000; text-decoration: underline}'
                 + '\/\/-->'
                 + '<\/style>';
      write(lstyle);
    }
    else {
      writeln('<style type="text\/css">');
      writeln('<!--');
      writeln('div {color: #000000; }');
      writeln('.heada {font-family: ' + fontFamily + '; font-size: 10pt}');
      writeln('.heada_cnt {font-family: ' + fontFamily + '; font-size: 8pt}');
      if (isIE4) {
        writeln('.parent {font-family: ' + fontFamily + '; color: #000000; text-decoration: none; display: block}');
        writeln('.child {font-family: ' + fontFamily + '; font-size: 8pt; color: #000000; text-decoration: none; display: none}');
        writeln('.item, .item:active, .item:hover, .tblItem, .tblItem:active {color: #000000; text-decoration: none; font-size: 8pt}');
        writeln('.tblItem:hover {color: #000000; text-decoration: underline}');
      }
      else {
        writeln('.parent {font-family: ' + fontFamily + '; color: #000000; text-decoration: none; position: absolute; visibility: hidden}');
        writeln('.child {font-family: ' + fontFamily + '; font-size: 8pt; color: #000000; position: absolute; visibility: hidden}');
        writeln('.item, .tblItem {color: #000000; text-decoration: none}');
      }
      writeln('\/\/-->');
      writeln('<\/style>');
    }
  }
}
else {
  with (document) {
    writeln('<style type="text\/css">');
    writeln('<!--');
    writeln('div {color: #000000; }');
    writeln('.heada {font-family: ' + fontFamily + '; font-size: 10pt}');
    writeln('.heada_cnt {font-family: ' + fontFamily + '; font-size: 8pt}');
    writeln('.parent {font-family: ' + fontFamily + '; color: #000000; text-decoration: none}');
    writeln('.child {font-family: ' + fontFamily + '; font-size: 8pt; color: #000000; text-decoration: none}');
    writeln('.item, .item:active, .item:hover, .tblItem, .tblItem:active {color: #000000; text-decoration: none}');
    writeln('.tblItem:hover {color: #000000; text-decoration: underline}');
    writeln('\/\/-->');
    writeln('<\/style>');
  }
} // end of adding styles


onload = initIt;
