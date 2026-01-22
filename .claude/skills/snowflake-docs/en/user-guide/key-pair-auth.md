---
auto_generated: true
description: This topic describes using key pair authentication and key pair rotation
  in Snowflake.
last_scraped: '2026-01-14T16:57:07.290415+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/user-guide/key-pair-auth
title: Key-pair authentication and key-pair rotation | Snowflake Documentation
---

1. [Overview](../guides/README.md)
2. [Snowflake Horizon Catalog](snowflake-horizon.md)
4. [Applications and tools for connecting to Snowflake](../guides/overview-connecting.md)
6. [Virtual warehouses](warehouses.md)
7. [Databases, Tables, & Views](../guides/overview-db.md)
8. [Data types](../data-types.md)
10. Data Integration

    - [Snowflake Openflow](data-integration/openflow/about.md)
    - Apache Iceberg™

      - [Apache Iceberg™ Tables](tables-iceberg.md)
      - [Snowflake Open Catalog](opencatalog/overview.md)
11. Data engineering

    - [Data loading](../guides/overview-loading-data.md)
    - [Dynamic Tables](dynamic-tables-about.md)
    - [Streams and Tasks](data-pipelines-intro.md)
    - [dbt Projects on Snowflake](data-engineering/dbt-projects-on-snowflake.md)
    - [Data Unloading](../guides/overview-unloading-data.md)
12. [Storage Lifecycle Policies](storage-management/storage-lifecycle-policies.md)
13. [Migrations](../migrations/README.md)
15. [Queries](../guides/overview-queries.md)
16. [Listings](../collaboration/collaboration-listings-about.md)
17. [Collaboration](../guides/overview-sharing.md)
19. [Snowflake AI & ML](../guides/overview-ai-features.md)
21. [Snowflake Postgres](snowflake-postgres/about.md)
23. [Alerts & Notifications](../guides/overview-alerts.md)
25. [Security](../guides/overview-secure.md)

    * Authentication
    * [Overview of authentication](security-authentication-overview.md)
    * [Authentication policies](authentication-policies.md)
    * [Multi-factor authentication (MFA)](security-mfa.md)")
    * [Federated authentication and SSO](admin-security-fed-auth-overview.md)
    * [Key-pair authentication and rotation](key-pair-auth.md)

      + [Troubleshooting](key-pair-auth-troubleshooting.md)
    * [Programmatic access tokens](programmatic-access-tokens.md)
    * [OAuth](oauth-intro.md)
    * [Workload identity federation](workload-identity-federation.md)
    * [API authentication and secrets](api-authentication.md)
    * Network security
    * [Malicious IP protection](malicious-ip-protection.md)
    * [Network policies](network-policies.md)
    * [Network rules](network-rules.md)
    * Private connectivity
    * [Inbound private connectivity](private-connectivity-inbound.md)
    * [Outbound private connectivity](private-connectivity-outbound.md)
    * Administration and authorization
    * [Trust Center](trust-center/overview.md)
    * [Sessions and session policies](session-policies.md)
    * [SCIM support](scim-intro.md)
    * [Access control](security-access-control-overview.md)
    * [Encryption](security-encryption-end-to-end.md)
26. [Data Governance](../guides/overview-govern.md)
27. [Privacy](../guides/overview-privacy.md)
29. [Organizations & Accounts](../guides/overview-manage.md)
30. [Business continuity & data recovery](replication-intro.md)
32. [Performance optimization](../guides/overview-performance.md)
33. [Cost & Billing](../guides/overview-cost.md)

[Guides](../guides/README.md)[Security](../guides/overview-secure.md)Key-pair authentication and rotation

# Key-pair authentication and key-pair rotation[¶](#key-pair-authentication-and-key-pair-rotation "Link to this heading")

This topic describes using key pair authentication and key pair rotation in Snowflake.

## Overview[¶](#overview "Link to this heading")

Snowflake supports using key pair authentication for enhanced authentication security as an alternative to basic authentication, such as
username and password.

