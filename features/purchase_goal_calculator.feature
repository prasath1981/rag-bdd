@happy @smoke @purchase-goal
Feature: Purchase Goal Calculator
  As a user planning for a major purchase
  I want to use the purchase goal calculator
  So that I can determine the timeline to reach my purchase goal

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @purchase-goal-timeline
  Scenario: Purchase Goal timeline to purchase shown
    Given I open the Purchase Goal Calculator
    When I enter target amount 25000, current savings 5000, monthly contribution 500
    Then I see the timeline to purchase calculation
    And the result contains non-empty values
    And accessibility violations are not critical
