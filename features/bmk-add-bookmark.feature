Feature: Adding bookmark to main Document story
  In order to add a bookmark to main the main document Story
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
    | run       |