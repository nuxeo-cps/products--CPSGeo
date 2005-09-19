/*
License: LGPL as per: http://www.gnu.org/copyleft/lesser.html
$Id$
*/

/**
 * Base Feature object that all Map Feature extend.
 * @constructor
 * @author Patrice G. Cappelaere  patATcappelaere.com
 * @param feature     Pointer to the feature instance that needs marker support
 * @param itemId      ItemId
 * @param popupStr    HTML text to appear in popup
 */
 
function FeatureBase(model) {

  this.install = function(feature, itemId, title, description, about) {
    feature.itemId = itemId;
    feature.overlib = ""; //popupStr;
    feature.title = title;
    feature.description = description;
    feature.link = about;
    feature.onmouseover = this.mouseOverHandler; 
    feature.onmouseout  = this.mouseOutHandler;
  }

/**
  * MouseOver Handler
  *
  * Note: "This" points to the feature
  */
  this.mouseOverHandler = function(ev) {
      
    // get the enclosing div to get the current position
    var normalImageDiv = document.getElementById(this.itemId+"_normal");
    var topPx = new String(normalImageDiv.style.top);
    var leftPx = new String(normalImageDiv.style.left);
    // remove the px
    var offx = normalImageDiv.offsetParent.offsetLeft;
    var offy = normalImageDiv.offsetParent.offsetTop;
    var top = parseInt(topPx.replace("px","")) + 10 + offy;
    var left = parseInt(leftPx.replace("px","")) + 10 + offx;
    	
    // hilite the marker
  	normalImageDiv.style.visibility = "hidden";
    var highlightImageDiv = document.getElementById(this.itemId+"_highlight");
    highlightImageDiv.style.visibility = "visible";
    
    // set the popup text with stylesheet output
	//var popupStr = this.overlib;
    //if( popupStr == undefined ) {
	//  popupStr = "Feature under construction.  Stay tuned!";
	//}

    var desc = this.description.replace(/'/, "\'");
    desc = desc.replace(/"/, "&quot;");
    var popupStr = "<p>" + desc + "</p><p>[<a href=\"" + this.link + "\">link</a>] [<a href=\"javascript:void(0);\" onclick=\"window.open(\'" + this.link + "\')\">new window</a>]</p>";
	overlib(popupStr, WIDTH, 150, STICKY, FIXX, left, FIXY, top, CAPTION, this.title);
    return true;
  }
  
   /*
   * Mouseout handler
   */
  this.mouseOutHandler = function(ev) {
    var highlightImageDiv = document.getElementById(this.itemId+"_highlight");
    highlightImageDiv.style.visibility = "hidden";
    var normalImageDiv = document.getElementById(this.itemId+"_normal");
    normalImageDiv.style.visibility = "visible";
    return nd();
  }
}
