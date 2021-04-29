Feature: Address field should be populated if ip or domain is polulated.
  Scenario: If the source.ip field exists then so should the source.address field.
    Given an event
    And the source.ip field is present
    Then the source.address field is present

  Scenario: If the source.domain field exists then so should source.address field.
    Given an event
    And the source.domain field is present
    Then the source.address field is present

  Scenario: If the destination.ip field exists then so should the destination.address field.
    Given an event
    And the destination.ip field is present
    Then the destination.address field is present

  Scenario: If the destination.domain field exists then so should the destination.address field.
    Given an event
    And the destination.domain field is present
    Then the destination.address field is present