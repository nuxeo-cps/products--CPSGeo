function switch_map() {
  var box = document.getElementById("map_selector").map;
  var mappath = box.options[box.selectedIndex].value;
  if (mappath != '')
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

function print_map_document() {
  var popup = window.open("cpsmap_document_print", "cpsmap_document_print", "toolbar=0, scrollbars=1, location=0, statusbar=0, menubar=0, resizable=1, dependent=1, width=800, height=600");
  if (!popup.opener) {
    popup.opener = window;
  }
}

function updateFromParent() {

  // Copy only the elements we want on the report
  var divs2copy = new Array("mainMapPane",
			    "legend",
			    "widget__map_id_widget");
  for (var i=0; i<divs2copy.length; i++) {
    var id_ = divs2copy[i];
    var orig_html = opener.document.getElementById(id_).innerHTML;
    var dest = document.getElementById(id_);
    dest.innerHTML = orig_html;
  }
  
  // Remove the dirt
  var submit = document.getElementById("layers_submit");
  submit.type = "hidden";

}

function editMap() {
  // Edit a map within a poup
  var box = document.getElementById("map_selector").map;
  var mappath = box.options[box.selectedIndex].value;  
  var args = "?mappath="+mappath;
  var popup = window.open("cps_map_edit"+args, "cps_map_edit", 
			  "toolbar=0, scrollbars=1, location=0, statusbar=0, menubar=0, resizable=1, dependent=1, width=800, height=600");
  if (!popup.opener) {
    popup.opener = window;
  }
}

function updateParentAfterEdit() {
  window.close();
  window.opener.location.reload(true);
}

function addMap() {
  // Add a new map within a poup
  var popup = window.open("cps_map_add", "cps_map_add", 
			  "toolbar=0, scrollbars=1, location=0, statusbar=0, menubar=0, resizable=1, dependent=1, width=800, height=600");
  if (!popup.opener) {
    popup.opener = window;
  }
}




