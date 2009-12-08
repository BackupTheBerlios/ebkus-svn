
function ZeitAnzeigen() {
var Wochentagname =  new Array("Sonntag","Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag");

 var Jetzt = new Date();
 var Tag = Jetzt.getDate();
 var Monat = Jetzt.getMonth() + 1;
 var Jahr = Jetzt.getYear();
 if(Jahr < 999) Jahr += 1900;
 var Stunden = Jetzt.getHours();
 var Minuten = Jetzt.getMinutes();
 var Sekunden = Jetzt.getSeconds();
 var WoTag = Jetzt.getDay();
 var Vortag  = ((Tag < 10) ? "0" : "");
 var Vormon  = ((Monat < 10) ? ".0" : ".");
 var Vorstd  = ((Stunden < 10) ? "0" : "");
 var Vormin  = ((Minuten < 10) ? ":0" : ":");
 var Vorsek  = ((Sekunden < 10) ? ":0" : ":");
 var Datum = Vortag + Tag + Vormon + Monat  + "." + Jahr;
 var Uhrzeit = Vorstd + Stunden + Vormin + Minuten + Vorsek + Sekunden;
 var Gesamt = Wochentagname[WoTag] + ", " + Datum + ", " + Uhrzeit;
 document.getElementById("Uhr").firstChild.nodeValue = Gesamt
 window.setTimeout("ZeitAnzeigen()",1000);

}

function set_term_sum_fachstat(fieldname)
  {
  digit_test(document.fachstatform[fieldname].value,fieldname)
  document.fachstatform.kat.value =  eval(document.fachstatform.kkm.value)+
                                     eval(document.fachstatform.kkv.value)+
                                     eval(document.fachstatform.kki.value)+
                                     eval(document.fachstatform.kfa.value)+
                                     eval(document.fachstatform.kpa.value)+
                                     eval(document.fachstatform.ksoz.value)+
                                     eval(document.fachstatform.kleh.value)+
                                     eval(document.fachstatform.kerz.value)+
                                     eval(document.fachstatform.kkonf.value)+
                                     eval(document.fachstatform.kson.value);
  }

function digit_test(word,fieldname)
  {
  is_digit=true;
  if(word.length==0)
    {
    is_digit=false;
    }
  else
    {
    for(n=0;n<word.length;n++)
      {
      if(word.charAt(n)<"0" || word. charAt(n)>"9")
        {
        is_digit=false;
        }
      }
    }
  if(is_digit==false)
    {
    alert("Dies ist kein gültiger Wert. Er wird entfernt.");
    document.fachstatform[fieldname].value="0";
    this.focus();
    document.fachstatform[fieldname].focus();
    return false;
    }
 return true;
  }

function go_to_url(url)
  {
  // dann gehts in einem neuen Fenster auf
  if(url.indexOf("newXX ")==0)
  {
     window.open(url.substr(6, url.length));
     return true;        
  }
  if(url!="nothing")
    {
        window.location.href = url;
    }
  }

function view_details(url)
  {
  if(url!="nothing")
    {
    var winl = (screen.width-850)/2;
    var wint = (screen.height-250)/2;

    var settings  ='';
    settings     +='height=250,';
    settings     +='width=850,';
    settings     +='top='+wint+',';
    settings     +='left='+winl+',';
    settings     +='scrollbars=yes,';
    settings     +='resizable=no';
    DetailWindow = window.open(url, "Detailansicht", settings);
    DetailWindow.focus();
    }
  }

function set_focus_login()
  {
  document.logindaten.username.value='';
  document.logindaten.pass.value='';
  document.logindaten.username.focus();
  }

function Fehlermeldung(tb)
{
alert('Der Wert ' + tb.value + ' ist kein gültiges Datum.');
tb.value='';
this.focus();
tb.focus();
}


