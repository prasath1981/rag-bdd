@happy @smoke @protected-income
Feature: Protected Income Calculator
  As a user planning for retirement income
  I want to use the protected income calculator
  So that I can estimate annuity income projections

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @protected-income-projection
  Scenario: Protected Income annuity income projection visible
    Given I open the Protected Income Calculator
    When I enter investment amount 100000, age 55, income start age "65"
    Then I see an income projection result
    And the result contains non-empty values
    And accessibility violations are not critical
