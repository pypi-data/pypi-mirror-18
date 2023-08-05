Feature: Google Search
    As the developer of a web testing framework I want to know that my
    framework functions correctly, and that it can interact with the google
    search page.

Scenario: Open Home Page
    Given I open "https://www.google.co.uk" in my web browser
     Then I expect the url to start with "https://www.google.co.uk"

Scenario: Search for "Fattoush"
    Given I open "https://www.google.com" in my web browser
     When I type "Fattoush" into the search box
      And I submit the search
     Then I expect the top result to contain the string "Fattoush"
