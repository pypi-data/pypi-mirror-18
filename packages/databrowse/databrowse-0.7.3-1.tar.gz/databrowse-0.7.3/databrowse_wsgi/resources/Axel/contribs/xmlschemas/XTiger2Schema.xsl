<?xml version="1.0" encoding="utf-8"?>

<!-- This transformation generates an XML Schema from a XTiger XML template.
     The generated schema defines the structure of the XML data created
     by the AXEL editing library when used with the source XTiger XML template.

     Vincent Quint, INRIA
     <vincent.quint@inria.fr>

     Version 0.5
     12 May 2010

     Before running this transformation, clean up the XTiger XML template
     using transformation XTigerCleanup.xsl.

     An XSLT 2.0 engine is required to run this transformation.
  -->

<xsl:transform version="2.0"
               xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
               xmlns:fn="http://www.w3.org/2005/xpath-functions"
               xmlns:xt="http://ns.inria.org/xtiger"
               xmlns:ht="http://www.w3.org/1999/xhtml"
               xmlns:xsd="http://www.w3.org/2001/XMLSchema"
               exclude-result-prefixes="fn xt ht">
  <xsl:output method="xml" version="1.0"
              omit-xml-declaration="no" indent="yes"
              encoding="utf-8" media-type="application/xml"/>

  <!-- version number of this transformation sheet -->
  <xsl:variable name="version" select="0.5"/>

  <!-- generate the root element (xsd:schema) and its first elements -->
  <xsl:template match="/">
    <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <!-- generate an xsd:annotation -->
      <xsd:annotation>
        <xsd:documentation xml:lang="en">
        This schema was generated by
        XTiger2Schema.xsl version <xsl:value-of select="$version"/><xsl:text>
      </xsl:text>
        </xsd:documentation>
      </xsd:annotation>
      <!-- if this template uses the "wiki" filter, generate the declaration
           of the corresponding elements -->
      <xsl:if test="//xt:use/@param='filter=wiki'">
        <xsd:complexType name="Fragment">
          <xsd:simpleContent>
            <xsd:extension base="xsd:string">
              <xsd:attribute name="FragmentKind" use="optional">
                <xsd:simpleType>
                  <xsd:restriction base="xsd:string">
                    <xsd:enumeration value="verbatim"/>
                    <xsd:enumeration value="important"/>
                  </xsd:restriction>
                </xsd:simpleType>
              </xsd:attribute>
            </xsd:extension>
          </xsd:simpleContent>
        </xsd:complexType>
        <xsd:complexType name="Link">
          <xsd:sequence>
            <xsd:element name="LinkText">
              <xsd:simpleType>
                <xsd:restriction base="xsd:string"/>
              </xsd:simpleType>
            </xsd:element>
            <xsd:element name="LinkRef">
              <xsd:simpleType>
                <xsd:restriction base="xsd:string"/>
              </xsd:simpleType>         
            </xsd:element>
          </xsd:sequence>
        </xsd:complexType>
        <xsd:group name="wikiContent">
           <xsd:sequence>
             <xsd:choice minOccurs="0" maxOccurs="unbounded">
               <xsd:element name="Fragment" type="Fragment"/>
               <xsd:element name="Link" type="Link"/>
             </xsd:choice>
           </xsd:sequence>
        </xsd:group>
      </xsl:if>
      <!-- if this template uses the "rich text" editor, generate the
           declaration of the corresponding elements and attributes -->
      <xsl:if test="//xt:use/@types='richtext'">
        <xsd:group name="richtextContent">
          <xsd:choice>
