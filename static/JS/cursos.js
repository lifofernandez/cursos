//console.log('Hola Enfermera');

var inicio = document.getElementById("id_inicio_fecha");
var inicio_inscripcion = document.getElementById("id_inicio_inscripcion");
var fin_inscripcion = document.getElementById("id_fin_inscripcion");

var type = document.createAttribute("type");
var type2 = document.createAttribute("type");
var type3 = document.createAttribute("type");
type.value = "date"
type2.value = "date"
type3.value = "date"

inicio.setAttributeNode(type);
inicio_inscripcion.setAttributeNode(type2);
fin_inscripcion.setAttributeNode(type3);

// document.getElementById("id_finalizacion_hora").attr("type","date");

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
// Get the first <h1> element in the document
