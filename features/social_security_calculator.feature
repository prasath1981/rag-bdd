@happy @smoke @social-security
Feature: Social Security Calculator
  As a user planning for retirement
  I want to use the social security calculator
  So that I can estimate my social security benefits

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @social-security-benefit-estimate
  Scenario: Social Security benefit estimate with default FRA
    Given I open the Social Security Calculator
    When I enter current age 45, annual earnings 80000, retirement age 67
    Then I see a social security benefit estimate
    And the result contains non-empty values
    And accessibility violations are not critical
