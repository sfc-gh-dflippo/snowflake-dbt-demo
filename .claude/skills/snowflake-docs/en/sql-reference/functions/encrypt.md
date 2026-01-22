---
auto_generated: true
description: Encryption functions
last_scraped: '2026-01-14T16:57:12.586102+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/encrypt
title: ENCRYPT | Snowflake Documentation
---

1. [Overview](../../reference.md)
2. [SQL data types reference](../../sql-reference-data-types.md)
3. [SQL command reference](../../sql-reference-commands.md)
4. [Function and stored procedure reference](../../sql-reference-functions.md)

   * [Summary of functions](../intro-summary-operators-functions.md)
   * [All functions (alphabetical)](../functions-all.md)")
   * [Aggregate](../functions-aggregation.md)
   * AI Functions

     * Scalar functions

       * [AI\_CLASSIFY](ai_classify.md)
       * [AI\_COMPLETE](ai_complete.md)
       * [AI\_COUNT\_TOKENS](ai_count_tokens.md)
       * [AI\_EMBED](ai_embed.md)
       * [AI\_EXTRACT](ai_extract.md)
       * [AI\_FILTER](ai_filter.md)
       * [AI\_PARSE\_DOCUMENT](ai_parse_document.md)
       * [AI\_REDACT](ai_redact.md)
       * [AI\_SENTIMENT](ai_sentiment.md)
       * [AI\_SIMILARITY](ai_similarity.md)
       * [AI\_TRANSCRIBE](ai_transcribe.md)
       * [AI\_TRANSLATE](ai_translate.md)
       * [CLASSIFY\_TEXT (SNOWFLAKE.CORTEX)](classify_text-snowflake-cortex.md)")
       * [COMPLETE (SNOWFLAKE.CORTEX)](complete-snowflake-cortex.md)")
       * [COMPLETE multimodal (images) (SNOWFLAKE.CORTEX)](complete-snowflake-cortex-multimodal.md) (SNOWFLAKE.CORTEX)")
       * [EMBED\_TEXT\_768 (SNOWFLAKE.CORTEX)](embed_text-snowflake-cortex.md)")
       * [EMBED\_TEXT\_1024 (SNOWFLAKE.CORTEX)](embed_text_1024-snowflake-cortex.md)")
       * [ENTITY\_SENTIMENT (SNOWFLAKE.CORTEX)](entity_sentiment-snowflake-cortex.md)")
       * [EXTRACT\_ANSWER (SNOWFLAKE.CORTEX)](extract_answer-snowflake-cortex.md)")
       * [FINETUNE (SNOWFLAKE.CORTEX)](finetune-snowflake-cortex.md)")
       * [PARSE\_DOCUMENT (SNOWFLAKE.CORTEX)](parse_document-snowflake-cortex.md)")
       * [SENTIMENT (SNOWFLAKE.CORTEX)](sentiment-snowflake-cortex.md)")
       * [SUMMARIZE (SNOWFLAKE.CORTEX)](summarize-snowflake-cortex.md)")
       * [TRANSLATE (SNOWFLAKE.CORTEX)](translate-snowflake-cortex.md)")
     * Aggregate functions

       * [AI\_AGG](ai_agg.md)
       * [AI\_SUMMARIZE\_AGG](ai_summarize_agg.md)
     * Helper functions

       * [COUNT\_TOKENS (SNOWFLAKE.CORTEX)](count_tokens-snowflake-cortex.md)")
       * [SEARCH\_PREVIEW (SNOWFLAKE.CORTEX)](search_preview-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_MARKDOWN\_HEADER (SNOWFLAKE.CORTEX)](split_text_markdown_header-snowflake-cortex.md)")
       * [SPLIT\_TEXT\_RECURSIVE\_CHARACTER (SNOWFLAKE.CORTEX)](split_text_recursive_character-snowflake-cortex.md)")
       * [TRY\_COMPLETE (SNOWFLAKE.CORTEX)](try_complete-snowflake-cortex.md)")
   * [Bitwise expression](../expressions-byte-bit.md)
   * [Conditional expression](../expressions-conditional.md)
   * [Context](../functions-context.md)
   * [Conversion](../functions-conversion.md)
   * [Data generation](../functions-data-generation.md)
   * [Data metric](../functions-data-metric.md)
   * [Date & time](../functions-date-time.md)
   * [Differential privacy](../functions-differential-privacy.md)
   * [Encryption](../functions-encryption.md)

     + [ENCRYPT](encrypt.md)
     + [DECRYPT](decrypt.md)
     + [TRY\_DECRYPT](try_decrypt.md)
     + [ENCRYPT\_RAW](encrypt_raw.md)
     + [DECRYPT\_RAW](decrypt_raw.md)
     + [TRY\_DECRYPT\_RAW](try_decrypt_raw.md)
   * [File](../functions-file.md)
   * [Geospatial](../functions-geospatial.md)
   * [Hash](../functions-hash-scalar.md)
   * [Metadata](../functions-metadata.md)
   * [ML Model Monitors](../functions-model-monitors.md)
   * [Notification](../functions-notification.md)
   * [Numeric](../functions-numeric.md)
   * [Organization users and organization user groups](../functions-organization-users.md)
   * [Regular expressions](../functions-regexp.md)
   * [Semi-structured and structured data](../functions-semistructured.md)
   * [Snowpark Container Services](../functions-spcs.md)
   * [String & binary](../functions-string.md)
   * [System](../functions-system.md)
   * [Table](../functions-table.md)
   * [Vector](../functions-vector.md)
   * [Window](../functions-window.md)
   * [Stored procedures](../../sql-reference-stored-procedures.md)
