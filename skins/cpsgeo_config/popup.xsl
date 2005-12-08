<?xml version="1.0" encoding="UTF-8"?>

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

Description: converts queried document info to a data model for use with
             map popups.
-->

<xsl:stylesheet version="1.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
  xmlns:rss="http://purl.org/rss/1.0/" 
  xmlns:taxo="http://purl.org/rss/1.0/modules/taxonomy/" 
  xmlns:dc="http://purl.org/dc/elements/1.1/" 
  xmlns:syn="http://purl.org/rss/1.0/modules/syndication/" 
  xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">

   <xsl:output method="xml" indent="yes" />

  <xsl:template match="rss:item">
    <results> 
  	<b>title:</b><xsl:value-of select="rss:title"/><br/>
  	<b>description:</b><xsl:value-of select="rss:description"/><br/>
  	<b>date:</b><xsl:value-of select="rss:date"/><br/>
    <b>long:</b><xsl:value-of select="geo:long"/><br/>
    <b>lat:</b><xsl:value-of select="geo:lat"/><br/>
    <b>link:</b><xsl:element name="a">
     <xsl:attribute name="href"><xsl:value-of select="rss:link"/></xsl:attribute>click here for more information!
    </xsl:element><br/>
    </results>
  </xsl:template>

</xsl:stylesheet>
