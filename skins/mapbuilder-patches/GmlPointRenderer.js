/*
Author:       Cameron Shorter cameronATshorter.net
License:      LGPL as per: http://www.gnu.org/copyleft/lesser.html

$Id: GmlPointRenderer.js,v 1.3 2005/08/05 18:47:11 madair1 Exp $
*/

/*
Heavily modified by Sean Gillies, sgillies@frii.com, and will be rolled back
into mapbuilder November 2005
*/

// Ensure this object's dependancies are loaded.
mapbuilder.loadScript(baseDir+"/model/Proj.js");
mapbuilder.loadScript(baseDir+"/widget/MapContainerBase.js");
mapbuilder.loadScript(baseDir+"/widget/Popup.js");
mapbuilder.loadScript(baseDir+"/tool/FeatureBase.js");

// Resource: http://www.bazon.net/mishoo/articles.epl?art_id=824

/**
 * Render GML point geometery into HTML.  This is a MapContainer widget.
 * Other Geometries could be handled if there was some way to get a point 
 * out of it (e.g. polygon centroid).
 * This widget places an image at the specified point on the map.
 * It also places a highlight image at the same spot and registers a 
 * hihglightFeature event on the model, where the featureId is set as the model param.
 * Models using this widget must implement getFeatureNodes(), 
 * @constructor
 * @base MapContainerBase
 * @param widgetNode  The widget's XML object node from the configuration document.
 * @param model       The model object that this widget belongs to.
 */

function GmlPointRenderer(widgetNode, model) {

  this.normalImage = widgetNode.selectSingleNode("mb:normalImage").firstChild.nodeValue; 
  	this.highlightImage = widgetNode.selectSingleNode("mb:highlightImage").firstChild.nodeValue;
  this.popup = new Popup( widgetNode, model );
  
  this.featureBase = new FeatureBase(model);
  
  /**
    * Clear all markers
    */
  this.clearWidget = function(objRef) {
    // we need to clear all the div's first
    var divs = document.getElementsByTagName("div");
    //for (var i=0;i< divs.length;i++) {
    for (var i= divs.length-1; i>= 0; i--) {
        var id = new String(divs[i].getAttribute("id"));
      if( id.indexOf("RSS_Item") >= 0 ) {
          var img = divs[i].firstChild;
          img.onmouseover = null;
          img.onmouseout = null;
          divs[i].parentNode.removeChild( divs[i] );
        }
      }
  }
  
  /** draw the points by putting the image at the point
    * @param objRef a pointer to this widget object
    */
  this.paint = function(objRef) {
    var divs = document.getElementsByTagName("div");
    for (var i=divs.length-1; i>=0; i--) {
      var div = divs[i];
      if (div.id.indexOf("RSS_Item") > -1) {
        var img = div.firstChild;
        img.onmouseover = null;
        img.onmouseout = null;
        div.parentNode.removeChild(div);
      }
    }          	
    var containerProj = new Proj(objRef.containerModel.getSRS());
    var features = objRef.model.getFeatureNodes();
    for (var i=0; i<features.length; ++i) {
      var feature = features[i];
      var title = objRef.model.getFeatureName(feature);
      var itemId = objRef.model.getFeatureId(feature);   //or feature id's for feature collections?
      var point = objRef.model.getFeaturePoint(feature);
      var description = feature.selectSingleNode("rss:description").firstChild.nodeValue;
      var about = feature.selectSingleNode("rss:link").firstChild.nodeValue;

      if( (point[0] == 0) && (point[1] == 0 )) {
      		// no point in going any further 
      		return;
      	}
      	
      point = containerProj.Forward(point);
      point = objRef.containerModel.extent.getPL(point);

      var normalImageDiv = document.getElementById(itemId+"_normal");
      var highlightImageDiv = document.getElementById(itemId+"_highlight");
      if (!normalImageDiv) {
        //add in the normalImage
        normalImageDiv = document.createElement("DIV");
        normalImageDiv.setAttribute("id",itemId+"_normal");
        normalImageDiv.style.position = "absolute";
        normalImageDiv.style.visibility = "visible";
        normalImageDiv.style.zIndex = 300;
        
        var newImage = document.createElement("IMG");
        newImage.src = config.skinDir+objRef.normalImage;
        newImage.title = title;
 				             
        normalImageDiv.appendChild(newImage);
        objRef.node.appendChild( normalImageDiv );

        //var overlib = objRef.popup.transform( objRef.popup, feature );
        objRef.featureBase.install(newImage, itemId, title, description, about);

        //add in the highlightImage
        highlightImageDiv = document.createElement("DIV");
        highlightImageDiv.setAttribute("id",itemId+"_highlight");
        highlightImageDiv.style.position = "absolute";
        highlightImageDiv.style.visibility = "hidden";
        highlightImageDiv.style.zIndex = 301;   //all highlight images are on top of others
        var newImage = document.createElement("IMG");
        newImage.src = config.skinDir+objRef.highlightImage;
        newImage.title = title;
        highlightImageDiv.appendChild(newImage);
        objRef.node.appendChild( highlightImageDiv );
      }

      normalImageDiv.style.left = point[0];
      normalImageDiv.style.top = point[1];
      highlightImageDiv.style.left = point[0];
      highlightImageDiv.style.top = point[1];
    }
  }
    
  this.stylesheet = new XslProcessor(baseDir+"/widget/Null.xsl");
  var base = new MapContainerBase(this,widgetNode,model);
 
  /** highlights the selected feature by switching to the highlight image
    * @param objRef a pointer to this widget object
    */
  this.highlight = function(objRef, featureId) {
    var normalImageDiv = document.getElementById(featureId+"_normal");
    normalImageDiv.style.visibility = "hidden";
    var highlightImageDiv = document.getElementById(featureId+"_highlight");
    highlightImageDiv.style.visibility = "visible";
  }
  this.model.addListener("highlightFeature",this.highlight, this);

  /** highlights the selected feature by switching to the highlight image
    * @param objRef a pointer to this widget object
    */
  this.dehighlight = function(objRef, featureId) {
    var normalImageDiv = document.getElementById(featureId+"_normal");
    normalImageDiv.style.visibility = "visible";
    var highlightImageDiv = document.getElementById(featureId+"_highlight");
    highlightImageDiv.style.visibility = "hidden";
  }
  this.model.addListener("dehighlightFeature",this.dehighlight, this);

}

