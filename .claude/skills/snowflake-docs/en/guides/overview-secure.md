---
auto_generated: true
description: Snowflake provides industry-leading features that help ensure you can
  configure the highest levels of security for your account and users, as well as
  all the data you store in Snowflake.
last_scraped: '2026-01-14T16:54:13.942030+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/guides-overview-secure
title: Securing Snowflake | Snowflake Documentation
---

1. [Overview](README.md)
2. [Snowflake Horizon Catalog](../user-guide/snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](overview-connecting.md)
6. [Virtual warehouses](../user-guide/warehouses.md)
7. [Databases, Tables, & Views](overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../user-guide/data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../user-guide/tables-iceberg.md)
      - [Snowflake Open Catalog](../user-guide/opencatalog/overview.md)
11. Data engineering

    - [Data loading](overview-loading-data.md)
    - [Dynamic Tables](../user-guide/dynamic-tables-about.md)
    - [Streams and Tasks](../user-guide/data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../user-guide/data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](overview-unloading-data.md)
12. [Storage Lifecycle Policies](../user-guide/storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](overview-queries.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](overview-sharing.md)
19. [Snowflake AI & ML](overview-ai-features.md)
21. [Snowflake Postgres](../user-guide/snowflake-postgres/about.md)
23. [Alerts & Notifications](overview-alerts.md)
25. [Security](overview-secure.md)

    * Authentication
    * [Overview of authentication](../user-guide/security-authentication-overview.md)
    * [Authentication policies](../user-guide/authentication-policies.md)
    * [Multi-factor authentication (MFA)](../user-guide/security-mfa.md)")
    * [Federated authentication and SSO](../user-guide/admin-security-fed-auth-overview.md)
    * [Key-pair authentication and rotation](../user-guide/key-pair-auth.md)
    * [Programmatic access tokens](../user-guide/programmatic-access-tokens.md)
    * [OAuth](../user-guide/oauth-intro.md)
    * [Workload identity federation](../user-guide/workload-identity-federation.md)
    * [API authentication and secrets](../user-guide/api-authentication.md)
    * Network security
    * [Malicious IP protection](../user-guide/malicious-ip-protection.md)
    * [Network policies](../user-guide/network-policies.md)
    * [Network rules](../user-guide/network-rules.md)
    * Private connectivity
    * [Inbound private connectivity](../user-guide/private-connectivity-inbound.md)
    * [Outbound private connectivity](../user-guide/private-connectivity-outbound.md)
    * Administration and authorization
    * [Trust Center](../user-guide/trust-center/overview.md)
    * [Sessions and session policies](../user-guide/session-policies.md)
    * [SCIM support](../user-guide/scim-intro.md)
    * [Access control](../user-guide/security-access-control-overview.md)
    * [Encryption](../user-guide/security-encryption-end-to-end.md)
26. [Data Governance](overview-govern.md)
27. [Privacy](overview-privacy.md)
29. [Organizations & Accounts](overview-manage.md)
30. [Business continuity & data recovery](../user-guide/replication-intro.md)
32. [Performance optimization](overview-performance.md)
33. [Cost & Billing](overview-cost.md)

[Guides](README.md)Security

# Securing Snowflake[¶](#securing-snowflake "Link to this heading")

Snowflake provides industry-leading features that help ensure you can configure the highest levels of security for your account and users,
as well as all the data you store in Snowflake.

These topics are intended primarily for administrators (i.e. users with the ACCOUNTADMIN, SYSADMIN, or SECURITYADMIN roles).

## Authentication[¶](#authentication "Link to this heading")

[Authentication policies](user-guide/authentication-policies)
:   Using authentication policies to restrict account and user authentication by client, authentication methods, and more.

[Multi-factor authentication (MFA)](user-guide/security-mfa)
:   Using multi-factor authentication with Snowflake.

[Federated Authentication & SSO](user-guide/admin-security-fed-auth-overview)
:   Topics related to federated authentication to Snowflake.

[Key-pair authentication and key-pair rotation](user-guide/key-pair-auth)
:   Using key-pair authentication to Snowflake.

[Using programmatic access tokens for authentication](user-guide/programmatic-access-tokens)
:   Generating and managing programmatic access tokens for authentication.

[OAuth](user-guide/oauth-intro)
:   Topics related to using Snowflake OAuth and External OAuth to connect to Snowflake.

[Workload identity federation](user-guide/workload-identity-federation)
:   Preferred authentication method for service-to-service workloads.

[External API authentication and secrets](user-guide/api-authentication)
:   Configuring Snowflake to authenticate to external services.

## Network security[¶](#network-security "Link to this heading")

[Malicious IP Protection](user-guide/malicious-ip-protection)
:   Protecting your account from IP addresses that are known to be malicious.

[Controlling network traffic with network policies](user-guide/network-policies)
:   Using network policies to restrict access to Snowflake.

[Network rules](user-guide/network-rules)
:   Using network rules with other Snowflake features to restrict access to and from Snowflake.

## Private connectivity[¶](#private-connectivity "Link to this heading")

[Private connectivity for inbound network traffic](user-guide/private-connectivity-inbound)
:   Using private connectivity to access the Snowflake service, Snowsight, Streamlit in Snowflake, internal stages, and Snowpark Container
    Services.

[Private connectivity for outbound network traffic](user-guide/private-connectivity-outbound)
:   Using private connectivity for external network locations, external functions, external stages, external tables, external
    volumes, and Snowpipe automation.

## Administration and authorization[¶](#administration-and-authorization "Link to this heading")

[Trust Center overview](user-guide/trust-center/overview)
:   Using the Trust Center to evaluate and monitor your account for security risks.

[Snowflake sessions and session policies](user-guide/session-policies)
:   Using session policies to manage your Snowflake session.

[SCIM](user-guide/scim-intro)
:   Topics related to using SCIM to provision users and groups to Snowflake.

[Access Control](user-guide/security-access-control-overview)
:   Topics related to role-based access control (RBAC) in Snowflake.

[End to End Encryption](user-guide/security-encryption-end-to-end)
:   Using end-to-end encryption in Snowflake.

Was this page helpful?

YesNo

[Visit Snowflake](https://www.snowflake.com)

[Join the conversation](https://community.snowflake.com/s/)

[Develop with Snowflake](https://developers.snowflake.com)

[Share your feedback](/feedback)

[Read the latest on our blog](https://www.snowflake.com/blog/)

[Get your own certification](https://learn.snowflake.com)

[Privacy Notice](https://www.snowflake.com/privacy-policy/)[Site Terms](https://www.snowflake.com/legal/snowflake-site-terms/)Cookies Settings© 2026 Snowflake, Inc. All Rights Reserved.

On this page

1. [Authentication](#authentication)
2. [Network security](#network-security)
3. [Private connectivity](#private-connectivity)
4. [Administration and authorization](#administration-and-authorization)