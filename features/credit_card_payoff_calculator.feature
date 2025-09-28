@happy @smoke @credit-card
Feature: Credit Card Payoff Calculator
  As a user planning to pay off credit card debt
  I want to use the credit card payoff calculator
  To understand my payoff timeline and strategy

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @credit-card-payoff-timeline
  Scenario: Credit Card payoff timeline calculation
    Given I open the Pay Off Credit Cards Calculator
    When I enter current balance 5000, interest rate 18.5%, minimum payment 150
    Then I see the payoff timeline calculation
    And the result contains non-empty values
    And accessibility violations are not critical
