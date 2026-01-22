---
auto_generated: true
description: Geospatial functions
last_scraped: '2026-01-14T16:56:08.775821+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/functions/st_aswkt
title: ST_ASWKT , ST_ASTEXT | Snowflake Documentation
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

     + Conversion, input, parsing
     + [ST\_GEOGFROMGEOHASH](st_geogfromgeohash.md)
     + [ST\_GEOGPOINTFROMGEOHASH](st_geogpointfromgeohash.md)
     + [ST\_GEOGRAPHYFROMWKB](st_geographyfromwkb.md)
     + [ST\_GEOGRAPHYFROMWKT](st_geographyfromwkt.md)
     + [ST\_GEOMETRYFROMWKB](st_geometryfromwkb.md)
     + [ST\_GEOMETRYFROMWKT](st_geometryfromwkt.md)
     + [ST\_GEOMFROMGEOHASH](st_geomfromgeohash.md)
     + [ST\_GEOMPOINTFROMGEOHASH](st_geompointfromgeohash.md)
     + [TO\_GEOGRAPHY](to_geography.md)
     + [TO\_GEOMETRY](to_geometry.md)
     + [TRY\_TO\_GEOGRAPHY](try_to_geography.md)
     + [TRY\_TO\_GEOMETRY](try_to_geometry.md)
     + Conversion, output, formatting
     + [ST\_ASGEOJSON](st_asgeojson.md)
     + [ST\_ASWKB](st_aswkb.md)
     + [ST\_ASBINARY](st_aswkb.md)
     + [ST\_ASEWKB](st_asewkb.md)
     + [ST\_ASWKT](st_aswkt.md)
     + [ST\_ASTEXT](st_aswkt.md)
     + [ST\_ASEWKT](st_asewkt.md)
     + [ST\_GEOHASH](st_geohash.md)
     + Constructor
     + [ST\_MAKELINE](st_makeline.md)
     + [ST\_MAKEGEOMPOINT](st_makegeompoint.md)
     + [ST\_GEOMPOINT](st_makegeompoint.md)
     + [ST\_MAKEPOINT](st_makepoint.md)
     + [ST\_POINT](st_makepoint.md)
     + [ST\_MAKEPOLYGON](st_makepolygon.md)
     + [ST\_POLYGON](st_makepolygon.md)
     + [ST\_MAKEPOLYGONORIENTED](st_makepolygonoriented.md)
     + Accessor
     + [ST\_DIMENSION](st_dimension.md)
     + [ST\_ENDPOINT](st_endpoint.md)
     + [ST\_POINTN](st_pointn.md)
     + [ST\_SRID](st_srid.md)
     + [ST\_STARTPOINT](st_startpoint.md)
     + [ST\_X](st_x.md)
     + [ST\_XMAX](st_xmax.md)
     + [ST\_XMIN](st_xmin.md)
     + [ST\_Y](st_y.md)
     + [ST\_YMAX](st_ymax.md)
     + [ST\_YMIN](st_ymin.md)
     + Relationship and measurement
     + [HAVERSINE](haversine.md)
     + [ST\_AREA](st_area.md)
     + [ST\_AZIMUTH](st_azimuth.md)
     + [ST\_CONTAINS](st_contains.md)
     + [ST\_COVEREDBY](st_coveredby.md)
     + [ST\_COVERS](st_covers.md)
     + [ST\_DISJOINT](st_disjoint.md)
     + [ST\_DISTANCE](st_distance.md)
     + [ST\_DWITHIN](st_dwithin.md)
     + [ST\_HAUSDORFFDISTANCE](st_hausdorffdistance.md)
     + [ST\_INTERSECTS](st_intersects.md)
     + [ST\_LENGTH](st_length.md)
     + [ST\_NPOINTS](st_npoints.md)
     + [ST\_NUMPOINTS](st_npoints.md)
     + [ST\_PERIMETER](st_perimeter.md)
     + [ST\_WITHIN](st_within.md)
     + Transformation
     + [ST\_BUFFER](st_buffer.md)
     + [ST\_CENTROID](st_centroid.md)
     + [ST\_COLLECT](st_collect.md)
     + [ST\_DIFFERENCE](st_difference.md)
     + [ST\_ENVELOPE](st_envelope.md)
     + [ST\_INTERPOLATE](st_interpolate.md)
     + [ST\_INTERSECTION](st_intersection.md)
     + [ST\_INTERSECTION\_AGG](st_intersection_agg.md)
     + [ST\_SETSRID](st_setsrid.md)
     + [ST\_SIMPLIFY](st_simplify.md)
     + [ST\_SYMDIFFERENCE](st_symdifference.md)
     + [ST\_TRANSFORM](st_transform.md)
     + [ST\_UNION](st_union.md)
     + [ST\_UNION\_AGG](st_union_agg.md)
     + Utility
     + [ST\_ISVALID](st_isvalid.md)
     + H3
     + [H3\_CELL\_TO\_BOUNDARY](h3_cell_to_boundary.md)
     + [H3\_CELL\_TO\_CHILDREN](h3_cell_to_children.md)
     + [H3\_CELL\_TO\_CHILDREN\_STRING](h3_cell_to_children_string.md)
     + [H3\_CELL\_TO\_PARENT](h3_cell_to_parent.md)
     + [H3\_CELL\_TO\_POINT](h3_cell_to_point.md)
     + [H3\_COMPACT\_CELLS](h3_compact_cells.md)
     + [H3\_COMPACT\_CELLS\_STRINGS](h3_compact_cells_strings.md)
     + [H3\_COVERAGE](h3_coverage.md)
     + [H3\_COVERAGE\_STRINGS](h3_coverage_strings.md)
     + [H3\_GET\_RESOLUTION](h3_get_resolution.md)
     + [H3\_GRID\_DISK](h3_grid_disk.md)
     + [H3\_GRID\_DISTANCE](h3_grid_distance.md)
     + [H3\_GRID\_PATH](h3_grid_path.md)
     + [H3\_INT\_TO\_STRING](h3_int_to_string.md)
     + [H3\_IS\_PENTAGON](h3_is_pentagon.md)
     + [H3\_IS\_VALID\_CELL](h3_is_valid_cell.md)
     + [H3\_LATLNG\_TO\_CELL](h3_latlng_to_cell.md)
     + [H3\_LATLNG\_TO\_CELL\_STRING](h3_latlng_to_cell_string.md)
     + [H3\_POINT\_TO\_CELL](h3_point_to_cell.md)
     + [H3\_POINT\_TO\_CELL\_STRING](h3_point_to_cell_string.md)
     + [H3\_POLYGON\_TO\_CELLS](h3_polygon_to_cells.md)
     + [H3\_POLYGON\_TO\_CELLS\_STRINGS](h3_polygon_to_cells_strings.md)
     + [H3\_STRING\_TO\_INT](h3_string_to_int.md)
     + [H3\_TRY\_COVERAGE](h3_try_coverage.md)
     + [H3\_TRY\_COVERAGE\_STRINGS](h3_try_coverage_strings.md)
     + [H3\_TRY\_GRID\_DISTANCE](h3_try_grid_distance.md)
     + [H3\_TRY\_GRID\_PATH](h3_try_grid_path.md)
     + [H3\_TRY\_POLYGON\_TO\_CELLS](h3_try_polygon_to_cells.md)
     + [H3\_TRY\_POLYGON\_TO\_CELLS\_STRINGS](h3_try_polygon_to_cells_strings.md)
     + [H3\_UNCOMPACT\_CELLS](h3_uncompact_cells.md)
     + [H3\_UNCOMPACT\_CELLS\_STRINGS](h3_uncompact_cells_strings.md)
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

