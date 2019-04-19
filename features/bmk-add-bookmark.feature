Feature: Modifying bookmarks in various story parts
  In order to add, remove or modify bookmarks in different story parts
  As a developer using python-docx
  I need bookmark start and end functionality in different story-elements


  Scenario Outline: Add bookmark to different story elements
    Given a <element>
     When I start a bookmark named test in <element> as bookmark
      And I terminate bookmark in <element>
     Then len(bookmarks) == 1
      And bookmarks[0] has name test

  Examples: Different elements in story
    | element   |
    | document  |
    | paragraph |
    | header    |
    | footer    |

  Scenario Outline: Removing bookmarks from document
    Given a Bookmarks object of length 5 as bookmarks
     When I remove bookmark <name> by <identifier>
     Then len(bookmarks) == 4
      And no bookmark named bookmark_body is found in document

  Examples: Removing bookmark by name or index
    | name           | identifier |
    | bookmark_body  | name       |
    | 0              | index      |

  @wip
  Scenario: Check if bookmark is empty
    Given a paragraph
     When I start a bookmark named test in paragraph as bookmark
      And I terminate bookmark in paragraph
     Then bookmark.empty == True

  @wip
  Scenario: Check if bookmark is not empty
    Given a paragraph
     When I start a bookmark named test in paragraph as bookmark
      And I set the paragraph text
      And I terminate bookmark in paragraph
     Then bookmark.empty == False
