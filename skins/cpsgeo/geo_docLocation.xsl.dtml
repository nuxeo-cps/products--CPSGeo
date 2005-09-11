<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:gml="http://www.opengis.net/gml" version="1.0">

<!--
Description: Convert a GML Point feature to an HTML form field that is
             compatible with the pos_list field of the CPSGeo geolocation
             schema.
Author:      Sean Gillies (sgillies@frii.com)
-->

  <xsl:output method="xml" encoding="utf-8"/>

  <!-- Common params for all widgets -->
  <!--xsl:param name="targetModelId"/-->
  <xsl:param name="modelId"/>
  <xsl:param name="widgetId"/>

  <!-- Main html -->
  <xsl:template match="/">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- All nodes -->
  <xsl:template match="*">
    <xsl:variable name="xlink">
      <xsl:call-template name="getXpath">
        <xsl:with-param name="node" select="."/>
      </xsl:call-template>
    </xsl:variable>
      <xsl:if test="not(./*)">
          <input
            type="text"
            id="doc_location_pos_list"
            size="25"
            value="{format-number(number(substring-before(text(), ',')), '#.#######')} {format-number(number(substring-after(text(), ',')), '#.#######')}"
            name="pos_list"/>
      </xsl:if>
      <xsl:if test="./*">
        <xsl:apply-templates>
        </xsl:apply-templates>
      </xsl:if>
  </xsl:template>

  <!-- Return xpath reference to a node. Calls itself recursively -->
  <xsl:template name="getXpath">
    <xsl:param name="node"/>
    <xsl:if test="name($node/..)">
      <xsl:call-template name="getXpath">
        <xsl:with-param name="node" select="$node/.."/>
      </xsl:call-template>
    </xsl:if>
    <xsl:text>/</xsl:text>
    <xsl:value-of select="name($node)"/>
  </xsl:template>

  <!-- Remove documentation, text, comments -->
  <xsl:template match="comment()|text()|processing-instruction()">
  </xsl:template>
</xsl:stylesheet>