5. [Class reference](../../sql-reference-classes.md)
6. [Scripting reference](../../sql-reference-snowflake-scripting.md)
7. [General reference](../../sql-reference.md)
8. [API reference](../../api-reference.md)

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Encryption](../functions-encryption.md)ENCRYPT

Categories:
:   [Encryption functions](../functions-encryption)

# ENCRYPT[¶](#encrypt "Link to this heading")

Encrypts a VARCHAR or BINARY value using a VARCHAR passphrase.

See also:
:   [ENCRYPT\_RAW](encrypt_raw) , [DECRYPT](decrypt) , [DECRYPT\_RAW](decrypt_raw) , [TRY\_DECRYPT](try_decrypt) , [TRY\_DECRYPT\_RAW](try_decrypt_raw)

## Syntax[¶](#syntax "Link to this heading")

```
ENCRYPT( <value_to_encrypt> , <passphrase> ,
         [ [ <additional_authenticated_data> , ] <encryption_method> ]
       )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

**Required:**

`value_to_encrypt`
:   The VARCHAR or BINARY value to encrypt.

`passphrase`
:   The passphrase to use to encrypt/decrypt the data. The passphrase is always a VARCHAR, regardless of whether the
    `value_to_encrypt` is VARCHAR or BINARY.

**Optional:**

`additional_authenticated_data`
:   Additional authenticated data (AAD) is additional data whose confidentiality and authenticity is assured during the
    decryption process. However, this AAD is not encrypted and is not included as a field in the returned value from the
    ENCRYPT or ENCRYPT\_RAW function.

    If AAD is passed to the encryption function (ENCRYPT or ENCRYPT\_RAW), then the same AAD must be passed to the
    decryption function (DECRYPT or DECRYPT\_RAW). If the AAD passed to the decryption function does not match the
    AAD passed to the encryption function, then decryption fails.

    The difference between the AAD and the `passphrase` is that the passphrase is intended to be kept
    secret (otherwise, the encryption is essentially worthless) while the AAD can be left public. The AAD helps
    authenticate that a public piece of information and an encrypted value are associated with each other. The
    examples section in the [ENCRYPT](#) function includes an example showing the behavior
    when the AAD matches and the behavior when it doesn’t match.

    For ENCRYPT\_RAW and DECRYPT\_RAW, the data type of the AAD should be BINARY.
    For ENCRYPT and DECRYPT, the data type of the AAD can be either VARCHAR or BINARY, and does not need to match
    the data type of the value that was encrypted.

    AAD is supported only by AEAD-enabled encryption modes like GCM (default).

`encryption_method`
:   This string specifies the method to use for encrypting/decrypting the data. This string contains subfields:

    ```
    <algorithm>-<mode> [ /pad: <padding> ]
    ```

    Copy

    The `algorithm` is currently limited to:

    > * `'AES'`: When a passphrase is passed (e.g. to ENCRYPT), the function uses AES-256 encryption (256 bits). When a key
    >   is passed (e.g. to ENCRYPT\_RAW), the function uses 128, 192, or 256-bit encryption, depending upon the key
    >   length.

    The `algorithm` is case-insensitive.

    The `mode` specifies which block cipher mode should be used to encrypt messages.
    The following table shows which modes are supported, and which of those modes support padding:

    | Mode | Padding | Description |
    | --- | --- | --- |
    | `'ECB'` | Yes | Encrypt every block individually with the key. This mode is generally discouraged and is included only for compatibility with external implementations. |
    | `'CBC'` | Yes | The encrypted block is XORed with the previous block. |
    | `'GCM'` | No | Galois/Counter Mode is a high-performance encryption mode that is AEAD-enabled. AEAD additionally assures the authenticity and confidentiality of the encrypted data by generating an AEAD tag. Moreover, AEAD supports AAD (additional authenticated data). |
    | `'CTR'` | No | Counter mode. |
    | `'OFB'` | No | Output feedback. The ciphertext is XORed with the plaintext of a block. |
    | `'CFB'` | No | Cipher feedback is a combination of OFB and CBC. |

    The `mode` is case-insensitive.

    The `padding` specifies how to pad messages whose length is not a multiple of the block size. Padding is
    applicable only for ECB and CBC modes; padding is ignored for other modes. The possible values for padding are:

    > * `'PKCS'`: Uses PKCS5 for block padding.
    > * `'NONE'`: No padding. The user needs to take care of the padding when using ECB or CBC mode.

    The `padding` is case-insensitive.

    Default setting: `'AES-GCM'`.

    If the `mode` is not specified, GCM is used.

    If the `padding` is not specified, PKCS is used.

## Returns[¶](#returns "Link to this heading")

The data type of the returned value is BINARY.

Although only a single value is returned, that value contains two or three concatenated fields:

* The first field is an initialization vector (IV). The IV is generated randomly using a CTR-DRBG random number
  generator. Both encryption and decryption use the IV.
* The second field is the ciphertext (encrypted value) of the `value_to_encrypt`.
* If the encryption mode is AEAD-enabled, then the returned value also contains a third field, which is the AEAD tag.

The IV and tag size depend on the encryption mode.

## Usage notes[¶](#usage-notes "Link to this heading")



* To decrypt data encrypted by `ENCRYPT()`, use `DECRYPT()`. Do not use `DECRYPT_RAW()`.
* To decrypt data encrypted by `ENCRYPT_RAW()`, use `DECRYPT_RAW()`. Do not use `DECRYPT()`.
* The function’s parameters are masked for security. Sensitive information such as the following is
  not visible in the query log and is not visible to Snowflake:

  + The string or binary value to encrypt or decrypt.
  + The passphrase or key.
* The functions use a FIPS-compliant cryptographic library to effectively perform the encryption and decryption.
* The passphrase or key used to decrypt a piece of data must be the same as the passphrase or key used to encrypt that
  data.

* The passphrase can be of arbitrary length, even 0 (the empty string). However, Snowflake
  strongly recommends using a passphrase that is at least 8 bytes.
* Snowflake recommends that the passphrase follow general best practices for passwords, such as using a mix of
  uppercase letters, lowercase letters, numbers, and punctuation.
* The passphrase is not used directly to encrypt/decrypt the input. Instead, the passphrase is used to derive an
  encryption/decryption key, which is always the same for the same passphrase. Snowflake uses the
  <https://en.wikipedia.org/wiki/PBKDF2> key-derivation function with a Snowflake-internal seed to compute the
  encryption/decryption key from the given passphrase.

  Because of this key derivation, the encrypt/decrypt function cannot be used to:

  + Decrypt data that was externally encrypted.
  + Encrypt data that will be externally decrypted.

  To do either of these, use [ENCRYPT\_RAW](encrypt_raw) or [DECRYPT\_RAW](decrypt_raw).
* Because the initialization vector is always regenerated randomly, calling `ENCRYPT()` with the same
  `value_to_encrypt` and `passphrase` does not return the same result every time. If you need to
  generate the same output for the same `value_to_encrypt` and `passphrase`, consider using
  [ENCRYPT\_RAW](encrypt_raw) and specifying the initialization vector.

## Examples[¶](#examples "Link to this heading")

This example encrypts a VARCHAR with a simple passphrase.

> ```
> SELECT encrypt('Secret!', 'SamplePassphrase');
> ```
>
> Copy
>
> The output is text that is not easy for humans to read.

The code below shows a simple example of encryption and decryption:

> ```
> SET passphrase='poiuqewjlkfsd';
> ```
>
> Copy
>
> ```
> SELECT
>     TO_VARCHAR(
>         DECRYPT(
>             ENCRYPT('Patient tested positive for COVID-19', $passphrase),
>             $passphrase),
>         'utf-8')
>         AS decrypted
>     ;
> +--------------------------------------+
> | DECRYPTED                            |
> |--------------------------------------|
> | Patient tested positive for COVID-19 |
> +--------------------------------------+
> ```
>
> Copy

This example uses a BINARY value for the `value_to_encrypt` and for the authenticated data.

> ```
> SELECT encrypt(to_binary(hex_encode('Secret!')), 'SamplePassphrase', to_binary(hex_encode('Authenticated Data')));
> ```
>
> Copy
>
> The output is:
>
> ```
> 6E1361E297C22969345F978A45205E3E98EB872844E3A0F151713894C273FAEF50C365S
> ```
>
> Copy

This example shows how to use an alternative mode (`CBC`) as part of the specifier for the encryption method.
This encryption method also specifies a padding rule (`PKCS`). In this example, the AAD parameter is NULL.

> ```
> SELECT encrypt(to_binary(hex_encode('secret!')), 'sample_passphrase', NULL, 'aes-cbc/pad:pkcs') as encrypted_data;
> ```
>
> Copy

This example shows how to use the AAD:

```
SELECT
    TO_VARCHAR(
        DECRYPT(
            ENCRYPT('penicillin', $passphrase, 'John Dough AAD', 'aes-gcm'),
            $passphrase, 'John Dough AAD', 'aes-gcm'),
        'utf-8')
        AS medicine
    ;
+------------+
| MEDICINE   |
|------------|
| penicillin |
+------------+
```

Copy

If you pass the wrong AAD, decryption fails:

```
SELECT
    DECRYPT(
        ENCRYPT('penicillin', $passphrase, 'John Dough AAD', 'aes-gcm'),
        $passphrase, 'wrong patient AAD', 'aes-gcm') AS medicine
    ;
```

Copy

```
100311 (22023): Decryption failed. Check encrypted data, key, AAD, or AEAD tag.
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

### Alternative interfaces

[Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview)[Snowflake REST APIs](/developer-guide/snowflake-rest-api/snowflake-rest-api)[Snowflake CLI](/developer-guide/snowflake-cli/index)

See all interfaces

On this page

1. [Syntax](#syntax)
2. [Arguments](#arguments)
3. [Returns](#returns)
4. [Usage notes](#usage-notes)
5. [Examples](#examples)