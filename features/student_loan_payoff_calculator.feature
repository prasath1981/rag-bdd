@happy @smoke @student-loan
Feature: Student Loan Payoff Calculator
  As a user planning to pay off student loans
  I want to use the student loan payoff calculator
  To understand my payoff timeline and strategy

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @student-loan-payoff-timeline
  Scenario: Student Loan payoff timeline calculation
    Given I open the Pay Off Student Loans Calculator
    When I enter loan balance 25000, interest rate 6.5%, monthly payment 300
    Then I see the payoff timeline calculation
    And the result contains non-empty values
    And accessibility violations are not critical
