.. _fields:

Fields
======

Fields in Word are used as placeholders for data that might change in a
document and for creating form letters and labels in mail merge documents.

Word inserts fields automatically when you use particular commands, such as
when you insert a page number, when you insert a document building block such
as a cover page, or when you create a table of contents. You can also manually
insert fields to automate aspects of your document, such as merging data from
a data source or performing calculations.

An overview of possible field codes is provided here

https://support.office.com/en-us/article/list-of-field-codes-in-word-1ad6d91a-55a7-4a8d-b535-cf7888659a51#__toc316563575


FieldChar class
---------------

fldChar (Complex Field Character)

This element specifies the presence of a complex field character at the
current location in the parent run. A complex field character is a special
character which delimits the start and end of a complex field or separates its
field codes from its current field result.

A complex field is defined via the use of the two required complex field
characters: a start character, which specifies the beginning of a complex
field within the document content; and an end character, which specifies the
end of a complex field. This syntax allows multiple fields to be embedded
(or "nested") within each other in a document.

As well, because a complex field can specify both its field codes and its
current result within the document, these two items are separated by the
optional separator character, which defines the end of the field codes and the
beginning of the field contents. The omission of this character shall be used
to specify that the contents of the field are entirely field codes
(i.e. the field has no result).

See --> https://msdn.microsoft.com/en-us/library/office/documentformat.openxml.wordprocessing.fieldchar.aspx

SimpleField class
-----------------

fldSimple (Simple Field)

This element specifies the presence of a simple field at the current location
in the document. The semantics of this field are defined via its field codes.

See --> https://msdn.microsoft.com/en-us/library/office/documentformat.openxml.wordprocessing.simplefield.aspx


Protocol
--------

Since field codes are located in a run, the obvious location would be in the
Run object.

>>> Run.add_field({ FIELD NAME Instructions Optional switches })

FIELD NAME     This is the name that appears in the list of field names
               in the Field dialog box.

Instructions  These are any instructions or variables that are used in a
              particular field. Not all fields have parameters, and in some
              fields, parameters are optional instead of required.

Optional switches    These are any optional settings that are available for a
                     particular field. Not all fields have switches available,
                     other than those that govern the formatting of the field
                     results.

Word UI features and behaviors
------------------------------

* The field codes are accessed via the `Quick Parts` - field dialog. This
  provides access to all the different field codes available within the word
  editor.

* The field codes are evaluated when the field codes are updated within the
  text editor (Ctrl+F9 or Print Preview)

Related items from Microsoft VBA API
------------------------------------

* `Fields`
  https://docs.microsoft.com/en-us/dotnet/api/microsoft.office.interop.word.fields?view=word-pia


* `Field`
  https://docs.microsoft.com/en-us/dotnet/api/microsoft.office.interop.word.field?view=word-pia

* Apparently has a property `kind` which has the enumeration `WdFieldKind`

Enumerations
------------

--->> hele linker kolom??? https://docs.microsoft.com/en-us/dotnet/api/microsoft.office.interop.word.wdmergetarget?view=word-pia


WdFieldType
~~~~~~~~~~~

https://docs.microsoft.com/en-us/dotnet/api/microsoft.office.interop.word.wdfieldtype?view=word-pia

https://msdn.microsoft.com/en-us/vba/word-vba/articles/wdfieldtype-enumeration-word

https://support.office.com/en-us/article/list-of-field-codes-in-word-1ad6d91a-55a7-4a8d-b535-cf7888659a51#top


**wdFieldAddin**
    81	-- Add-in field. Not available through the Field dialog box. Used to store data that is hidden from the user interface.
**wdFieldAddressBlock**
    93	AddressBlock field.
**wdFieldAdvance**
    84	Advance field.
**wdFieldAsk**
    38	Ask field.
**wdFieldAuthor**
    17	Author field.
**wdFieldAutoNum**
  	54	AutoNum field.
