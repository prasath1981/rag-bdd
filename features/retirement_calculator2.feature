@happy @smoke @retirement
Feature: Retirement Calculator
  As a user planning for retirement
  I want to use the retirement calculator
  So that I can estimate my retirement savings needs

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @retirement-basic-projection
  Scenario: Retirement basic projection calculation
    Given click on the retirement calculator link
    When I enter age 35, income 120000, savings 50000, contribute 10%
    Then I see a proj retirement outcome card
     And accessibility violations met

  @retirement-adjust-contribution
  Scenario: Retirement adjust contribution updates result
    Given I open the Retirement Calculator
    When I enter age 35, income 120000, savings 50000, contribute 10%
    And I see a projected retirement outcome card
    When I adjust the contribution to 15%
    Then the projected outcome is updated
    And the result shows different values than before
    And accessibility violations are not critical
