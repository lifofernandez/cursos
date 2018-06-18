console.log('Hola Enfermera');

var ddl = document.getElementById("id_modalidad");
ddl.addEventListener("change",validate); 

function validate(){
  var selectedValue = this.options[ ddl.selectedIndex ].value;
  if (selectedValue == "v"){
    var dias = document.getElementById("id_dias");
    selectAllOptions(dias) 
    var inicio = document.getElementById("id_inicio_hora").value = "00:00:00";
    var fin = document.getElementById("id_finalizacion_hora").value = "23:59:59";
  }
}

function selectAllOptions(obj) {
  for (var i=0; i<obj.options.length; i++) {
    obj.options[i].selected = true;
  }
}
