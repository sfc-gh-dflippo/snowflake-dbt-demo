---
auto_generated: true
description: String & binary functions (AI Functions)
last_scraped: '2026-01-14T16:57:55.820396+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/ai_translate
title: AI_TRANSLATE | Snowflake Documentation
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)AI FunctionsScalar functionsAI\_TRANSLATE

Categories:
:   [String & binary functions](../functions-string) (AI Functions)

# AI\_TRANSLATE[¶](#ai-translate "Link to this heading")

Note

AI\_TRANSLATE is the updated version of [TRANSLATE (SNOWFLAKE.CORTEX)](translate-snowflake-cortex).
For the latest functionality, use AI\_TRANSLATE.

Translates the given input text from one supported language to another.

## Syntax[¶](#syntax "Link to this heading")

```
AI_TRANSLATE(
    <text>, <source_language>, <target_language>)
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`text`
:   A string containing the text to be translated.

`source_language`
:   A string specifying the language code for the language the text is currently in. See [Usage notes](#usage-notes) for a list of
    supported language codes. If the source language code is an empty string, `''`, the source language is
    automatically detected.

`target_language`
:   A string specifying the language code into which the text should be translated. See [Usage notes](#usage-notes) for a list of
    supported language codes.

## Returns[¶](#returns "Link to this heading")

A string containing a translation of the original text into the target language.

## Usage notes[¶](#usage-notes "Link to this heading")

The following languages are supported by the AI\_TRANSLATE function. Use the corresponding language code for the source and
target language.

The AI\_TRANSLATE model also supports a mix of different languages in the text being translated (for example,
“Spanglish”). In this case, specify an empty string (`''`) as the source language to auto-detect the languages
used in the source text.

| Language | Code |
| --- | --- |
| Arabic | `'ar'` |
| Chinese | `'zh'` |
| Croatian | `'hr'` |
| Czech | `'cs'` |
| Dutch | `'nl'` |
| English | `'en'` |
| Finnish | `'fi'` |
| French: | `'fr'` |
| German | `'de'` |
| Greek | `'el'` |
| Hebrew | `'he'` |
| Hindi | `'hi'` |
| Italian | `'it'` |
| Japanese | `'ja'` |
| Korean | `'ko'` |
| Norwegian | `'no'` |
| Polish | `'pl'` |
| Portuguese | `'pt'` |
| Romanian | `'ro'` |
| Russian | `'ru'` |
| Spanish | `'es'` |
| Swedish | `'sv'` |
| Turkish | `'tr'` |

## Access control requirements[¶](#access-control-requirements "Link to this heading")

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](../snowflake-db-roles.html#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](../../user-guide/snowflake-cortex/aisql.html#label-cortex-llm-privileges) for more information on this privilege.

## Examples[¶](#examples "Link to this heading")

The following example translates each row of a table from English to German (in this example, `review_content` is
a column from the `reviews` table):

```
SELECT AI_TRANSLATE(review_content, 'en', 'de') FROM reviews LIMIT 10;
```

Copy

The following example translates a fictitious product review from English to Spanish:

```
SELECT AI_TRANSLATE(
  'Hit the slopes with Snowflake\'s latest innovation - "Skii Headphones" designed to keep your ears warm and your soul ablaze. Engineered specifically for snow weather, these rugged headphones combine crystal-clear sound with thermally-insulated ear cups to keep the chill out and the beats in. Whether you\'re carving through powder or cruising down groomers, Skii Headphones will fuel your mountain adventures with vibrant sound and unrelenting passion. Stay warm, stay fired up, and shred the mountain with Snowflake Skii Headphones',
'en','es');
```

Copy

The result of this query is:

```
Sube a las pistas con la última innovación de Snowflake: "Skii Headphones", diseñados para mantener tus oídos calientes y tu alma encendida. Diseñados específicamente para el clima de nieve, estos audífonos resistentes combinan un sonido cristalino con copas de oído aisladas térmicamente para mantener el frío fuera y los ritmos dentro. Ya sea que estés esculpiendo en polvo o deslizándote por pistas preparadas, los Skii Headphones alimentarán tus aventuras en la montaña con un sonido vibrante y una pasión incesante. Mantente caliente, mantente encendido y arrasa la montaña con los Skii Headphones de Snowflake.
```

The following example translates a call transcript from German to English:

```
SELECT AI_TRANSLATE(
  ('Kunde: Hallo
    Agent: Hallo, ich hoffe, es geht Ihnen gut. Um Ihnen am besten helfen zu können, teilen Sie bitte Ihren Vor- und Nachnamen und den Namen der Firma, von der aus Sie anrufen.
    Kunde: Ja, hier ist Thomas Müller von SkiPisteExpress.
    Agent: Danke Thomas, womit kann ich Ihnen heute helfen?
    Kunde: Also wir haben die XtremeX Helme in Größe M bestellt, die wir speziell für die kommende Wintersaison benötigen. Jedoch sind alle Schnallen der Helme defekt, und keiner schließt richtig.
    Agent: Ich verstehe, dass das ein Problem für Ihr Geschäft sein kann. Lassen Sie mich überprüfen, was mit Ihrer Bestellung passiert ist. Um zu bestätigen: Ihre Bestellung endet mit der Nummer 56682?
    Kunde: Ja, das ist meine Bestellung.
    Agent: Ich sehe das Problem. Entschuldigen Sie die Unannehmlichkeiten. Ich werde sofort eine neue Lieferung mit reparierten Schnallen für Sie vorbereiten, die in drei Tagen bei Ihnen eintreffen sollte. Ist das in Ordnung für Sie?
    Kunde: Drei Tage sind ziemlich lang, ich hatte gehofft, diese Helme früher zu erhalten. Gibt es irgendeine Möglichkeit, die Lieferung zu beschleunigen?
    Agent: Ich verstehe Ihre Dringlichkeit. Ich werde mein Bestes tun, um die Lieferung auf zwei Tage zu beschleunigen. Wie kommst du damit zurecht?
    Kunde: Das wäre großartig, ich wäre Ihnen sehr dankbar.
    Agent: Kein Problem, Thomas. Ich kümmere mich um die eilige Lieferung. Danke für Ihr Verständnis und Ihre Geduld.
    Kunde: Vielen Dank für Ihre Hilfe. Auf Wiedersehen!
    Agent: Bitte, gerne geschehen. Auf Wiedersehen und einen schönen Tag noch!'
,'de','en');
```

Copy

The result is:

```
Customer: Hello
Agent: Hello, I hope you are well. To best assist you, please share your first and last name and the name of the company you are calling from.
Customer: Yes, this is Thomas Müller from SkiPisteExpress.
Agent: Thank you, Thomas, what can I help you with today?
Customer: So, we ordered the XtremeX helmets in size M, which we specifically need for the upcoming winter season. However, all the buckles on the helmets are defective and none of them close properly.
Agent: I understand that this can be a problem for your business. Let me check what happened with your order. To confirm: your order ends with the number 56682?
Customer: Yes, that's my order.
Agent: I see the issue. I apologize for the inconvenience. I will prepare a new delivery with repaired buckles for you immediately, which should arrive in three days. Is that okay for you?
Customer: Three days is quite a long time; I was hoping to receive these helmets sooner. Is there any way to expedite the delivery?
Agent: I understand your urgency. I will do my best to expedite the delivery to two days. How does that sound?
Customer: That would be great, I would be very grateful.
Agent: No problem, Thomas. I will take care of the urgent delivery. Thank you for your understanding and patience.
Customer: Thank you very much for your help. Goodbye!
Agent: You're welcome. Goodbye and have a nice day!
```

Finally, the following example illustrates translating text from two different languages (in this case English and Spanish, or “Spanglish”) to English.
Note that the specification of the source language is the empty string, which tells AI\_TRANSLATE to automatically detect the language.

```
SELECT AI_TRANSLATE('Voy a likear tus fotos en Insta.', '', 'en')
```

Copy

This query results in:

```
I'm going to like your photos on Insta.
```

## Legal notices[¶](#legal-notices "Link to this heading")

Refer to [Snowflake AI and ML](../../guides-overview-ai-features).

## Limitations[¶](#limitations "Link to this heading")

Snowflake Cortex functions do not support dynamic tables.

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
5. [Access control requirements](#access-control-requirements)
6. [Examples](#examples)
7. [Legal notices](#legal-notices)
8. [Limitations](#limitations)

Related content

1. [Snowflake Cortex AI Functions (including LLM functions)](/sql-reference/functions/../../user-guide/snowflake-cortex/aisql)