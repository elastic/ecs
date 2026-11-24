# 0059: Add as.type

- Stage: **Proposal**
- Date: **TBD**
- Target maturity: **beta**

## Summary

Add `as.type` to the existing `as` fieldset to enable standardised classification of Autonomous Systems. This provides defenders with a mechanism to flag anomalous network behaviour, such as the use of cloud or hosting infrastructure in Adversary-in-the-Middle (AitM) attacks.

## Usage

With the increase in session token theft and AitM phishing campaigns using toolkits like Evilginx, defenders require a method to identify malicious sessions that originate from, or span, anomalous networks. 

A classic AitM scenario involves a victim being phished into visiting a landing page hosted on data centre infrastructure. As the user logs in, the attacker's reverse proxy intercepts the live authentication exchange. The hijacked session token is then utilised simultaneously by the legitimate user (from their standard location) and maliciously by the attacker (often routing through a different hosting provider or residential proxy network). 

With `as.type`:

- Detection rules can flag anomalies such as corporate traffic originating from non-corporate networks (dependent on individual organisational setup).
- Analytics engines can alert when an active token spans multiple conflicting network environments, such as a single session shifting between `isp` and `hosting` types within a short time window (a primary indicator of an AitM compromise).

## Fields

Proposed definition (also in [`rfcs/text/0059/as.yaml`](./0059/as.yaml)):

```yaml
- name: type
  level: extended
  beta: This field is beta and subject to change.
  type: keyword
  description: >
    Functional category or classification of the Autonomous System.
    Because an Autonomous System can have multiple functions, this
    field is designed to accept an array of values.
  example: hosting
  allowed_values:
    - name: hosting
      description: >
        Cloud service providers, datacenters, or dedicated server networks
        (e.g., AWS, OVH).
    - name: isp
      description: >
        Internet Service Providers, i.e., consumer-facing fixed-line 
        or broadband internet services (e.g., British Telecom).
    - name: cellular
      description: >
        Mobile carrier networks (e.g., Vodafone, T-Mobile). 
    - name: cdn 
      description: > 
        Content Delivery Networks, i.e., edge networks designed to cache 
        and rapidly deliver web content (e.g., Cloudflare, Akamai).
    - name: vpn 
      description: > 
        Anonymisation services.
    - name: business 
      description: > 
        Enterprise transit networks serving private corporate infrastructure or offices.
    - name: education
      description: > 
        Academic networks allocated strictly to universities, schools, or research labs.
    - name: government
      description: >
        Municipal, state, or federal networks assigned to public sector infrastructure.
```

This is a single additive keyword under the existing `as` group. No child objects or `flattened` fields are required.

## Source data

### OXL Risk Database Lists
[OXL Risk Database Lists](https://codeberg.org/OXL/risk-db-lists) is an open-source repository that aggregates network and ASN reputations. It maps IPs and ASNs to classifications, including `hosting`, `vpn`, `isp`, and `education`. However, the format is individual CSV and TXT files with the classification as a suffix, e.g., `kind_education.csv`, `kind_hosting.txt`. 

### MaxMind
[MaxMind GeoIP2 / GeoLite2](https://www.maxmind.com/en/geoip-enterprise-database) is a commercial solution providing in-depth contextual information about IP addresses.

```json
{
  "traits": {
    "autonomous_system_number": 217,
    "autonomous_system_organization": "University of Minnesota",
    "connection_type": "Corporate",
    "domain": "umn.edu",
    "ip_address": "128.101.101.101"
  }
}
```

### IPinfo
[IPinfo.io](https://ipinfo.io) provides commercial enrichment endpoints that output network routing types alongside ASN metadata.

```json
{
  "ip": "172.56.21.89",
  "asn": {
    "asn": "AS21928",
    "name": "T-Mobile USA, Inc.",
    "domain": "t-mobile.com",
    "route": "172.56.0.0/16",
    "type": "isp"
  }
}
```


## Scope of impact

* **Ingestion:** No breaking changes. The field is additive. Existing integrations that do not populate it continue to work.
* **Usage:** Enables anomalous network detection and behavioural profiling. No breaking change to existing `as.*` consumers.
* **ECS project:** One new field in `schemas/as.yml`, alongside regenerated documentation and generated schema artefacts. No existing fields are modified.

## Concerns

* **Why place this under `as` instead of `source`/`destination`/etc?** 
Classifications targeting the raw IP enable more granular categories, e.g., `tor`, `proxy`, etc., which could be highly valuable for defenders. However, adding an `ip_classification` field under `source` would require the same to be done for `destination`, `client`, `server` and `threat.indicator`. 
Adding `type` to the `as` field loses granularity but enables the field to be injected wherever the `as` block is used, while still maintaining a reasonable level of utility.

* **Why not under `network`?**
The `network` field group is reserved for physical and logical characteristics of the traffic session or packet transit itself, rather than attributes of the organisation owning and routing the IP ranges.


## People

* @apocrypsis | author

## References

### RFC Pull Requests

* Proposal:  (this PR)