[Reference](../../reference.md)[Function and stored procedure reference](../../sql-reference-functions.md)[Geospatial](../functions-geospatial.md)ST\_ASTEXT

Categories:
:   [Geospatial functions](../functions-geospatial)

# ST\_ASWKT , ST\_ASTEXT[¶](#st-aswkt-st-astext "Link to this heading")

Given a value of type [GEOGRAPHY](../data-types-geospatial.html#label-data-types-geography) or [GEOMETRY](../data-types-geospatial.html#label-data-types-geometry), return the
text (VARCHAR) representation of that value in
[WKT (well-known text)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) format.

See also:
:   [ST\_ASEWKT](st_asewkt)

## Syntax[¶](#syntax "Link to this heading")

Use one of the following:

```
ST_ASWKT( <geography_or_geometry_expression> )

ST_ASTEXT( <geography_or_geometry_expression> )
```

Copy

## Arguments[¶](#arguments "Link to this heading")

`geography_or_geometry_expression`
:   The argument must be an expression of type GEOGRAPHY or GEOMETRY.

## Returns[¶](#returns "Link to this heading")

A VARCHAR.

## Usage notes[¶](#usage-notes "Link to this heading")

* ST\_ASTEXT is an alias for ST\_ASWKT.
* To return the output in EWKT format, use [ST\_ASEWKT](st_asewkt) instead.

## Examples[¶](#examples "Link to this heading")

### GEOGRAPHY examples[¶](#geography-examples "Link to this heading")

The following example demonstrates the ST\_ASWKT function:

> ```
> create table geospatial_table (id INTEGER, g GEOGRAPHY);
> insert into geospatial_table values
>     (1, 'POINT(-122.35 37.55)'), (2, 'LINESTRING(-124.20 42.00, -120.01 41.99)');
> ```
>
> Copy
>
> ```
> select st_astext(g)
>     from geospatial_table
>     order by id;
> +-------------------------------------+
> | ST_ASTEXT(G)                        |
> |-------------------------------------|
> | POINT(-122.35 37.55)                |
> | LINESTRING(-124.2 42,-120.01 41.99) |
> +-------------------------------------+
> ```
>
> Copy
>
> ```
> select st_aswkt(g)
>     from geospatial_table
>     order by id;
> +-------------------------------------+
> | ST_ASWKT(G)                         |
> |-------------------------------------|
> | POINT(-122.35 37.55)                |
> | LINESTRING(-124.2 42,-120.01 41.99) |
> +-------------------------------------+
> ```
>
> Copy

### GEOMETRY examples[¶](#geometry-examples "Link to this heading")

The example below demonstrates how to use the ST\_ASEWKT function. The example returns the EWKT representations of two geometries.

> ```
> CREATE OR REPLACE TABLE geometry_table (g GEOMETRY);
> INSERT INTO geometry_table VALUES
>   ('POINT(-122.35 37.55)'), ('LINESTRING(0.75 0.75, -10 20)');
>
> ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='WKT';
> SELECT ST_ASWKT(g) FROM geometry_table;
> ```
>
> Copy
>
> ```
> +------------------------------+
> | ST_ASWKT(G)                  |
> |------------------------------|
> | POINT(-122.35 37.55)         |
> | LINESTRING(0.75 0.75,-10 20) |
> +------------------------------+
> ```
>
> Copy

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

Related content

1. [Geospatial data types](/sql-reference/functions/../data-types-geospatial)