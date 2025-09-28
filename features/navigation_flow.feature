@happy @smoke @navigation
Feature: Navigation Flow
  As a user of the financial planning tools
  I want to navigate between different calculators
  So that I can access all available planning tools

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @navigation-hub-to-calculator
  Scenario: Navigation hub to any calculator CTA works
    Given I can see all calculator links on the homepage
    When I click on the "Retirement" calculator link
    Then I am navigated to the Retirement Calculator page
    And the calculator page loads successfully
    When I navigate back to the homepage
    And I click on the "Social Security" calculator link
    Then I am navigated to the Social Security Calculator page
    And the calculator page loads successfully
    And accessibility violations are not critical
