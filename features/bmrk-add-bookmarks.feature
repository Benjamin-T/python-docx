Feature: Add a bookmark to text
  In order to mark a location in my document
  As a developer using python-docx
  I need the ability to add a bookmark
  
  @wip
  Scenario: Adding a bookmark to a document
    Given a document
     When I start a body bookmark
      And I end a bookmark
    Then the document contains a bookmark

  @wip
  Scenario: Adding a bookmark to a paragraph
    Given a document 
     When I start a paragraph bookmark
      And I end a bookmark
     Then the document contains a bookmark

  @wip
  Scenario: Adding a bookmark to a run
    Given a document
     When I add a paragraph
      And I add a run to the paragraph
      And I add text to the run
      And I start a run bookmark
      And I end a bookmark
     Then the document contains a bookmark
