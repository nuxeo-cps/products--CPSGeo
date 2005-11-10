<?xml version="1.0" encoding="ISO-8859-1"?>

<!--
# (C) Copyright 2005 Nuxeo SARL 
# Author: Sean Gillies (sgillies@frii.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

Description: converts queried document info to form fields so that we
             can push features to the external mapserver for a print map
-->

<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
  xmlns:rss="http://purl.org/rss/1.0/" 
  xmlns:taxo="http://purl.org/rss/1.0/modules/taxonomy/" 
  xmlns:dc="http://purl.org/dc/elements/1.1/" 
  xmlns:syn="http://purl.org/rss/1.0/modules/syndication/" 
  xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">

  <xsl:output method="xml" omit-xml-declaration="no" encoding="utf-8" indent="yes"/>

  <xsl:param name="modelId"/>
  <xsl:param name="targetModelId"/>
  <xsl:param name="widgetId"/>
 
  <xsl:template match="/rdf:RDF">
    <xsl:apply-templates select="rss:item"/>
  </xsl:template>
 
  <xsl:template match="rss:item">
    <xsl:variable name="x"><xsl:value-of select="geo:long"/></xsl:variable>
    <xsl:variable name="y"><xsl:value-of select="geo:lat"/></xsl:variable>
    <xsl:variable name="title"><xsl:value-of select="rss:title"/></xsl:variable>
    <input type="hidden" name="map_cpsdocs_feature" value="new"/>
    <input type="hidden" name="map_cpsdocs_feature_points" value="{$x} {$y}"/>
    <input type="hidden" name="map_cpsdocs_feature_text" value="{$title}"/>
  </xsl:template>

</xsl:stylesheet>

