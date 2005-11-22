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
  var doc_location = document.getElementById("doc_location");
  var pos = doc_location.pos_list.value;
  var srs = config.objects.mainMap.getSRS();
  doc_location.srs.value = srs;
  window.close();
}

function update_map() {
  //
  // changes the mainMap model and triggers a re-draw of the main map pane
  //
  var name_list = [];
  var layers = config.objects.layerControl.doc.selectNodes("//wmc:Layer");
  for (var i=0; i<layers.length; i++)
  {
    var layer = layers[i];
    if (layer.getAttribute("hidden") == "0")
    {
      name_list.push(layer.selectSingleNode("wmc:Name").firstChild.nodeValue);
    }
  }
  var agg_layer_name = config.objects.mainMap.doc.selectSingleNode("//wmc:Layer/wmc:Name");
  agg_layer_name.firstChild.nodeValue = name_list.join(",");
  config.objects.mainMap.callListeners("loadModel");
}

