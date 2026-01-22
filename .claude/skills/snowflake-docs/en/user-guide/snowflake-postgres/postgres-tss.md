---
auto_generated: true
description: Preview Feature — Open
last_scraped: '2026-01-14T16:57:51.843789+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/snowflake-postgres/postgres-tss
title: Snowflake Postgres Tri-Secret Secure | Snowflake Documentation
---

1. [Overview](../../guides/README.md)
2. [Snowflake Horizon Catalog](../snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../../guides/overview-connecting.md)
6. [Virtual warehouses](../warehouses.md)
7. [Databases, Tables, & Views](../../guides/overview-db.md)
8. [Data types](../../data-types.md)
10. Data Integration

    - [Snowflake Openflow](../data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](../tables-iceberg.md)
      - [Snowflake Open Catalog](../opencatalog/overview.md)
11. Data engineering

    - [Data loading](../../guides/overview-loading-data.md)
    - [Dynamic Tables](../dynamic-tables-about.md)
    - [Streams and Tasks](../data-pipelines-intro.md)
    - [dbt Projects on Snowflake](../data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](../storage-management/storage-lifecycle-policies.md)
13. [Migrations](../../migrations/README.md)
15. [Queries](../../guides/overview-queries.md)
16. [Listings](../../collaboration/collaboration-listings-about.md)
17. [Collaboration](../../guides/overview-sharing.md)
19. [Snowflake AI & ML](../../guides/overview-ai-features.md)
21. [Snowflake Postgres](about.md)

    * [Creating instances](postgres-create-instance.md)
    * [Connecting](connecting-to-snowflakepg.md)
    * [Managing instances](managing-instances.md)
    * Monitoring
    * [Evaluate cost](postgres-cost.md)
    * [Insights](insights.md)
    * [Logging](postgres-logging.md)
    * Security and networking
    * [Networking](postgres-network.md)
    * [Tri-Secret Secure](postgres-tss.md)
    * Reference
    * [Instance sizes](postgres-instance-sizes.md)
    * [Extensions](postgres-extensions.md)
    * [Server settings](postgres-server-settings.md)
23. [Alerts & Notifications](../../guides/overview-alerts.md)
25. [Security](../../guides/overview-secure.md)
26. [Data Governance](../../guides/overview-govern.md)
27. [Privacy](../../guides/overview-privacy.md)
29. [Organizations & Accounts](../../guides/overview-manage.md)
30. [Business continuity & data recovery](../replication-intro.md)
32. [Performance optimization](../../guides/overview-performance.md)
33. [Cost & Billing](../../guides/overview-cost.md)

[Guides](../../guides/README.md)[Snowflake Postgres](about.md)Tri-Secret Secure

# Snowflake Postgres Tri-Secret Secure[¶](#snowpg-tri-secret-secure "Link to this heading")

[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Preview Feature](../../release-notes/preview-features) — Open

Available to all accounts.



[![Snowflake logo in black (no text)](../../_images/logo-snowflake-black.png)](../../_images/logo-snowflake-black.png) [Business Critical Feature](../intro-editions)

Requires Business Critical Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

[Tri-Secret Secure](../security-encryption-tss) is supported for Snowflake Postgres instance storage. Snowflake Postgres Tri-Secret Secure
instance storage uses a self-service registration process similar to that outlined in [Tri-Secret Secure self-service in Snowflake](../security-encryption-tss-self-serve)
with the following differences:

* Snowflake Postgres Tri-Secret Secure uses different Snowflake system functions for activation and CMK registration.
* Snowflake Postgres Tri-Secret Secure does not support private connectivity.
* Snowflake Postgres Tri-Secret Secure does not support self-registration with support activation.
* While Snowflake Postgres Tri-Secret Secure supports registering and activating new CMKs, it does not support rekeying of existing Snowflake Postgres
  instances with new CMKs.

Attention

