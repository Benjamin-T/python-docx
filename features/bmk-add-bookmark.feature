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
