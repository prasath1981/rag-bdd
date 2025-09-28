@happy @smoke @experience-goal
Feature: Experience Goal Calculator
  As a user planning for a life experience
  I want to use the experience goal calculator
  So that I can plan for achieving my experience goals

  Background:
    Given I am on the Financial Planning Tools homepage
    And the page loads successfully

  @experience-goal-outcome
  Scenario: Experience Goal outcome shows summary
    Given I open the Experience Goal Calculator
    When I enter goal type "vacation", estimated cost 8000, timeframe 2 years
    Then I see the goal outcome summary
    And the result contains non-empty values
    And accessibility violations are not critical
