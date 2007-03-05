
var DHTML = 0, DOM = 0, MS = 0, NS = 0, OP = 0;

function DHTML_init() {

 if (window.opera) {
     OP = 1;
 }
 if(document.getElementById) {
   DHTML = 1;
   DOM = 1;
 }
 if(document.all && !OP) {
   DHTML = 1;
   MS = 1;
 }
if(document.layers && !OP) {
   DHTML = 1;
   NS = 1;
 }
}

function getElem(p1,p2,p3) {
 var Elem;
 if(DOM) {
   if(p1.toLowerCase()=="id") {
     if (typeof document.getElementById(p2) == "object")
     Elem = document.getElementById(p2);
     else Elem = void(0);
     return(Elem);
   }
   else if(p1.toLowerCase()=="name") {
     if (typeof document.getElementsByName(p2) == "object")
     Elem = document.getElementsByName(p2)[p3];
     else Elem = void(0);
     return(Elem);
   }
   else if(p1.toLowerCase()=="tagname") {
     if (typeof document.getElementsByTagName(p2) == "object" || (OP && typeof document.getElementsByTagName(p2) == "function"))
     Elem = document.getElementsByTagName(p2)[p3];
     else Elem = void(0);
     return(Elem);
   }
   else return void(0);
 }
 else if(MS) {
   if(p1.toLowerCase()=="id") {
     if (typeof document.all[p2] == "object")
     Elem = document.all[p2];
     else Elem = void(0);
     return(Elem);
   }
   else if(p1.toLowerCase()=="tagname") {
     if (typeof document.all.tags(p2) == "object")
     Elem = document.all.tags(p2)[p3];
     else Elem = void(0);
     return(Elem);
   }
   else if(p1.toLowerCase()=="name") {
     if (typeof document[p2] == "object")
     Elem = document[p2];
     else Elem = void(0);
     return(Elem);
   }
   else return void(0);
 }
 else if(NS) {
   if(p1.toLowerCase()=="id" || p1.toLowerCase()=="name") {
   if (typeof document[p2] == "object")
     Elem = document[p2];
     else Elem = void(0);
     return(Elem);
   }
   else if(p1.toLowerCase()=="index") {
    if (typeof document.layers[p2] == "object")
     Elem = document.layers[p2];
    else Elem = void(0);
     return(Elem);
   }
   else return void(0);
 }
}

function getCont(p1,p2,p3) {
   var Cont;
   if(DOM && getElem(p1,p2,p3) && getElem(p1,p2,p3).firstChild) {
     if(getElem(p1,p2,p3).firstChild.nodeType == 3)
       Cont = getElem(p1,p2,p3).firstChild.nodeValue;
     else
       Cont = "";
     return(Cont);
   }
   else if(MS && getElem(p1,p2,p3)) {
     Cont = getElem(p1,p2,p3).innerText;
     return(Cont);
   }
   else return void(0);
}

function getAttr(p1,p2,p3,p4) {
   var Attr;
   if((DOM || MS) && getElem(p1,p2,p3)) {
     Attr = getElem(p1,p2,p3).getAttribute(p4);
     return(Attr);
   }
   else if (NS && getElem(p1,p2)) {
       if (typeof getElem(p1,p2)[p3] == "object")
        Attr=getElem(p1,p2)[p3][p4]
       else
        Attr=getElem(p1,p2)[p4]
         return Attr;
       }
   else return void(0);
}

function setCont(p1,p2,p3,p4) {
   if(DOM && getElem(p1,p2,p3) && getElem(p1,p2,p3).firstChild)
     getElem(p1,p2,p3).firstChild.nodeValue = p4;
   else if(MS && getElem(p1,p2,p3))
     getElem(p1,p2,p3).innerText = p4;
   else if(NS && getElem(p1,p2,p3)) {
     getElem(p1,p2,p3).document.open();
     getElem(p1,p2,p3).document.write(p4);
     getElem(p1,p2,p3).document.close();
   }
}

DHTML_init();

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
 setCont("id","Uhr",null,Gesamt);
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
    var winl = (screen.width-790)/2;
    var wint = (screen.height-250)/2;

    var settings  ='height=250,';
    settings     +='width=790,';
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

function strassen_meldung(meldung)
{
alert(meldung);
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
    var winl = (screen.width-740)/2;
    var wint = (screen.height-345)/2;

    var settings  ='height=345,';
    settings     +='width=740,';
    settings     +='top='+wint+',';
    settings     +='left='+winl+',';
    settings     +='scrollbars=no,';
    settings     +='resizable=no';

    DetailWindow = open('strkat',"Strassensuche",settings);
    DetailWindow.focus();
  }

function strkat_hausnr(formname,fieldname)
{
   // 1. ---
   // 2. xa
   // 3. x

   var nr;
   var n_count;
   nr = document.forms[formname].elements[fieldname].value;
   n_count = 0;
   for(n=0;n<nr.length;n++)
   {
      if (nr.charAt(n) >= "a" && nr.charAt(n) <= "z")
      {
         n_count++;
         if (n < nr.length-1) n_count++;
      }
      else if ((nr.charAt(n) < "a" || nr.charAt(n) > "z") && (nr.charAt(n) < "0" || nr.charAt(n) > "9"))
      {
         n_count++;n_count++;
      }
   }

   if (n_count > 1)
   {
      //this.focus();
      alert ("Bitte gültigen Wert eintragen. z.B. 1, 10,100, 1a, 10a, 100a");
      document.forms[formname].elements[fieldname].value = "";
      this.focus();
      document.forms[formname].elements[fieldname].focus();
      return 0;
   }

   if (isNaN(nr))
   {
      n = nr.length;
      while(n < 4){
         nr = "0" + nr;
         n++;
      }
   }
   else
   {
      if (n == "") return 0;
      n = nr.length;
      while(n < 3){
         nr = "0" + nr;
         n++;
      }
   }
   document.forms[formname].elements[fieldname].value = nr;
}