function PruefeDatum(tb,Startjahr,Endjahr,aktMonat,aktTag){
  var Date, Tag, Monat, Jahr, date_length, tageMonat;
  Date = tb.value;
  date_length = Date.length;

  if(Date != ""){
    // Punkteanzahl im Datumssstring
    var point_count = 0;
    // Positionen Punkte im Datumsstring
    var point_positions = new Array;
    //Enthält am Ende der Funktion das Datum in der korrekten Form
    var correct_date_temp = new Array;
    var year_start_pos;

    for(var str_pos = 0;str_pos < date_length; str_pos++){
      if(Date.charAt(str_pos)<"0" || Date.charAt(str_pos)>"9"){
        if(Date.substr(str_pos,1)=='.'){
          point_count++;
          if(point_count <= 2){
            point_positions[point_positions.length] = str_pos;
          }
        }
        else{
          Fehlermeldung(tb);
          return false;
        }
      }
    }
    if(point_count!=2){
      Fehlermeldung(tb);
      return false;
    }
    //Fall 1 Tag 1-stellig
    if(point_positions[0] == 1){
      correct_date_temp[correct_date_temp.length] = "0";
      correct_date_temp[correct_date_temp.length] = Date.substr(0,1);
      correct_date_temp[correct_date_temp.length] = ".";
      //Monat ist auch 1-stellig
      if(point_positions[1] == 3){
        correct_date_temp[correct_date_temp.length] = "0";
        correct_date_temp[correct_date_temp.length] = Date.substr(2,1);
        correct_date_temp[correct_date_temp.length] = ".";
        year_start_pos = 4;
      }
      //Monat ist 2-stellig
      else if(point_positions[1] == 4){
        correct_date_temp[correct_date_temp.length] = Date.substr(2,2);
        correct_date_temp[correct_date_temp.length] = ".";
        year_start_pos = 5;
      }
      //Punkt an ungueltiger Stelle
      else{
        Fehlermeldung(tb);
        return false;
      }
    }
    //Fall 2 Tag 2-stellig
    else if(point_positions[0] == 2){
      correct_date_temp[correct_date_temp.length] = Date.substr(0,2);
      correct_date_temp[correct_date_temp.length] = ".";
      //Monat ist 1-stellig
      if(point_positions[1] == 4){
        correct_date_temp[correct_date_temp.length] = "0";
        correct_date_temp[correct_date_temp.length] = Date.substr(3,1);
        correct_date_temp[correct_date_temp.length] = ".";
        year_start_pos = 5;
      }
      //Monat ist auch 2-stellig
      else if(point_positions[1] == 5){
        correct_date_temp[correct_date_temp.length] = Date.substr(3,2);
        correct_date_temp[correct_date_temp.length] = ".";
        year_start_pos = 6;
      }
      //Punkt an ungueltiger Stelle
      else{
        Fehlermeldung(tb);
        return false;
      }
    }
    //Jahr ist 1-stellig
    if(date_length - year_start_pos == 1){
      correct_date_temp[correct_date_temp.length] = "200";
      correct_date_temp[correct_date_temp.length] = Date.substr(year_start_pos,1);
    }
    //Jahr ist 2-stellig
    else if(date_length - year_start_pos == 2){
      if(Date.substr(year_start_pos,2)<=30){
        correct_date_temp[correct_date_temp.length] = "20";
        correct_date_temp[correct_date_temp.length] = Date.substr(year_start_pos,2);
      }
      else{
        correct_date_temp[correct_date_temp.length] = "19";
        correct_date_temp[correct_date_temp.length] = Date.substr(year_start_pos,2);
      }
    }
    //Jahr muss 4-stellig sein
    else if(date_length - year_start_pos == 4){
      correct_date_temp[correct_date_temp.length] = Date.substr(year_start_pos,4);
    }
    else{
      Fehlermeldung(tb);
      return false;
    }
    Date = correct_date_temp.join("");
    tb.value = Date;

    if (Date.length==10 && Date.substring(2,3)=="." && Date.substring(5,6)=="."){
      Tag=parseInt(Date.substring(0,2),10);
      Monat=parseInt(Date.substring(3,5),10);
      Jahr=parseInt(Date.substring(6,10),10);
    }
    else{
      Fehlermeldung(tb);
      return false;
    }
    if (Monat==4 || Monat==6 || Monat==9 || Monat==11){
      tageMonat=30;
    }
    else if (Monat==1 || Monat==3 || Monat==5 || Monat==7 || Monat==8 || Monat==10 || Monat==12){
      tageMonat=31;
    }
    else if(Monat==2 && Jahr%4==0 && Jahr%100!=0 || Jahr%400==0){
      tageMonat=29;
    }
    else if(Monat==2 && Jahr%4!=0 || Jahr%100==0 && Jahr%400!=0){
      tageMonat=28;
    }
    if (Tag>=1 && Tag<=tageMonat && Monat>=1 && Monat<=12 && Jahr>=Startjahr && Jahr<=Endjahr){
      return true;
    }
    else{
      Fehlermeldung(tb);
      return false;
    }
  }
}

