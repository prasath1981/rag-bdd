@happy @smoke @disclaimer
Feature: Disclaimer Verification
  As a user of the financial planning tools
  I want to see appropriate disclaimers
  So that I understand the educational nature of the tools

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @disclaimer-present
  Scenario: Disclaimer present on results page for educational use
    Given I am on the Financial Planning Tools homepage
    Then I can see disclaimer text about educational use
    When I open the Retirement Calculator
    And I enter age 35, income 120000, savings 50000, contribute 10%
    And I see a projected retirement outcome card
    Then the disclaimer is visible on the results page
    And the disclaimer mentions educational or informational purpose
    And accessibility violations are not critical
