


document.addEventListener('DOMContentLoaded', function () {

var etape1 = document.getElementById('etape1');
var etape2 = document.getElementById('etape2');
var etape3 = document.getElementById('etape3');
var etape4 = document.getElementById('etape4');
var etape5 = document.getElementById('etape5');

  etape1.addEventListener('click', save_step_1);
  etape2.addEventListener('click', save_step_2);
  etape3.addEventListener('click', save_step_3);
  etape4.addEventListener('click', save_step_4);


});


function save_step_1()
{
                    change_step(1,2);
            
}

function save_step_2()
{

				change_step(2, 3);



}

function save_step_3()
{
    change_step(3, 4);
}





function save_step_4()
{

				change_step(4, 5);


}

function save_step_5()
{
	window.open(serveur + "/PHP/");
}



function change_step(step_old, new_step)
{
	document.getElementById("step" + step_old).style.display ="none";
	document.getElementById("step" + new_step).style.display ="block";

	document.getElementById("button_" + step_old).className = "btn btn-default btn-circle";
	document.getElementById("button_" + new_step).className = "btn btn-primary btn-circle";


}
