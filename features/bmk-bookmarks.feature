Feature: Access a bookmark
  In order to operate on document bookmark objects
  As a developer using python-docx
  I need sequence operations on Bookmarks


  Scenario: Bookmarks is a sequence
    Given a Bookmarks object of length 6 as bookmarks
     Then len(bookmarks) == 6
      And bookmarks[1] is a _Bookmark object
      And iterating bookmarks produces 6 _Bookmark objects

  Scenario Outline: Bookmarks provides name based access
    Given a Bookmarks object of length 6 as bookmarks
     Then bookmarks.get(<name>) returns _Bookmark named <name> and id <id>

    Examples: Named Bookmarks
        | name               | id |
        | bookmark_body      | 2  |
        | bookmark_endnote   | 1  |
        | bookmark_footer    | 7  |
        | bookmark_footnote  | 0  |
        | bookmark_header    | 6  |
        | bookmark_comment   | 4  |
