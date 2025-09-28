Feature: Retirement Calculator
Scenario: Custom retirement age projection update
Given I open the Retirement Calculator
When I enter age 35, income 120000, savings 50000, contribute 10%
And I see a projected retirement outcome card
When I set a custom retirement age of 65
Then the projected outcome is updated based on the new retirement age
And the result reflects the changes made
And accessibility violations are not critical

Matches:
1. [C:\Users\adspr\pythonscripts\rag-bdd\features\retirement_calculator.feature::Retirement adjust contribution updates result] - 60% similarity
2. [C:\Users\adspr\pythonscripts\rag-bdd\features\retirement_calculator.feature::Retirement adjust contribution updates result] - 60% similarity