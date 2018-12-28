Table Border
============

The border of a table can be formatted to change the overall appearance of the
table. Within the word editor there are different ways to change this
appearance. The first is applying a specific predifined table style and the
second is manually changing the individual borders. This feature analysis
focusses on the latter.

The manual specification of the table border properties can be applied at table
level and at cell level. This specific feature focusses on the main table
border formatting.

The main properties are added to the `w:tblPr` element, there is in cases of
legacy documents, also the possibility of a `w:tblPrEx` element. This element
contains certain exceptions to the overall table border formatting definined
in the `w:tblPr` element. That override the table formatting. However, it's
somewhat redundant as, the cell level border specification, in the form of the
`w:tcPr` element, overrides any table level border specification. Hence this
feature request will only focus on the `w:tblPr` implementation of the borders.


Candidate protocol
------------------

Table level borders:

    >>> table = Document().add_table(4, 4)
    >>> borders = table.borders
    >>> borders
    <docx.table.Borders object at 0x...>
    >>> top = borders.top
    >>> top
    <docx.table.Border object at 0x...>
    >>> top.val = 'single'
    >>> bottom = borders.bottom
    >>> bottom
    <docx.table.Border object at 0x...>
    >>> bottom.val = 'double'
    >>> bottom.color = RGBColor(1, 1, 1)
    >>> bottom.size = 4


MS API - Partial Summary
------------------------

https://docs.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.tableborders?view=openxml-2.8.1

The `w:tblBorders` element specifies the set of borders for the edges of the
parent table row via a set of table-level property exceptions, using the six
border types defined by its child elements.

If the cell spacing for any row is non-zero as specified using the
`w:tblCellSpacing` element,  then there is no border conflict and the table
border (or table-level exception border, if one is specified) shall be
displayed.

If the cell spacing is zero, then there is a conflict. For instance:

Between the left border of all cells in the first column and the left border
of the table-level exceptions. This conflict shall be resolved as follows:

 - If there is a cell border, then the cell border shall be displayed

 - If there is no cell border, then the table-level exception border shall be
   displayed

 - If there is no cell or table-level exception border, then the table border
   shall be displayed

If this element is omitted, then this table shall have the borders specified by
the associated table style. If no borders are specified in the style hierarchy,
then this table shall not have any table borders.

Consider a table with no associated table style, which defines a set of table
borders via direct formatting as shown in the specimen xml. The tblBorders
element specifies the set of table borders applied to the current table.

Specimen xml
------------

.. highlight:: xml

::

    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="0" w:type="auto"/>
        <w:tblBorders>
          <w:top w:val="single" w:sz="4" w:space="0" w:color="000000" w:themeColor="text1"/>
          <w:left w:val="single" w:sz="4" w:space="0" w:color="000000" w:themeColor="text1"/>
          <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000" w:themeColor="text1"/>
          <w:right w:val="single" w:sz="4" w:space="0" w:color="000000" w:themeColor="text1"/>
          <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000" w:themeColor="text1"/>
          <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000" w:themeColor="text1"/>
        </w:tblBorders>
      </w:tblPr>
    </w:tbl>

Enumeration:

https://docs.microsoft.com/en-us/dotnet/api/documentformat.openxml.wordprocessing.bordervalues?view=openxml-2.8.1


Schema Definitions
------------------

.. highlight:: xml

::

  <xsd:complexType name="CT_TblBorders">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="top"     type="CT_Border" minOccurs="0"/>
      <xsd:element name="start"   type="CT_Border" minOccurs="0"/>
      <xsd:element name="left"    type="CT_Border" minOccurs="0"/>
      <xsd:element name="bottom"  type="CT_Border" minOccurs="0"/>
      <xsd:element name="end"     type="CT_Border" minOccurs="0"/>
      <xsd:element name="right"   type="CT_Border" minOccurs="0"/>
      <xsd:element name="insideH" type="CT_Border" minOccurs="0"/>
      <xsd:element name="insideV" type="CT_Border" minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_Border">  <!-- denormalized -->
    <xsd:attribute name="val"         type="ST_Border"             use="required"/>
    <xsd:attribute name="color"       type="ST_HexColor"           use="optional"/>
    <xsd:attribute name="themeColor"  type="ST_ThemeColor"         use="optional"/>
    <xsd:attribute name="themeTint"   type="ST_UcharHexNumber"     use="optional"/>
    <xsd:attribute name="themeShade"  type="ST_UcharHexNumber"     use="optional"/>
    <xsd:attribute name="sz"          type="ST_EighthPointMeasure" use="optional"/>
    <xsd:attribute name="space"       type="ST_PointMeasure"       use="optional"/>
    <xsd:attribute name="shadow"      type="s:ST_OnOff"            use="optional"/>
    <xsd:attribute name="frame"       type="s:ST_OnOff"            use="optional"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_Border">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="nil"/>
      <xsd:enumeration value="none"/>
      <xsd:enumeration value="single"/>
      <xsd:enumeration value="thick"/>
      <xsd:enumeration value="double"/>
      <xsd:enumeration value="dotted"/>
      <xsd:enumeration value="dashed"/>
      <xsd:enumeration value="dotDash"/>
      <xsd:enumeration value="dotDotDash"/>
      <xsd:enumeration value="triple"/>
      <xsd:enumeration value="thinThickSmallGap"/>
      <xsd:enumeration value="thickThinSmallGap"/>
      <xsd:enumeration value="thinThickThinSmallGap"/>
      <xsd:enumeration value="thinThickMediumGap"/>
      <xsd:enumeration value="thickThinMediumGap"/>
      <xsd:enumeration value="thinThickThinMediumGap"/>
      <xsd:enumeration value="thinThickLargeGap"/>
      <xsd:enumeration value="thickThinLargeGap"/>
      <xsd:enumeration value="thinThickThinLargeGap"/>
      <xsd:enumeration value="wave"/>
      <xsd:enumeration value="doubleWave"/>
      <xsd:enumeration value="dashSmallGap"/>
      <xsd:enumeration value="dashDotStroked"/>
      <xsd:enumeration value="threeDEmboss"/>
      <xsd:enumeration value="threeDEngrave"/>
      <xsd:enumeration value="outset"/>
      <xsd:enumeration value="inset"/>
    </xsd:restriction>

  <xsd:simpleType name="ST_HexColor">
    <xsd:union memberTypes="ST_HexColorAuto s:ST_HexColorRGB"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_ThemeColor">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="dark1"/>
      <xsd:enumeration value="light1"/>
      <xsd:enumeration value="dark2"/>
      <xsd:enumeration value="light2"/>
      <xsd:enumeration value="accent1"/>
      <xsd:enumeration value="accent2"/>
      <xsd:enumeration value="accent3"/>
      <xsd:enumeration value="accent4"/>
      <xsd:enumeration value="accent5"/>
      <xsd:enumeration value="accent6"/>
      <xsd:enumeration value="hyperlink"/>
      <xsd:enumeration value="followedHyperlink"/>
      <xsd:enumeration value="none"/>
      <xsd:enumeration value="background1"/>
      <xsd:enumeration value="text1"/>
      <xsd:enumeration value="background2"/>
      <xsd:enumeration value="text2"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="ST_UcharHexNumber">
    <xsd:restriction base="xsd:hexBinary">
      <xsd:length value="1"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="ST_EighthPointMeasure">
    <xsd:restriction base="s:ST_UnsignedDecimalNumber"/>
  </xsd:simpleType>

  <xsd:simpleType name="ST_PointMeasure">
    <xsd:restriction base="s:ST_UnsignedDecimalNumber"/>
  </xsd:simpleType>