**wdFieldAutoNumLegal**
  	53	AutoNumLgl field.
**wdFieldAutoNumOutline**
  	52	AutoNumOut field.
**wdFieldAutoText**
  	79	AutoText field.
**wdFieldAutoTextList**
  	89	AutoTextList field.
**wdFieldBarCode**
  	63	BarCode field.
**wdFieldBidiOutline**
  	92	BidiOutline field.
**wdFieldComments**
  	19	Comments field.
**wdFieldCompare**
  	80	Compare field.
**wdFieldCreateDate**
  	21	CreateDate field.
**wdFieldData**
  	40	Data field.
**wdFieldDatabase**
  	78	Database field.
**wdFieldDate**
  	31	Date field.
**wdFieldDDE**
  	45	DDE field. No longer available through the Field dialog box,
        but supported for documents created in earlier versions of Word.
**wdFieldDDEAuto**
  	46	DDEAuto field. No longer available through the Field dialog box,
        but supported for documents created in earlier versions of Word.
**wdFieldDisplayBarcode**
  	99	DisplayBarcode field.
**wdFieldDocProperty**
  	85	DocProperty field.
**wdFieldDocVariable**
  	64	DocVariable field.
**wdFieldEditTime**
  	25	EditTime field.
**wdFieldEmbed**
  	58	Embedded field.
**wdFieldEmpty**
  	-1	Empty field. Acts as a placeholder for field content that has not yet
        been added. A field added by pressing Ctrl+F9 in the user interface
        is an Empty field.
**wdFieldExpression**
  	34	= (Formula) field.
**wdFieldFileName**
  	29	FileName field.
**wdFieldFileSize**
  	69	FileSize field.
**wdFieldFillIn**
  	39	Fill-In field.
**wdFieldFootnoteRef**
  	5	FootnoteRef field. Not available through the Field dialog box.
      Inserted programmatically or interactively.
**wdFieldFormCheckBox**
  	71	FormCheckBox field.
**wdFieldFormDropDown**
  	83	FormDropDown field.
**wdFieldFormTextInput**
  	70	FormText field.
**wdFieldFormula**
  	49	EQ (Equation) field.
**wdFieldGlossary**
  	47	Glossary field. No longer supported in Word.
**wdFieldGoToButton**
  	50	GoToButton field.
**wdFieldGreetingLine**
	  94	GreetingLine field.
**wdFieldHTMLActiveX**
	  91	HTMLActiveX field. Not currently supported.
**wdFieldHyperlink**
	  88	Hyperlink field.
**wdFieldIf**
	  7	If field.
**wdFieldImport**
	  55	Import field. Cannot be added through the Field dialog box,
        but can be added interactively or through code.
**wdFieldInclude**
	  36	Include field. Cannot be added through the Field dialog box,
        but can be added interactively or through code.
**wdFieldIncludePicture**
	  67	IncludePicture field.
**wdFieldIncludeText**
	  68	IncludeText field.
**wdFieldIndex**
	  8	Index field.
**wdFieldIndexEntry**
	  4	XE (Index Entry) field.
**wdFieldInfo**
	  14	Info field.
**wdFieldKeyWord**
	  18	Keywords field.
**wdFieldLastSavedBy**
	  20	LastSavedBy field.
**wdFieldLink**
	  56	Link field.
**wdFieldListNum**
	  90	ListNum field.
**wdFieldMacroButton**
	  51	MacroButton field.
**wdFieldMergeBarcode**
	  98	MergeBarcode field.
**wdFieldMergeField**
	  59	MergeField field.
**wdFieldMergeRec**
	  44	MergeRec field.
**wdFieldMergeSeq**
	  75	MergeSeq field.
**wdFieldNext**
	  41	Next field.
**wdFieldNextIf**
	  42	NextIf field.
**wdFieldNoteRef**
	  72	NoteRef field.
