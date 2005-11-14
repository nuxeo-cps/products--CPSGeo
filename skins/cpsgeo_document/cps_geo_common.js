// URL of Mapbuilder configuration file.
// Has to be included in all geo related template.
var mbConfigUrl='geo_edit_config.xml';
    
function switch_map() {
  var box = document.getElementById("map_selector").map;
  var mappath = box.options[box.selectedIndex].value;
  if (mappath)
  {
    config.loadModel('mainMap', mappath + '/aggMapContext');
    config.loadModel('layerControl', mappath + '/mapContext');
  }
}

function submit_location() {
  var pos = document.getElementById("doc_location").pos_list.value;
  var field = opener.document.forms[2].widget__pos_list.value = pos;
  window.close();
}

function update_map() {
  //
  // changes the mainMap model and triggers a re-draw of the main map pane
  //
  // join names of all visible layers in the layerControl and use this
  // string as the name of the mainMap context 
  alert(config.objects['mainMap'].doc.selectNodes("wmc:Layer"));
  
}

