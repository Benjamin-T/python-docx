
Bookmarks
=========

WordprocessingML allows for custom specification of bookmarks at different
locations within the document. The bookmarks object will therefore be available
from the main document API. The location will be docx.document.
The bookmarks object will be a list like sequence object, it will be possible
to iterate through the different bookmarks. A __len__ property is also
required to provide the bookmark a unique id, to go along with a new bookmark.
A bookmark is a separate object which has no particular place, therefore the
both the Bookmark and the Bookmarks objects will be placed in the
docx.text.bookmark location.

A Bookmark object has two properties, a name and an id which has to be
identical within a single bookmark. A Bookmark can be started in
a run or a paragraph and ended in a different part of the document.
A working bookmark consists of a bookmarkStart element and a
bookmarkEnd element, matched by unique id's.

Bookmarks can be used to mark certain location in the document. Insertion
of a bookmark can be done from either document, paragraph or run level.

There are many applications for the bookmark, many are found in the 'tracked
changes' like operations in word. The intended use for this implementation lies
more in the captions and crossrefernces. It could however also be extended to
also include specific cell locations in a table.

Protocol
--------

.. highlight:: python

# Adding a bookmark:

    >>> bookmarks = document.bookmarks
    >>> bookmarks
    <docx.text.bookmark.Bookmarks object at 0x000000000>
    >>> bookmark = document.start_bookmark(name='test')
    # Some  code here
    >>> document.end_bookmark(bookmark)
    >>> len(bookmarks)
    1
    >>> bookmarks.get(name='test')
    docx.text.bookmark.Bookmark object at 0x000000001>
    >>> bookmarks[0]
    docx.text.bookmark.Bookmark object at 0x000000001>

Word Behavior
-------------

When a <w:bookmarkStart> element is present, word inspects whether it has a
name and an id. This id is used to match the corresponding <w:bookmarkEnd>
element. Without the ID the document is non compliant.

Word is capable of redefining the id's, the bookmark names can be found in the
cross reference dialog.

An unclosed bookmark (i.e. only a <w:bookmarkStart> element is inserted, but
the corresponding <W:bookmarkEnd> element is missing.) it will be ignored by
word.


XML Semantics
-------------

* The bookmark XML element predates the real structured XML element list of
word and has therefore a less strict location structure

* The id's in the elements need be identical for a bookmark to work.

* The <w:bookmarkStart> element requires the <w:id> and <w:name> elements.

* The <w:bookmarkEnd> element only needs to contain the <w:id> element.

Specimen XML
------------

.. highlight:: xml

::

  <w:p>
     <w:r>
       <w:t>Example</w:t>
     </w:r>
     <w:bookmarkStart w:id="0" w:name="sampleBookmark" />
     <w:r>
       <w:t xml:space="preserve"> text.</w:t>
     </w:r>
  </w:p>
  <w:p>
    <w:r>
      <w:t>Example</w:t>
    </w:r>
      <w:bookmarkEnd w:id="0" />
    <w:r>
      <w:t xml:space="preserve"> text.</w:t>
    </w:r>
  </w:p>

MS API Protocol
---------------

The MS API defines a `Bookmarks` object which is a collection of
`Bookmark objects`

.. _Bookmarks object:
  https://msdn.microsoft.com/en-us/vba/word-vba/articles/bookmarks-object-word

.. _Bookmark objects:
   https://msdn.microsoft.com/en-us/vba/word-vba/articles/bookmark-object-word


Schema excerpt
--------------

::

  <xsd:complexType name="CT_Body">
    <xsd:sequence>
      <xsd:choice minOccurs="0" maxOccurs="unbounded">
        <xsd:element name="p"                           type="CT_P"/>
        <xsd:element name="tbl"                         type="CT_Tbl"/>
        <xsd:element name="customXml"                   type="CT_CustomXmlBlock"/>
        <xsd:element name="sdt"                         type="CT_SdtBlock"/>
        <xsd:element name="proofErr"                    type="CT_ProofErr"/>
        <xsd:element name="permStart"                   type="CT_PermStart"/>
        <xsd:element name="permEnd"                     type="CT_Perm"/>
        <xsd:element name="ins"                         type="CT_RunTrackChange"/>
        <xsd:element name="del"                         type="CT_RunTrackChange"/>
        <xsd:element name="moveFrom"                    type="CT_RunTrackChange"/>
        <xsd:element name="moveTo"                      type="CT_RunTrackChange"/>
        <xsd:element  ref="m:oMathPara"                 type="CT_OMathPara"/>
        <xsd:element  ref="m:oMath"                     type="CT_OMath"/>
        <xsd:element name="bookmarkStart"               type="CT_Bookmark"/>
        <xsd:element name="bookmarkEnd"                 type="CT_MarkupRange"/>
        <xsd:element name="moveFromRangeStart"          type="CT_MoveBookmark"/>
        <xsd:element name="moveFromRangeEnd"            type="CT_MarkupRange"/>
        <xsd:element name="moveToRangeStart"            type="CT_MoveBookmark"/>
        <xsd:element name="moveToRangeEnd"              type="CT_MarkupRange"/>
        <xsd:element name="commentRangeStart"           type="CT_MarkupRange"/>
        <xsd:element name="commentRangeEnd"             type="CT_MarkupRange"/>
        <xsd:element name="customXmlInsRangeStart"      type="CT_TrackChange"/>
        <xsd:element name="customXmlInsRangeEnd"        type="CT_Markup"/>
        <xsd:element name="customXmlDelRangeStart"      type="CT_TrackChange"/>
        <xsd:element name="customXmlDelRangeEnd"        type="CT_Markup"/>
        <xsd:element name="customXmlMoveFromRangeStart" type="CT_TrackChange"/>
        <xsd:element name="customXmlMoveFromRangeEnd"   type="CT_Markup"/>
        <xsd:element name="customXmlMoveToRangeStart"   type="CT_TrackChange"/>
        <xsd:element name="customXmlMoveToRangeEnd"     type="CT_Markup"/>
        <xsd:element name="altChunk"                    type="CT_AltChunk"/>
      </xsd:choice>
      <xsd:element name="sectPr" type="CT_SectPr" minOccurs="0" maxOccurs="1"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_Bookmark">
    <xsd:complexContent>
      <xsd:extension base="CT_BookmarkRange">
        <xsd:attribute name="name" type="ST_String" use="required">
          <xsd:annotation>
            <xsd:documentation>Bookmark Name</xsd:documentation>
          </xsd:annotation>
        </xsd:attribute>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>

  <xsd:complexType name="CT_BookmarkRange">
    <xsd:complexContent>
      <xsd:extension base="CT_MarkupRange">
        <xsd:attribute name="colFirst" type="ST_DecimalNumber" use="optional">
          <xsd:annotation>
            <xsd:documentation>First Table Column Covered By Bookmark</xsd:documentation>
          </xsd:annotation>
        </xsd:attribute>
        <xsd:attribute name="colLast" type="ST_DecimalNumber" use="optional">
          <xsd:annotation>
            <xsd:documentation>Last Table Column Covered By Bookmark</xsd:documentation>
          </xsd:annotation>
        </xsd:attribute>
      </xsd:extension>
    </xsd:complexContent>
  </xsd:complexType>