**wdFieldNumChars**
	  28	NumChars field.
**wdFieldNumPages**
	  26	NumPages field.
**wdFieldNumWords**
	  27	NumWords field.
**wdFieldOCX**
	  87	OCX field. Cannot be added through the Field dialog box, but can be
        added through code by using the AddOLEControl method of the Shapes
        collection or of the InlineShapes collection.
**wdFieldPage**
	  33	Page field.
**wdFieldPageRef**
	  37	PageRef field.
**wdFieldPrint**
	  48	Print field.
**wdFieldPrintDate**
  	23	PrintDate field.
**wdFieldPrivate**
  	77	Private field.
**wdFieldQuote**
  	35	Quote field.
**wdFieldRef**
  	3	Ref field.
**wdFieldRefDoc**
  	11	RD (Reference Document) field.
**wdFieldRevisionNum**
  	24	RevNum field.
**wdFieldSaveDate**
  	22	SaveDate field.
**wdFieldSection**
	  65	Section field.
**wdFieldSectionPages**
  	66	SectionPages field.
**wdFieldSequence**
	  12	Seq (Sequence) field.
**wdFieldSet**
  	6	Set field.
**wdFieldShape**
	  95	Shape field. Automatically created for any drawn picture.
**wdFieldSkipIf**
	  43	SkipIf field.
**wdFieldStyleRef**
  	10	StyleRef field.
**wdFieldSubject**
  	16	Subject field.
**wdFieldSubscriber**
  	82	Macintosh only. For information about this constant, consult the language reference Help included with Microsoft Office Macintosh Edition.
**wdFieldSymbol**
	  57	Symbol field.
**wdFieldTemplate**
	  30	Template field.
**wdFieldTime**
	  32	Time field.
**wdFieldTitle**
	  15	Title field.
**wdFieldTOA**
	  73	TOA (Table of Authorities) field.
**wdFieldTOAEntry**
	  74	TOA (Table of Authorities Entry) field.
**wdFieldTOC**
	  13	TOC (Table of Contents) field.
**wdFieldTOCEntry**
	  9	TOC (Table of Contents Entry) field.
**wdFieldUserAddress**
	  62	UserAddress field.
**wdFieldUserInitials**
	  61	UserInitials field.
**wdFieldUserName**
  	60	UserName field.
**wdFieldBibliography**
	  97	Bibliography field.
**wdFieldCitation**
  	96	Citation field.


WdFieldKind
~~~~~~~~~~~

**wdFieldKindCold**
   3  A field that doesn't have a result, for example, an Index Entry (XE),
      Table of Contents Entry (TC), or Private field.

**wdFieldKindHot**
   1  A field that's automatically updated each time it's displayed or each time
      the page is reformatted, but which can also be manually updated
      (for example, INCLUDEPICTURE or FORMDROPDOWN).

**wdFieldKindNone**
   0  An invalid field (for example, a pair of field characters with nothing inside).

**wdFieldKindWarm**
   2  A field that can be updated and has a result. This type includes fields
      that are automatically updated when the source changes as well as fields
      that can be manually updated (for example, DATE or INCLUDETEXT).

XML specimens
-------------

Example use of a simple field.

.. highlight:: xml

  <w:fldSimple w:instr="FILENAME">
    <w:r>
      <w:t>Example Document.docx</w:t>
    </w:r>
  </w:fldSimple>

Example use of a complex field character:

.. highlight:: xml

    <w:r>
      <w:fldChar w:fldCharType="begin" />
    </w:r>
    <w:r>
      <w:instrText>AUTHOR</w:instrText>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="separate" />
    </w:r>
    <w:r>
      <w:t>Rex Jaeschke</w:t>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="end" />
    </w:r>

Example of a locked field code:

