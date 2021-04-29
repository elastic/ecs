Feature: General
  Scenario: The agent.hostname field should not be populated.
    Given an event
    Then the agent.hostname field is not present

  Scenario: The agent.name field should not be equal to host.name field.
    Given an event
    And the agent.name field is present
    And the host.name field is present
    Then the agent.name field should not equal the host.name field
