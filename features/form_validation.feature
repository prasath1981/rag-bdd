@happy @smoke @validation
Feature: Form Validation
  As a user of the financial planning tools
  I want proper form validation
  So that I receive helpful feedback when entering invalid data

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @form-validation-pass
  Scenario: Basic form validation passes with valid data
    Given I open the Retirement Calculator
    When I enter valid retirement planning data
    Then the form accepts the input without validation errors
    And I can proceed to see results
    And accessibility violations are not critical

  @form-validation-feedback
  Scenario: Form provides helpful validation feedback
    Given I open the Emergency Fund Calculator
    When I enter invalid data in required fields
    Then I see appropriate validation messages
    And the form prevents submission until corrected
    And accessibility violations are not critical