This authentication method requires, as a minimum, a 2048-bit RSA key pair. You can generate the Privacy Enhanced Mail (PEM)
private-public key pair using OpenSSL. Some of the [Supported Snowflake Clients](#supported-snowflake-clients) allow using encrypted private keys to connect to
Snowflake. The public key is assigned to the Snowflake user who uses the Snowflake client to connect and authenticate to Snowflake.

Snowflake also supports rotating public keys in an effort to allow compliance with more robust security and governance postures.

## Supported Snowflake clients[¶](#supported-snowflake-clients "Link to this heading")

The following table summarizes support for key pair authentication among Snowflake Clients. A checkmark (✔) indicates full support.
A missing checkmark indicates key pair authentication is not supported.

| Client | Key Pair Authentication | Key Pair Rotation | Unencrypted Private Keys | Encrypted Private Keys |
| --- | --- | --- | --- | --- |
| [Snowflake CLI](../developer-guide/snowflake-cli/index) | ✔ | ✔ | ✔ | ✔ |
| [SnowSQL (CLI client)](snowsql) | ✔ | ✔ | ✔ | ✔ |
| [Snowflake Connector for Python](../developer-guide/python-connector/python-connector) | ✔ | ✔ | ✔ | ✔ |
| [Snowflake Connector for Spark](spark-connector) | ✔ | ✔ | ✔ |  |
| [Snowflake Connector for Kafka](kafka-connector) | ✔ | ✔ | ✔ |  |
| [Snowflake Horizon Catalog endpoint](tables-iceberg-query-using-external-query-engine-snowflake-horizon) | ✔ | ✔ | ✔ | ✔ |
| [Go driver](https://godoc.org/github.com/snowflakedb/gosnowflake) | ✔ | ✔ | ✔ |  |
| [JDBC Driver](../developer-guide/jdbc/jdbc) | ✔ | ✔ | ✔ | ✔ |
| [ODBC Driver](../developer-guide/odbc/odbc) | ✔ | ✔ | ✔ | ✔ |
| [Node.js Driver](../developer-guide/node-js/nodejs-driver) | ✔ | ✔ | ✔ | ✔ |
| [.NET Driver](../developer-guide/dotnet/dotnet-driver) | ✔ | ✔ | ✔ | ✔ |
| [PHP PDO Driver for Snowflake](../developer-guide/php-pdo/php-pdo-driver) | ✔ | ✔ | ✔ | ✔ |

## Configuring key-pair authentication[¶](#configuring-key-pair-authentication "Link to this heading")

Complete the following steps to configure key pair authentication for all supported Snowflake clients.

### Generate the private keys[¶](#generate-the-private-keys "Link to this heading")

Depending on which one of the [Supported Snowflake Clients](#supported-snowflake-clients) you use to connect to Snowflake, you have the option to generate encrypted or
unencrypted private keys. Generally, it is safer to generate encrypted keys. Snowflake recommends communicating with your internal security
and governance officers to determine which key type to generate prior to completing this step.

Snowflake supports cryptographic keys generated using the following algorithms:

* RSA digital signature algorithms RS256, RS384, and RS512.
* Elliptic Curve Digital Signature Algorithms (ECDSA) algorithms ES256(P-256), ES384 (P-384), and ES512 (P-512).

These signatures use the SHA-256, SHA-384, and SHA-512 hash algorithms, respectively.

Tip

The command to generate an encrypted key prompts for a passphrase to regulate access to the key. Snowflake recommends using a passphrase
that complies with PCI DSS standards to protect the locally generated private key. Additionally, Snowflake recommends storing the
passphrase in a secure location. If you are using an encrypted key to connect to Snowflake, enter the passphrase during the initial
connection. The passphrase is only used for protecting the private key and will never be sent to Snowflake.

To generate a long and complex passphrase based on PCI DSS standards:

> 1. Access the [PCI Security Standards Document Library](https://www.pcisecuritystandards.org/document_library).
> 2. For PCI DSS, select the most recent version and your desired language.
> 3. Complete the form to access the document.
> 4. Search for `Passwords/passphrases must meet the following:` and follow the recommendations for password/passphrase
>    requirements, testing, and guidance. Depending on the document version, the phrase is likely located in a section called
>    `Requirement 8: Identify and authenticate access to system components` or a similar name.

To start, open a terminal window and generate a private key.

You can generate either an encrypted version of the private key or an unencrypted version of the private key.

To generate an unencrypted version, use the following command:

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
```

Copy

To generate an encrypted version, use the following command, which omits `-nocrypt`:

```
openssl genrsa 2048 | openssl pkcs8 -topk8 -v2 des3 -inform PEM -out rsa_key.p8
```

Copy

The commands generate a private key in PEM format.

```
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIE6T...
-----END ENCRYPTED PRIVATE KEY-----
```

Copy

### Generate a public key[¶](#generate-a-public-key "Link to this heading")

From the command line, generate the public key by referencing the private key. The following command assumes the private key is encrypted
and contained in the file named `rsa_key.p8`.

```
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
```

Copy

The command generates the public key in PEM format.

```
-----BEGIN PUBLIC KEY-----
MIIBIj...
-----END PUBLIC KEY-----
```

Copy

### Store the private and public keys securely[¶](#store-the-private-and-public-keys-securely "Link to this heading")

Copy the public and private key files to a local directory for storage. Record the path to the files. Note that the private key is stored
using the PKCS#8 (Public Key Cryptography Standards) format and is encrypted using the passphrase you specified in the previous step.

However, the file should still be protected from unauthorized access using the file permission mechanism provided by your operating system.
It is your responsibility to secure the file when it is not being used.

### Grant the privilege to assign a public key to a Snowflake user[¶](#grant-the-privilege-to-assign-a-public-key-to-a-snowflake-user "Link to this heading")

To assign a public key to a user, you must have one of the following
[roles or privileges](security-access-control-overview):

* MODIFY PROGRAMMATIC AUTHENTICATION METHODS privilege on the user.
* OWNERSHIP privilege on the user.

You can use the [GRANT <privileges> … TO ROLE](../sql-reference/sql/grant-privilege) or [GRANT OWNERSHIP](../sql-reference/sql/grant-ownership) command to grant the
MODIFY PROGRAMMATIC AUTHENTICATION METHODS or OWNERSHIP privilege on the user to a role.

For example, suppose that you want to users with the `my_service_owner_role` custom role to assign the public key to the service
user `my_service_user`. The following statement grants the MODIFY PROGRAMMATIC AUTHENTICATION METHODS privilege on the
`my_service_user` user to the role `my_service_owner_role`:

```
GRANT MODIFY PROGRAMMATIC AUTHENTICATION METHODS ON USER my_service_user
  TO ROLE my_service_owner_role;
```

Copy

### Assign the public key to a Snowflake user[¶](#assign-the-public-key-to-a-snowflake-user "Link to this heading")

To assign the public key to the user, execute an [ALTER USER](../sql-reference/sql/alter-user) command to set the RSA\_PUBLIC\_KEY property
of the user. For example:

```
ALTER USER example_user SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...';
```

Copy

Note

* Exclude the public key delimiters in the SQL statement.

### Verify the user’s public key fingerprint[¶](#verify-the-user-s-public-key-fingerprint "Link to this heading")

1. Execute the following command to retrieve the user’s public key fingerprint:

   ```
   DESC USER example_user
     ->> SELECT SUBSTR(
           (SELECT "value" FROM $1
              WHERE "property" = 'RSA_PUBLIC_KEY_FP'),
           LEN('SHA256:') + 1) AS key;
   ```

   Copy

   Output:

   ```
   Azk1Pq...
   ```
2. Copy the output.
3. Run the following command on the command line:

   ```
   openssl rsa -pubin -in rsa_key.pub -outform DER | openssl dgst -sha256 -binary | openssl enc -base64
   ```

   Copy

   Output:

   ```
   writing RSA key
   Azk1Pq...
   ```
4. Compare both outputs. If both outputs match, the user correctly configured their public key.

### Configure the Snowflake client to use key-pair authentication[¶](#configure-the-snowflake-client-to-use-key-pair-authentication "Link to this heading")

Update the client to use key pair authentication to connect to Snowflake.

* [Snowflake CLI](../developer-guide/snowflake-cli/connecting/configure-connections.html#label-snowcli-private-key)
* [SnowSQL](snowsql-start.html#label-snowsql-key-pair-authn-rotation)
* [Python connector](../developer-guide/python-connector/python-connector-connect.html#label-python-key-pair-authn-rotation)
* [Spark connector](spark-connector-use.html#label-spark-key-pair-authn-rotation)
* [Kafka connector](kafka-connector-install.html#label-kafka-key-pair-authn-rotation)
* [Go driver](https://godoc.org/github.com/snowflakedb/gosnowflake)
* [JDBC driver](../developer-guide/jdbc/jdbc-configure.html#label-jdbc-using-key-pair-authentication)
* [ODBC driver](../developer-guide/odbc/odbc-parameters.html#label-odbc-key-pair-authentication)
* [.NET driver](https://github.com/snowflakedb/snowflake-connector-net/blob/master/README.md)
* [Node.js Driver](../developer-guide/node-js/nodejs-driver-authenticate.html#label-nodejs-key-pair-authentication)

## Configuring key-pair rotation[¶](#configuring-key-pair-rotation "Link to this heading")

Snowflake supports multiple active keys to allow for uninterrupted rotation. Rotate and replace your public and private keys based on the
expiration schedule you follow internally.

Currently, you can use the `RSA_PUBLIC_KEY` and `RSA_PUBLIC_KEY_2` parameters for [ALTER USER](../sql-reference/sql/alter-user) to
associate up to 2 public keys with a single user.

Complete the following steps to configure key pair rotation and rotate your keys.

1. Complete all steps in [Configuring key-pair authentication](#label-configuring-key-pair-authentication) with the following updates:

   * Generate a new private and public key set.
   * Assign the public key to the user. Set the public key value to either `RSA_PUBLIC_KEY` or `RSA_PUBLIC_KEY_2`, whichever key
     value is not currently in use. For example:

     ```
     ALTER USER example_user SET RSA_PUBLIC_KEY_2='JERUEHtcve...';
     ```

     Copy
2. Update the code to connect to Snowflake. Specify the new private key.

   Snowflake verifies the correct active public key for authentication based on the private key submitted with your connection information.
3. Remove the old public key from the user profile using an [ALTER USER](../sql-reference/sql/alter-user) command.

   ```
   ALTER USER example_user UNSET RSA_PUBLIC_KEY;
   ```

   Copy

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

1. [Overview](#overview)
2. [Supported Snowflake clients](#supported-snowflake-clients)
3. [Configuring key-pair authentication](#configuring-key-pair-authentication)
4. [Generate the private keys](#generate-the-private-keys)
5. [Generate a public key](#generate-a-public-key)
6. [Store the private and public keys securely](#store-the-private-and-public-keys-securely)
7. [Grant the privilege to assign a public key to a Snowflake user](#grant-the-privilege-to-assign-a-public-key-to-a-snowflake-user)
8. [Assign the public key to a Snowflake user](#assign-the-public-key-to-a-snowflake-user)
9. [Verify the user’s public key fingerprint](#verify-the-user-s-public-key-fingerprint)
10. [Configure the Snowflake client to use key-pair authentication](#configure-the-snowflake-client-to-use-key-pair-authentication)
11. [Configuring key-pair rotation](#configuring-key-pair-rotation)

Related content

1. [Key Pair Authentication: Troubleshooting](/user-guide/key-pair-auth-troubleshooting)