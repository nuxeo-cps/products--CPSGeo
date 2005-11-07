// URL of Mapbuilder configuration file.
// Has to be included in all geo related template.
var mbConfigUrl='geo_edit_config.xml';
    
function switch_map() {
  var box = document.getElementById("map_selector").map;
  var modelurl = box.options[box.selectedIndex].value;
  if (modelurl) config.loadModel('mainMap', modelurl);
}

function submit_location() {
  var pos = document.getElementById("doc_location").pos_list.value;
  var field = opener.document.forms[2].widget__pos_list.value = pos;
  window.close();
}
