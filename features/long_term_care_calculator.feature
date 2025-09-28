@happy @smoke @long-term-care
Feature: Long Term Care Calculator
  As a user planning for healthcare costs
  I want to use the long term care calculator
  So that I can estimate nursing home costs

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @long-term-care-cost-estimate
  Scenario: Long Term Care nursing home cost estimate shows
    Given I open the Long Term Care Calculator
    When I enter current age 50, care type "nursing home", location "national average"
    Then I see a nursing home cost estimate
    And the result contains non-empty values
    And accessibility violations are not critical