function view_strkat()
  {
    str = _fetch("str");
    ort = _fetch("ort");
    plz = _fetch("plz");
    hsnr = _fetch("hsnr");
    ortsteil = _fetch("ortsteil");
    bezirk = _fetch("bezirk");
    samtgemeinde = _fetch("samtgemeinde");
    strkat_on = document.getElementsByName("strkat_on")[0];
    if (strkat_on.checked) 
    {
/*        var winl = (screen.width-740)/2;
        var wint = (screen.height-345)/2;
        
        var settings  ='height=345,';
        settings     +='width=740,';
        settings     +='top='+wint+',';
        settings     +='left='+winl+',';
        settings     +='scrollbars=no,';
        settings     +='resizable=no';
        
        DetailWindow = open('strkat',"Strassensuche",settings);
*/
        //ohne Settings einfach ein neues Fenster bzw. im Firefox ein Tab
        //Übergabe aller Parameter in der URL
        url = 'strkat?str=' + str + '&ort=' + ort + '&plz=' + plz + '&hsnr=' + hsnr;
        url += '&ortsteil=' + ortsteil + '&bezirk=' + bezirk + '&samtgemeinde=' + samtgemeinde;
        DetailWindow = open(url, "Straßensuche");
        DetailWindow.focus();
    }
  }

function submit_strkat()
{
   index = document.getElementsByName("strid")[0].options.selectedIndex;
   if (index == -1)
   {
      alert("Bitte Eintrag auswählen", "Fehler");
      return 0;
   }
   strasse = document.getElementsByName("strid")[0].options[index].value
   if (!strasse)
   {
      //alert("Bitte Eintrag auswählen", "Fehler");
      return 0;
   }
   array = strasse.split("#");
   _assign('str', array[0]);
   _assign('hsnr', array[1]);
   _assign('plz', array[2]);
   _assign('ort', array[3]);
   _assign('ortsteil', array[4]);
   _assign('samtgemeinde', array[5]);
   _assign('bezirk', array[6]);
   _assign('strid', array[7]);
   opener.document.getElementsByName("str")[0].focus();
   window.close();
}

function reset_strkat()
{
   _reset('strid');
   _reset('str');
   _reset('hsnr');
   _reset('plz');
   _reset('ort');
   _reset('ortsteil');
   _reset('samtgemeinde');
   _reset('bezirk');
   _reset('planungsr');
}
function _reset(name)
{
   try {
  document.getElementsByName(name)[0].value = ''
   } catch(e) {}
}

function _assign(name, value)
{
   try {
     opener.document.getElementsByName(name)[0].value = value;
   } catch(e) {}
}
function _fetch(name)
{
   try {
     return document.getElementsByName(name)[0].value;
   } catch(e) {}
   return '';
}

function warn_kein_strkat()
{
    strkat_on = document.getElementsByName("strkat_on")[0];
    if (strkat_on.checked == false) 
    { 
        text = "Bitte Straßenkatalog nur dann deaktivieren, wenn die Adresse\r\n";
        text += "- nicht bekannt, unvollständig oder falsch ist, oder\r\n";
        text += "- außerhalb des Geltungsbereichs des Staßenkatalogs liegt.\r\n";
        text += "In allen anderen Fällen führt eine erneute Suche mit weniger ";
        text += "restriktiven Suchkriterien fast immer zum Erfolg.\r\n";
        //alert(text);
        //confirm ging nicht richtig im IE
        text += "Wirklich Deaktivieren?";
        res = confirm(text);
        if(res == true)
        { 
           strkat_on.checked = false;
        } else
        {
           strkat_on.checked = true;
        }
    }               
        
}
function abfrage_bearbeiten(op)
{
    if (op == 'del' || op == 'edit')
    {
        index = document.getElementsByName("teilm")[0].options.selectedIndex;
        if (index == -1)
        {    
            alert("Bitte Eintrag auswählen", "Fehler");
            return 0;
        }
        abfr_id = document.getElementsByName("teilm")[0].options[index].value;
        if (!abfr_id)
        {
            alert("Bitte Eintrag auswählen", "Fehler");
            return 0;
        }
        url = 'abfragedef?abfrid=' + abfr_id + '&op=' + op;
    }
    else if (op == 'new')
    {
        url = 'abfragedef?op=new';
    }
    window.location.href = url;
}

function confirm_submit(msg, formname)
{
   res = window.confirm(msg);
   if (res)
   {
        document.getElementsByName("op")[0].value = "loeschen";
        document.forms[formname].submit();
   }       
}
function submit_abfragedef()
{
/*    
   index = document.getElementsByName("strid")[0].options.selectedIndex;
   if (index == -1)
   {
      alert("Bitte Eintrag auswählen", "Fehler");
      return 0;
   }
   strasse = document.getElementsByName("strid")[0].options[index].value
   if (!strasse)
   {
      //alert("Bitte Eintrag auswählen", "Fehler");
      return 0;
   }
*/
    document.abfragedef.submit();
        //window.close();
    return 0;
    
}
function del_anzahl_kontakte(ja_id, nein_id)
{
    select = document.getElementsByName("hda")[0];
    sel = select.options[select.selectedIndex].value;
    if (sel==ja_id)
    {
        document.getElementsByName("nbkges")[0].value = ''
    }
    else if (sel==nein_id)
    {
        document.getElementsByName("nbkakt")[0].value = ''
    }
}
