Feature: Source and Destination field sets are populated as a pair
  Scenario: If the source.address field exists then so should the destination.address field.
    Given an event
    And the source.address field is present
    Then the destination.address field is present
    
  Scenario: If the destination.address field exists then so should the source.address
    Given an event
    And the destination.address field is present
    Then the source.address field is present

  Scenario: If source.ip exists then so should destination.ip
    Given an event
    And the source.ip field is present
    Then the destination.ip field is present

  Scenario: If destination.ip exists then so should source.ip
    Given an event
    Given the destination.ip field is present
    Then the source.ip field is present

  Scenario: If source.mac exists then so should destination.mac
    Given an event
    And the source.mac field is present
    Then the destination.mac field is present

  Scenario: If destination.mac exists then so should source.mac
    Given an event
    Given the destination.mac field is present
    Then the source.mac field is present