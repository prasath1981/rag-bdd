@happy @smoke @emergency-fund
Feature: Emergency Fund Calculator
  As a user planning for emergencies
  I want to use the emergency fund calculator
  So that I can determine how long it takes to reach my emergency fund goal

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @emergency-fund-months-to-goal
  Scenario: Emergency Fund months to goal computed
    Given I open the Emergency Fund Calculator
    When I enter monthly expenses 4000, current savings 5000, target months 6
    Then I see the months to goal calculation
    And the result contains non-empty values
    And accessibility violations are not critical
