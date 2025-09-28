Feature: Retirement Calculator
Scenario: Retirement basic projection calculation with accessibility violations

Given I click on the retirement calculator link
When I enter my age as 35, income as 120000, savings as 50000, and contribution rate as 10%
Then I should see a projected retirement outcome card
And I should be notified of accessibility violations

Feature: Retirement Calculator
Scenario: Adjusting contribution updates retirement outcome

Given I open the Retirement Calculator
When I enter age 35, income 120000, savings 50000, and contribute 10%
And I see a projected retirement outcome card
When I adjust the contribution to 15%
Then the projected outcome should be updated
And the result should display different values than before
And there should be no critical accessibility violations