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
  // XXX getSRS() is a mapbuilder Context method
  // should get epsg:27582 for your customer's map
  // this value then needs to get passed to cps_geolocate:method
  // I'm not sure how you accomplish this -- Sean
  var srs = config.objects.mainMap.getSRS();
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

