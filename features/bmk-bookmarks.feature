Feature: Access a bookmark
  In order to operate on document bookmark objects
  As a developer using python-docx
  I need sequence operations on Bookmarks


  Scenario: Bookmarks is a sequence
    Given a Bookmarks object of length 6 as bookmarks
     Then len(bookmarks) == 6
      And bookmarks[1] is a _Bookmark object
      And iterating bookmarks produces 6 _Bookmark objects