.. highlight:: xml

    <w:r>
      <w:fldChar w:fldCharType="start" w:fldLock="true"/>
    </w:r>
    …<w:r>
      <w:fldChar w:fldCharType="separate"/>
    </w:r>
    <w:r>
      <w:t>field result</w:t>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="end" />
    </w:r>

The type attribute value of separate specifies
that this is a complex field separator character; therefore it is being used
to separate the field codes from the field contents in a complex field.

Example:
.. highlight:: xml

    <w:fldChar w:fldCharType="separate" />

Example: Dirty element

    <w:r>
      <w:fldChar w:fldCharType="start" w:dirty="true"/>
    </w:r>
    <w:r>
      <w:instrText>
    /l 1-3</w:instrText>
    </w:r>
    <w:r>
      <w:fldChar w:fldCharType="separate"/>
    </w:r>

XML semantics - CT_FldChar
--------------------------

* The `w:instrText` element specifies the field codes for the simple field.

* The `w:fldCharType` element specifies the type of the current complex field
  character in the document.
  The possible values for this attribute are defined by the `ST_FldCharType`
  simple type

* The `w:fldLock` element prevents the field code from updating.
  The possible values for this attribute are defined by the ST_OnOff simple type

* The `w:dirty` flags that the element needs updating.

* The parent element is `w:r` - run element

* Possible child element is `ffData` (Form Field Properties)

* If a complex field character is located in an inappropriate location in a
  WordprocessingML document, then its presence shall be ignored and no field
  shall be present in the resulting document when displayed.

* If a complex field is not closed before the end of a document story, then no
  field shall be generated and each individual run shall be processed as if the
  field characters did not exist.

XML semantics - CT_SimpleField
------------------------------

* The semantics of this field are defined via its field codes


Related Schema Definitions
--------------------------

::

  <xsd:complexType name="CT_SimpleField">
    <xsd:sequence>
      <xsd:element name="fldData" type="CT_Text" minOccurs="0" maxOccurs="1"/>
      <xsd:group ref="EG_PContent" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="instr" type="s:ST_String" use="required"/>
    <xsd:attribute name="fldLock" type="s:ST_OnOff"/>
    <xsd:attribute name="dirty" type="s:ST_OnOff"/>
  </xsd:complexType>

  <xsd:complexType name="CT_FldChar">
      <xsd:choice>
          <xsd:element name="fldData" type="CT_Text" minOccurs="0" maxOccurs="1"/>
          <xsd:element name="ffData" type="CT_FFData" minOccurs="0" maxOccurs="1"/>
          <xsd:element name="numberingChange" type="CT_TrackChangeNumbering" minOccurs="0"/>
      </xsd:choice>
      <xsd:attribute name="fldCharType" type="ST_FldCharType" use="required"/>
      <xsd:attribute name="fldLock" type="s:ST_OnOff"/>
      <xsd:attribute name="dirty" type="s:ST_OnOff"/>
  </xsd:complexType>

  <xsd:simpleType name="ST_FldCharType">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="begin"/>
      <xsd:enumeration value="separate"/>
      <xsd:enumeration value="end"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:group name="EG_PContent">
    <xsd:choice>
      <xsd:group ref="EG_ContentRunContent" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="fldSimple" type="CT_SimpleField" minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="hyperlink" type="CT_Hyperlink"/>
      <xsd:element name="subDoc" type="CT_Rel"/>
    </xsd:choice>
  </xsd:group>

  <xsd:group name="EG_ContentRunContent">
    <xsd:choice>
      <xsd:element name="customXml" type="CT_CustomXmlRun"/>
      <xsd:element name="smartTag" type="CT_SmartTagRun"/>
      <xsd:element name="sdt" type="CT_SdtRun"/>
      <xsd:element name="dir" type="CT_DirContentRun"/>
      <xsd:element name="bdo" type="CT_BdoContentRun"/>
      <xsd:element name="r" type="CT_R"/>
      <xsd:group ref="EG_RunLevelElts" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:choice>
  </xsd:group>