<!-- @@@@@@
            <xsd:group ref="plainText"/>   -->
            <xsd:element name="p">
              <xsd:complexType>
                <xsd:sequence>
                  <xsd:element name="span" minOccurs="0" maxOccurs="unbounded">
                    <xsd:complexType>
                      <xsd:simpleContent>
                        <xsd:extension  base="xsd:string">
                          <xsd:attribute name="style" type="xsd:string"/>
                        </xsd:extension>
                      </xsd:simpleContent>
                    </xsd:complexType>
                  </xsd:element>
                </xsd:sequence>
              </xsd:complexType>
            </xsd:element>
          </xsd:choice>
        </xsd:group>
      </xsl:if>
      <!-- start transforming the source XTiger template -->
      <xsl:apply-templates/>
    </xsd:schema>
  </xsl:template>

  <!-- all text contents from the XTiger template are ignored in all modes -->
  <xsl:template match="text()"/>
  <xsl:template match="text()" mode="flows"/>

  <!-- all xt:menu-marker elements from the XTiger template are ignored -->
  <xsl:template match="xt:menu-marker"/>

  <!-- transform xt:import elements into xsd:include elements -->
  <xsl:template match="xt:import">
    <xsl:if test="not (parent::xt:head)">
      <xsl:message terminate="yes">
        <xsl:text>*** ERROR: import </xsl:text>
        <xsl:value-of select="@name"/>
        <xsl:text> must be declared in xt:head ***</xsl:text>
      </xsl:message>
    </xsl:if>
    <xsl:element name="xsd:include">
      <xsl:attribute name="schemaLocation">
        <xsl:value-of select="@src"/>
      </xsl:attribute>
    </xsl:element>
  </xsl:template>

  <!-- generate the xsd:choice element corresponding to an xt:union element -->
  <xsl:template name="choiceEl">
    <xsl:element name="xsd:choice">
      <xsl:for-each select="fn:tokenize(@include, ' ')">
        <!-- generate an xsd:element for each name in the 'include' attribute
             of the xt:union element -->
        <xsl:element name="xsd:element">
          <xsl:attribute name="name">
            <xsl:value-of select="."/>
          </xsl:attribute>
          <xsl:attribute name="type">
            <xsl:value-of select="."/>
          </xsl:attribute>
        </xsl:element>
      </xsl:for-each>
    </xsl:element>
  </xsl:template>

  <!-- transform xt:union elements into xsd:choice elements -->
  <xsl:template match="xt:union">
    <xsl:if test="not (parent::xt:head)">
     <xsl:message terminate="yes">
       <xsl:text>*** ERROR: union </xsl:text>
       <xsl:value-of select="@name"/>
       <xsl:text> must be declared in xt:head ***</xsl:text>
     </xsl:message>
    </xsl:if>
    <xsl:if test="@exclude">
     <xsl:message terminate="yes">
       <xsl:text>*** ERROR: attribute 'exclude' not supported (union </xsl:text>
       <xsl:value-of select="@name"/>
       <xsl:text>) ***</xsl:text>
     </xsl:message>
    </xsl:if>
    <xsl:if test="parent::xt:head">
      <!-- generate an xsd:complexType element containing a xsd:choice -->
      <xsl:element name="xsd:complexType">
        <xsl:attribute name="name">
          <xsl:value-of select="@name"/>
        </xsl:attribute>
        <xsl:call-template name="choiceEl"/>
      </xsl:element>
      <!-- generate also a xsd:group element containing the same xsd:choice,
           if the xt:union element is referred by at least one xt:use element
           with no label -->
      <xsl:variable name="name" select="@name"/>
      <xsl:if test="/descendant::xt:use[(not (@label)) and (@types=$name)]">
        <xsl:element name="xsd:group">
          <xsl:attribute name="name">
            <xsl:value-of select="@name"/>
          </xsl:attribute>
          <xsl:call-template name="choiceEl"/>
        </xsl:element>
      </xsl:if>
    </xsl:if>
  </xsl:template>

  <!-- generate the content of a xt:component -->
  <xsl:template name="componentDef">
    <xsl:choose>
      <xsl:when test="child::xt:repeat or
                      count(child::xt:use) + count(child::xt:repeat)>1 or
                      child::xt:use/@label or
                      (child::xt:use/@types!='text' and
                       child::xt:use/@types!='string')">
        <!-- Several children or a complexType child
             Generate an xsd:sequence element -->
        <xsd:sequence>
          <xsl:apply-templates/>
        </xsd:sequence>
        <xsl:apply-templates select="descendant::xt:attribute" mode="attr"/>
      </xsl:when>
      <xsl:otherwise>
        <!-- there is no xt:repeat child in the xt:component, just a single
             xt:use child with types="text" or types="string" and no label.
             Generate an xsd:simpleContent element, except when the "wiki"
             filter is used -->
        <xsl:choose>
          <xsl:when test="child::xt:use/@param='filter=wiki'">
            <xsl:apply-templates/>
          </xsl:when>
          <xsl:otherwise>
            <xsd:simpleContent>
              <xsd:extension base="xsd:string">
                <!-- process the xt:attribute child elements -->
                <xsl:apply-templates select="descendant::xt:attribute"
                                     mode="attr"/>
                <!-- if the xt:use element uses the image filter, generate
                     the declaration of the 'Source' attribute -->
                <xsl:if test="child::xt:use/@param='filter=image'">
                  <xsd:attribute name="Source" type="xsd:string"/>
                </xsl:if>
              </xsd:extension>
            </xsd:simpleContent>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- transform xt:component elements into xsd:complexType elements -->
  <xsl:template match="xt:component">
    <xsl:if test="not (parent::xt:head)">
     <xsl:message terminate="yes">
       <xsl:text>*** ERROR: component </xsl:text>
       <xsl:value-of select="@name"/>
       <xsl:text> must be declared in xt:head ***</xsl:text>
     </xsl:message>
    </xsl:if>
    <xsl:if test="parent::xt:head">
      <xsl:element name="xsd:complexType">
        <xsl:attribute name="name">
          <xsl:value-of select="@name"/>
        </xsl:attribute>
        <xsl:call-template name="componentDef"/>
      </xsl:element>
      <!-- if the component is referred by a xt:use element with no label,
           an xsd:group definition will be needed, except if it's a
           simpleContent -->
      <xsl:if test="child::xt:repeat or
                    count(child::xt:use) + count(child::xt:repeat)>1 or
                    child::xt:use/@label or
                    (child::xt:use/@types!='text' and
                     child::xt:use/@types!='string')">
        <xsl:variable name="name" select="@name"/>
        <xsl:if test="/descendant::xt:use[(not (@label)) and (@types=$name)]">
          <xsl:element name="xsd:group">
            <xsl:attribute name="name">
              <xsl:value-of select="@name"/>
            </xsl:attribute>
            <xsl:call-template name="componentDef"/>
          </xsl:element>
        </xsl:if>
      </xsl:if>
    </xsl:if>
  </xsl:template>

  <!-- transform the 'types' attribute of an xt:use element -->
  <xsl:template name="typesAttribute">
    <!-- function "tokenize" requires a XPath 2.0 processor -->
    <xsl:if test="count(fn:tokenize(@types, ' '))=1">
      <!-- attribute 'types' contains a single name -->
      <xsl:if test="@types='text' or @types='string'">
        <!-- attribute 'types' contains just 'text' or 'string' -->
        <xsl:choose>
          <xsl:when test="(@types='text') and (@param='filter=wiki')">
            <!-- the "wiki" filter is used. Refer to the definition of "wiki"
                 content -->
            <xsd:complexType>
              <xsd:group ref="wikiContent"/>
            </xsd:complexType>
          </xsl:when>
          <xsl:otherwise>
            <!-- generate an attribute type="xd:string" -->
            <xsl:attribute name="type">
              <xsl:text>xsd:string</xsl:text>
            </xsl:attribute>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:if>
      <xsl:if test="@types='richtext'">
        <!-- attribute 'types' contains just 'richtext' -->
        <xsd:complexType>
          <xsd:group ref="richtextContent"/>
        </xsd:complexType>
      </xsl:if>
      <xsl:if test="@types!='text' and @types!='string' and @types!='richtext'">
        <!-- attribute 'types' contains a single name that is not "text"
             nor "string" nor "richtext" -->
        <xsl:attribute name="type">
          <xsl:value-of select="@types"/>
        </xsl:attribute>
      </xsl:if>
    </xsl:if>
    <xsl:if test="count(fn:tokenize(@types, ' '))>1">
      <!-- attribute 'types' contains multiple names. Generate an
           xsd:complexType element with an xsd:choice child element, and
           generate an xsd:element for each name -->
      <xsl:element name="xsd:complexType">
        <xsl:element name="xsd:choice">
          <xsl:for-each select="fn:tokenize(@types, ' ')">
            <xsl:element name="xsd:element">
              <xsl:attribute name="name">
                <xsl:value-of select="."/>
              </xsl:attribute>
              <xsl:attribute name="type">
                <xsl:value-of select="."/>
              </xsl:attribute>
            </xsl:element>
          </xsl:for-each>
        </xsl:element>
      </xsl:element>
    </xsl:if>
  </xsl:template>

  <!-- take the minOccurs and maxOccurs attributes from the parent
       xt:repeat element and copy them to the generated element -->
  <xsl:template name="minMaxParent">
    <xsl:if test="parent::xt:repeat/@minOccurs">
      <xsl:attribute name="minOccurs">
        <xsl:value-of select="parent::xt:repeat/@minOccurs"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:attribute name="maxOccurs">
      <xsl:if test="not (parent::xt:repeat/@maxOccurs)">
        <!-- the parent xt:repeat element has no maxOccurs attribute.
             Generate the default value "unbounded" -->
        <xsl:text>unbounded</xsl:text>
      </xsl:if>
      <xsl:if test="parent::xt:repeat/@maxOccurs">
        <xsl:if test="parent::xt:repeat/@maxOccurs!='*'">
          <xsl:value-of select="parent::xt:repeat/@maxOccurs"/>
        </xsl:if>
        <xsl:if test="parent::xt:repeat/@maxOccurs='*'">
          <xsl:text>unbounded</xsl:text>
        </xsl:if>
      </xsl:if>
    </xsl:attribute>
  </xsl:template>

  <!-- take the minOccurs and maxOccurs attributes from the
       xt:repeat element and copy them to the generated element -->
  <xsl:template name="minMaxOccurs">
    <xsl:if test="@minOccurs">
      <xsl:attribute name="minOccurs">
        <xsl:value-of select="@minOccurs"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:attribute name="maxOccurs">
      <xsl:if test="not (@maxOccurs)">
        <!-- the xt:repeat element has no maxOccurs attribute.
             Generate the default value "unbounded" -->
        <xsl:text>unbounded</xsl:text>
      </xsl:if>
      <xsl:if test="@maxOccurs">
        <xsl:if test="@maxOccurs!='*'">
          <xsl:value-of select="@maxOccurs"/>
        </xsl:if>
        <xsl:if test="@maxOccurs='*'">
          <xsl:text>unbounded</xsl:text>
        </xsl:if>
      </xsl:if>
    </xsl:attribute>
  </xsl:template>

  <!-- generate an xsd:element for an xt:use element with a 'label'
       attribute -->
  <xsl:template name="useWithLabel">
    <xsl:element name="xsd:element">
      <xsl:attribute name="name">
        <xsl:value-of select="@label"/>
      </xsl:attribute>
      <xsl:if test="parent::xt:repeat and
                    count(parent::xt:repeat/child::xt:use) +
                    count(parent::xt:repeat/child::xt:repeat) = 1">
        <!-- single child of an xt:repeat element. Get the 'minOccurs' and
             'maxOccurs' attributes from the xt:repeat parent element -->
        <xsl:call-template name="minMaxParent"/>
      </xsl:if>
      <xsl:if test="not(parent::xt:repeat)">
        <xsl:if test="@option">
          <!-- the parent is not an xt:repeat element, but the xt:use element
               has an 'option' attribute. Generate attribute minOccurs="0" -->
          <xsl:attribute name="minOccurs">
            <xsl:text>0</xsl:text>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
      <!-- handle the 'types' attribute, except when the "image" filter is used:
           element is empty in this case -->
      <xsl:if test="not (@param='filter=image')">
        <xsl:call-template name="typesAttribute"/>
      </xsl:if>
      <!-- if the "image" filter is used, generate the 'Source' attribute -->
      <xsl:if test="@param='filter=image'">
        <xsd:complexType>
          <xsd:attribute name="Source" type="xsd:string"/>
        </xsd:complexType>
      </xsl:if>
    </xsl:element>
  </xsl:template>

  <!-- process the xt:use elements that have a given value (flowPar) of
       attribute 'flow' -->
  <xsl:template match="xt:use[@flow]" mode="flowWithValue">
    <xsl:param name="flowPar"/>
    <xsl:if test="@flow=$flowPar">
      <!-- this xt:use element has a 'flow' attribute with the value of
           interest -->
      <xsl:if test="not(@label)">
        <xsl:message terminate="yes">
          <xsl:text>*** ERROR: element xt:use with 'flow=</xsl:text>
          <xsl:value-of select="@flow"/>
          <xsl:text>' must have a 'label' attribute ***</xsl:text>
        </xsl:message>
      </xsl:if>
      <xsl:call-template name="useWithLabel"/>
    </xsl:if>
  </xsl:template>

  <!-- process xt:use elements with a 'flow' attribute (in 'flows' mode) -->
  <xsl:template match="xt:use[@flow]" mode="flows">
    <xsl:if test="not(@label)">
      <xsl:message terminate="yes">
        <xsl:text>*** ERROR: element xt:use with 'flow=</xsl:text>
        <xsl:value-of select="@flow"/>
        <xsl:text>' must have a 'label' attribute ***</xsl:text>
      </xsl:message>
    </xsl:if>
    <xsl:variable name="flowVal" select="@flow"/>
    <xsl:if test="not(preceding::xt:use[@flow=$flowVal])">
      <!-- first occurence of this flow. Generate an element with the same
           name as the flow -->
      <xsl:element name="xsd:element">
        <xsl:attribute name="name">
          <xsl:value-of select="@flow"/>
        </xsl:attribute>
        <xsd:complexType>
          <xsd:sequence>
            <!-- process the xt:use element itself -->
            <xsl:call-template name="useWithLabel"/>
            <!-- process all other (following) xt:use elements with the same
                 'flow' attribute -->
            <xsl:apply-templates select="following::*" mode="flowWithValue">
              <xsl:with-param name="flowPar" select="$flowVal"/>
            </xsl:apply-templates>
          </xsd:sequence>
        </xsd:complexType>
      </xsl:element>
    </xsl:if>
  </xsl:template>

  <!-- transform xt:use elements, only if they do not have a
       'flow' attribute -->
  <xsl:template match="xt:use[not(@flow)]">
    <xsl:if test="@label">
      <!-- element xt:use has a 'label' attribute. Generate an xsd:element -->
      <xsl:call-template name="useWithLabel"/>
    </xsl:if>
    <xsl:if test="not(@label)">
      <!-- element xt:use has no 'label' attribute -->
      <xsl:if test="count(fn:tokenize(@types, ' '))=1">
        <!-- the 'types' attribute contains a single value. Generate a
             reference to the corresponding xsd:group element -->
        <xsl:element name="xsd:group">
          <xsl:attribute name="ref">
            <xsl:choose>
              <xsl:when test="(@types='text') and (@param='filter=wiki')">
                <xsl:text>wikiContent</xsl:text>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="@types"/>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:attribute>
          <xsl:if test="parent::xt:repeat and
                        count(parent::xt:repeat/child::xt:use) +
                        count(parent::xt:repeat/child::xt:repeat) = 1">
            <!-- only child of a xt:repeat element. Copy the 'minOccurs' and
                 'maxOccurs' attributes from the xt:repeat parent -->
            <xsl:call-template name="minMaxParent"/>
          </xsl:if>
        </xsl:element>
      </xsl:if>
      <xsl:if test="count(fn:tokenize(@types, ' '))>1">
        <!-- the 'types' attribute of this xt:use element has multiple
             values. Generate an xsd:choice element -->
        <xsl:element name="xsd:choice">
          <xsl:if test="parent::xt:repeat and
                        count(parent::xt:repeat/child::xt:use) +
                        count(parent::xt:repeat/child::xt:repeat) = 1">
            <!-- only child of a xt:repeat element. Copy the 'minOccurs' and
                 'maxOccurs' attributes from the xt:repeat parent -->
            <xsl:call-template name="minMaxParent"/>
          </xsl:if>
          <!-- for each name in the 'types' attribute, generate an xsd:element
               as a child of the xsd:choice element -->
          <xsl:for-each select="fn:tokenize(@types, ' ')">
            <xsl:element name="xsd:element">
              <xsl:attribute name="name">
                <xsl:value-of select="."/>
              </xsl:attribute>
              <xsl:attribute name="type">
                <xsl:value-of select="."/>
              </xsl:attribute>
            </xsl:element>
          </xsl:for-each>
        </xsl:element>
      </xsl:if>
    </xsl:if>
  </xsl:template>

  <!-- transform xt:repeat elements -->
  <xsl:template match="xt:repeat">
    <xsl:if test="@label">
      <!-- xt:repeat element with a label. Generate an xsd:element -->
      <xsl:element name="xsd:element">
        <xsl:attribute name="name">
          <xsl:value-of select="@label"/>
        </xsl:attribute>
        <xsl:if test="parent::xt:repeat/@minOccurs='0'">
          <!-- the parent is another xt:repeat with "minOccurs=0" -->
          <xsl:attribute name="minOccurs">
            <xsl:text>0</xsl:text>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="not (parent::xt:repeat/@minOccurs='0')">
          <xsl:if test="@minOccurs='0'">
            <!-- the xt:repeat element itself has "minOccurs=0" -->
            <xsl:attribute name="minOccurs">
              <xsl:text>0</xsl:text>
            </xsl:attribute>
          </xsl:if>
        </xsl:if>
        <xsl:element name="xsd:complexType">
          <xsl:element name="xsd:sequence">
            <xsl:apply-templates/>
          </xsl:element>
        </xsl:element>
      </xsl:element>
    </xsl:if>
    <xsl:if test="not (@label)">
      <!-- the xt:repeat element has no label -->
      <xsl:if test="count(child::xt:use) + count(child::xt:repeat)>1">
        <!-- more than 1 XTiger element in the xt:repeat. Generate an
             xsd:sequence element and put the occurence attributes on this
             element element -->
        <xsl:element name="xsd:sequence">
          <xsl:call-template name="minMaxOccurs"/>
        </xsl:element>
      </xsl:if>
      <xsl:apply-templates/>
    </xsl:if>
  </xsl:template>

  <!-- transform xt:attribute elements into xsd:attribute elements -->
  <xsl:template match="xt:attribute" mode="attr">
    <xsl:element name="xsd:attribute">
      <xsl:attribute name="name">
        <xsl:value-of select="@name"/>
      </xsl:attribute>
      <!-- accept both the 'types' attribute and its deprecated
           version 'type' -->
      <xsl:choose>
        <xsl:when test="@types='select' or @type='select'">
          <!-- types="select" -->
          <xsd:simpleType>
            <xsd:restriction base="xsd:string">
              <!-- generate an xsd:enumeration element for each substring
                   of attribute xt:values -->
              <!-- function "tokenize" requires a XPath 2.0 processor -->
              <xsl:for-each select="fn:tokenize(@values, ' ')">
                <xsl:element name="xsd:enumeration">
                  <xsl:attribute name="value">
                    <xsl:value-of select="."/>
                  </xsl:attribute>
                </xsl:element>
              </xsl:for-each>
            </xsd:restriction>
          </xsd:simpleType>
        </xsl:when>
        <xsl:otherwise>
          <xsl:attribute name="type">
            <xsl:if test="@types='text' or @types='string' or @types='photo' or
                          @type='text'  or @type='string'  or @type='photo'">
              <!-- types="text", "string" or "photo". Translate into
                   xsd:string -->
              <xsl:text>xsd:string</xsl:text>
            </xsl:if>
            <!-- other types than 'select' 'text' 'string' and 'photo' will
                 be handled here -->
          </xsl:attribute>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:element>
  </xsl:template>

  <!-- generate the root xsd:element from the ht:body element -->
  <xsl:template match="ht:body">
    <xsl:variable name="rootElem">
      <xsl:if test="preceding::xt:head/@label">
        <!-- element xt:head has a label. Take it as the name of the root
             element -->
        <xsl:value-of select="preceding::xt:head/@label"/>
      </xsl:if>
      <xsl:if test="not(preceding::xt:head/@label)">
        <!-- otherwise, call the root element 'root' by default -->
        <xsl:text>root</xsl:text>
      </xsl:if>
    </xsl:variable>
    <xsl:if test="not (/descendant::xt:use[@flow])">
      <!-- no flow in this template. Generate an xsd:element with an
           xsd:complexType child -->
      <xsl:element name="xsd:element">
        <xsl:attribute name="name">
          <xsl:value-of select="$rootElem"/>
        </xsl:attribute>
        <xsd:complexType>
          <xsl:call-template name="componentDef"/>
        </xsd:complexType>
      </xsl:element>
    </xsl:if>
    <xsl:if test="/descendant::xt:use[@flow]">
      <!-- this template uses at least one flow. Generate the definition of
           the 'tide' root element -->
      <xsl:element name="xsd:element">
        <xsl:attribute name="name">
          <xsl:text>tide</xsl:text>
        </xsl:attribute>
        <xsd:complexType>
          <xsd:sequence>
            <!-- generate the definition of the root of the main (default)
                 flow -->
            <xsl:element name="xsd:element">
              <xsl:attribute name="name">
                <xsl:value-of select="$rootElem"/>
              </xsl:attribute>
              <xsd:complexType>
                <!-- process all elements of the default flow -->
                <xsl:call-template name="componentDef"/>
              </xsd:complexType>
            </xsl:element>
            <!-- process all elements belonging to named flows -->
            <xsl:apply-templates select="/" mode="flows"/>
          </xsd:sequence>
        </xsd:complexType>
      </xsl:element>
    </xsl:if>
  </xsl:template>

</xsl:transform>
