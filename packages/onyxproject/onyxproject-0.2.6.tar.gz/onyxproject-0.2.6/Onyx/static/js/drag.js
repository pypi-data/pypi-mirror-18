<!--
var dX, dY;

function start_drag(objet,event)
{


  dragged = objet;
  
  event.returnValue = false;
  if( event.preventDefault ) event.preventDefault();
  
  //Coordonnées de la souris
  var x = event.clientX + (document.documentElement.scrollLeft + document.body.scrollLeft);
  var y = event.clientY + (document.documentElement.scrollTop + document.body.scrollTop);
  

  //Coordonnées de l'élément
  var eX = 0;
  var eY = 0;
  var element = objet;
  do
  {
    eX += element.offsetLeft;
    eY += element.offsetTop;
    element = element.offsetParent;
  } while( element && element.style.position != 'absolute');

  //Calcul du décallage
  dX = x - eX;
  dY = y - eY;




}





function drag_onmousemove(event) 
{
  if( dragged ) 
  {
    var x = event.clientX + (document.documentElement.scrollLeft + document.body.scrollLeft);
    var y = event.clientY + (document.documentElement.scrollTop + document.body.scrollTop);
    
    //On applique le décalage
    x -= dX;
    y -= dY;

    var id = dragged.id;
    var t = document.getElementById("t");
    t.innerHTML = x + " | " + y + " | " + id;

    dragged.style.position = 'absolute';
    dragged.style.left = x + 'px';
    dragged.style.top = y + 'px';
  }
}

function drag_onmouseup(event) 
{
  dragged = null; //On arrête le drag&drop
}

function addEvent(obj,event,fct)
{
  if( obj.attachEvent)
     obj.attachEvent('on' + event,fct);
  else
     obj.addEventListener(event,fct,true);
}

function drag_onmousedown (event)
{
  var target = event.target || event.srcElement;
  
  //On commence par trouver la fenêtre elle-même
  var fenetre = target;
  while( fenetre)
  {
    if( fenetre.className && fenetre.className.match(/\bwindow-base\b/g) )
    {
       break; //On arrête la boucle
    }
    fenetre = fenetre.parentNode;
  }
  if( !fenetre) //Si on est sorti de la boucle mais qu'on a trouvé aucune fenêtre, on abandonne
    return;

  //Maintenant, on part à la recherche d'un bouton déclencheur
  var element = target;
  while(element)
  {
    if( element.className)
    {
      if( element.className.match(/\bwindow-close\b/g))
      {
        close(fenetre);
        break;
      }
      else if( element.className.match(/\bwindow-min-max\b/g) )
      {
        min_max(fenetre);
        break;
      }
      else if( element.className.match(/\bwindow-move\b/g) )
      {
        start_drag(fenetre, event);
        break;
      }
    }
    element = element.parentNode;
  }
}



addEvent(document,'mousedown',drag_onmousedown);
addEvent(document,'mousemove',drag_onmousemove);
addEvent(document,'mouseup',drag_onmouseup);


function dupliquer(fenetre)
{
  var n_f = fenetre.cloneNode(true);
  n_f.style.left = parseInt(fenetre.style.left) + 10 + 'px';
  n_f.style.top = parseInt(fenetre.style.top) + 10 + 'px';
  fenetre.parentNode.appendChild(n_f);
}
-->