Before engaging with Snowflake to enable Snowflake Postgres Tri-Secret Secure for your account, you should carefully consider your responsibility for
safeguarding your key as mentioned in [Customer-managed keys](../security-encryption-manage.html#label-customer-managed-keys). If the customer managed key (CMK) in the composite master key hierarchy is revoked,
your data can no longer be decrypted by Snowflake.

If you have any questions or concerns, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Snowflake also bears the same responsibility for the keys that we maintain. As with all security-related aspects of our service, we treat
this responsibility with the utmost care and vigilance.

All of our keys are maintained under strict policies that have enabled us to earn the highest security accreditations, including SOC 2
Type II, PCI-DSS, HIPAA and [HITRUST CSF](../intro-cloud-platforms.html#label-hitrust-csf-cert).

## Activate Snowflake Postgres Tri-Secret Secure[¶](#activate-snowpg-tri-secret-secure "Link to this heading")

This procedure works on all cloud provider platforms that Snowflake supports. See your specific cloud provider documentation for any steps
taken on the cloud provider platform.

To create and register your CMK, and then activate Snowflake Postgres Tri-Secret Secure, complete the following steps:

1. On the cloud provider, create a CMK.

   Do this step in the key management service (KMS) on the cloud platform that hosts your Snowflake account.
2. In Snowflake, call the [SYSTEM$REGISTER\_CMK\_INFO\_POSTGRES](../../sql-reference/functions/system_register_cmk_info_postgres) system function.

   * This system function registers your CMK with your Snowflake account for use with Snowflake Postgres Tri-Secret Secure.
   * Double-check the system function arguments to make sure they are correct for the cloud platform that hosts your Snowflake account.
3. In Snowflake, call the [SYSTEM$GET\_CMK\_INFO\_POSTGRES](../../sql-reference/functions/system_get_cmk_info_postgres) system function.

   This system function returns the registration status and details for the CMK that you registered.
4. In Snowflake, call the [SYSTEM$GET\_CMK\_CONFIG\_POSTGRES](../../sql-reference/functions/system_get_cmk_config_postgres) system function.

   This system function generates the information required for your cloud provider to allow Snowflake to access your CMK.

   Note

   If Microsoft Azure hosts your Snowflake account, you must pass the `tenant_id` value into the function.
5. In Snowflake, call the [SYSTEM$VERIFY\_CMK\_INFO\_POSTGRES](../../sql-reference/functions/system_verify_cmk_info_postgres) system function.

   This system function confirms connectivity between your Snowflake account and your CMK.
6. In Snowflake, call the [SYSTEM$ACTIVATE\_CMK\_INFO\_POSTGRES](../../sql-reference/functions/system_activate_cmk_info_postgres) system function.

   This system function activates Snowflake Postgres Tri-Secret Secure with your newly registered CMK.

   Important

   Snowflake Postgres Tri-Secret Secure does not support rekeying of existing Snowflake Postgres instances. This means that:

   * Snowflake Postgres instances that were created before any CMK was activated will not use Snowflake Postgres Tri-Secret Secure.
   * Snowflake Postgres instances that were created while a prior CMK as active will continue to use that prior CMK.
   * Only Snowflake Postgres primary instances that are created after a CMK is activated will use that CMK.
   * Snowflake Postgres replicas and forks will always use the CMK in use by their primary instance.

### View the status of your CMK[¶](#view-the-status-of-your-cmk "Link to this heading")

You can call [SYSTEM$GET\_CMK\_INFO\_POSTGRES](../../sql-reference/functions/system_get_cmk_info_postgres) at any time, to check the registration and activation status of your CMK.

For example, depending on when you call SYSTEM$GET\_CMK\_INFO\_POSTGRES after the Snowflake Postgres Tri-Secret Secure activation process completes, the
function returns output that includes `...is activated...`. This means that your Snowflake account is using Snowflake Postgres Tri-Secret Secure with the
CMK that you registered.

### Change the CMK for Snowflake Postgres Tri-Secret Secure[¶](#change-the-cmk-for-snowpg-tri-secret-secure "Link to this heading")

Snowflake system functions support changing your customer-managed key (CMK), based on your security needs. Use the same steps to register a new CMK as the
steps that you followed to register your initial CMK. When you complete those steps again by using a new key, the output of the system functions
differs. Read the output from each system function that you call during self-service registration to confirm that you have changed your key.

### Deregister your current CMK[¶](#deregister-your-current-cmk "Link to this heading")

You can only register one CMK at a time with Snowflake Postgres Tri-Secret Secure. When you register your CMK, if the [SYSTEM$REGISTER\_CMK\_INFO\_POSTGRES](../../sql-reference/functions/system_register_cmk_info_postgres)
function fails because a different CMK exists, call the [SYSTEM$DEREGISTER\_CMK\_INFO\_POSTGRES](../../sql-reference/functions/system_deregister_cmk_info_postgres) system function, as prompted.

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

1. [Activate Snowflake Postgres Tri-Secret Secure](#activate-snowpg-tri-secret-secure)