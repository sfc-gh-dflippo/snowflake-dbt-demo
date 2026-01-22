---
auto_generated: true
description: Snowflake offers native support for geospatial features such as points,
  lines, and polygons on the Earth’s surface.
last_scraped: '2026-01-14T16:56:23.256542+00:00'
scraper_version: 1.1.0
source_url: https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html
title: Geospatial data types | Snowflake Documentation
---

1. [Overview](../reference.md)
2. [SQL data types reference](../sql-reference-data-types.md)

   * [Summary](intro-summary-data-types.md)
   * [Numeric](data-types-numeric.md)
   * [String & binary](data-types-text.md)
   * [Logical](data-types-logical.md)
   * [Date & time](data-types-datetime.md)
   * [Semi-structured](data-types-semistructured.md)
   * [Structured](data-types-structured.md)
   * [Unstructured](data-types-unstructured.md)
   * [Geospatial](data-types-geospatial.md)
   * [Vector](data-types-vector.md)
   * [Unsupported](data-types-unsupported.md)
   * [Conversion](data-type-conversion.md)
3. [SQL command reference](../sql-reference-commands.md)
4. [Function and stored procedure reference](../sql-reference-functions.md)
5. [Class reference](../sql-reference-classes.md)
6. [Scripting reference](../sql-reference-snowflake-scripting.md)
7. [General reference](../sql-reference.md)
8. [API reference](../api-reference.md)

[Reference](../reference.md)[SQL data types reference](../sql-reference-data-types.md)Geospatial

# Geospatial data types[¶](#geospatial-data-types "Link to this heading")

Snowflake offers native support for geospatial features such as points, lines, and polygons on the Earth’s surface.

Tip

You can use the search optimization service to improve query performance.
For details, see [Search optimization service](../user-guide/search-optimization-service).

## Data types[¶](#data-types "Link to this heading")

Snowflake provides the following data types for geospatial data:

* The [GEOGRAPHY](#label-data-types-geography) data type, which models Earth as though it were a perfect sphere.
* The [GEOMETRY](#label-data-types-geometry) data type, which represents features in a planar (Euclidean, Cartesian)
  coordinate system.

### GEOGRAPHY data type[¶](#geography-data-type "Link to this heading")

The GEOGRAPHY data type follows the WGS 84 standard (spatial reference ID 4326; for details, see
<https://epsg.io/4326>).

Points on the earth are represented as degrees of longitude (from -180 degrees to +180 degrees) and latitude
(-90 to +90). Snowflake uses 14 decimal places to store GEOGRAPHY coordinates. When the data includes decimal
places exceeding this limit, the coordinates are rounded to ensure compliance with the specified length constraint.

Altitude currently isn’t supported.

Line segments are interpreted as great circle arcs on the Earth’s surface.

Snowflake also provides
[geospatial functions](functions-geospatial) that
operate on the GEOGRAPHY data type.

If you have geospatial data (for example, longitude and latitude data, WKT, WKB, GeoJSON, and so on), we suggest converting and
storing this data in GEOGRAPHY columns, rather than keeping the data in their original formats in VARCHAR, VARIANT or NUMBER columns.
Storing your data in GEOGRAPHY columns can significantly improve the performance of queries that use geospatial functionality.

### GEOMETRY data type[¶](#geometry-data-type "Link to this heading")

The GEOMETRY data type represents features in a planar (Euclidean, Cartesian) coordinate system.

The coordinates are represented as pairs of real numbers (x, y). Currently, only 2D coordinates are supported.

The units of the X and Y are determined by the [spatial reference system (SRS)](https://en.wikipedia.org/wiki/Spatial_reference_system) associated with the GEOMETRY object.
The spatial reference system is identified by the [spatial reference system identifier (SRID)](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) number. Unless
the SRID is provided when creating the GEOMETRY object or by calling [ST\_SETSRID](functions/st_setsrid), the SRID is 0.

Snowflake uses 14 decimal places to store GEOMETRY coordinates. When the data includes decimal
places exceeding this limit, the coordinates are rounded to ensure compliance with the specified length constraint.

Snowflake provides a set of
[geospatial functions that operate on the GEOMETRY data type](functions-geospatial). For these functions:

* All functions assume planar coordinates, even if the geometry uses a non-planar SRS.
* The measurement functions (for example, [ST\_LENGTH](functions/st_length)) use the same units as the coordinate system.
* For functions that accept multiple GEOMETRY expressions as arguments (for example, [ST\_DISTANCE](functions/st_distance)),
  the input expressions must be defined in the same SRS.

## Geospatial input and output[¶](#geospatial-input-and-output "Link to this heading")

The following sections cover the supported standard formats and object types when reading and writing geospatial data.

* [Supported standard input and output formats](#label-data-types-geospatial-io-formats)
* [Supported geospatial object types](#label-data-types-geospatial-object-types)
* [Specifying the output format for result sets](#label-data-types-geospatial-output-format)
* [Examples of inserting and querying GEOGRAPHY data](#label-data-types-geospatial-io-examples)

### Supported standard input and output formats[¶](#supported-standard-input-and-output-formats "Link to this heading")

The GEOGRAPHY and GEOMETRY data types support the following standard industry formats for input and output:

* [Well-Known Text](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
  (WKT)
* [Well-Known Binary](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary)
  (WKB)
* [Extended WKT and WKB (EWKT and EWKB)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Format_variations)
  (see the [note on EWKT and EWKB handling](#label-a-note-on-ewkt-ewkb-handling))
* [IETF GeoJSON](https://tools.ietf.org/html/rfc7946)
  (see the [note on GeoJSON handling](#label-a-note-on-geojson-handling))

You might also find the following Open Geospatial Consortium’s Simple Feature Access references helpful:

* [Common Architecture](https://www.opengeospatial.org/standards/sfa)
* [SQL Option](https://www.opengeospatial.org/standards/sfs)

Any departure from these standards is noted explicitly in the Snowflake documentation.

#### GeoJSON handling for GEOGRAPHY values[¶](#geojson-handling-for-geography-values "Link to this heading")

The WKT and WKB standards specify a format only. The semantics of WKT/WKB objects depend on the reference system (for
example, a plane or a sphere).

The GeoJSON standard, on the other hand, specifies both a format and its semantics: GeoJSON points are explicitly
WGS 84 coordinates, and GeoJSON line segments are planar edges (straight lines).

Contrary to that, the Snowflake GEOGRAPHY data type interprets all line segments, including those input from or
output to GeoJSON format, as great circle arcs. In essence, Snowflake treats GeoJSON as JSON-formatted WKT with spherical
semantics.

#### EWKT and EWKB handling for GEOGRAPHY values[¶](#ewkt-and-ewkb-handling-for-geography-values "Link to this heading")

EWKT and EWKB are non-standard formats [introduced by PostGIS](https://postgis.net/docs/ST_GeomFromEWKT.html).
They enhance the WKT and WKB formats by including a [spatial reference system identifier (SRID)](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier), which specifies the
coordinate reference system to use with the data. Snowflake currently supports only WGS84, which maps to SRID=4326.

By default, Snowflake issues an error if an EWKB or EWKT input value contains an SRID other than 4326. Conversely, all EWKB and EWKT output values have SRID=4326.

### Supported geospatial object types[¶](#supported-geospatial-object-types "Link to this heading")

The GEOGRAPHY and GEOMETRY data types can store the following types of geospatial objects:

* WKT / WKB / EWKT / EWKB / GeoJSON geospatial objects:

  + Point
  + MultiPoint
  + LineString
  + MultiLineString
  + Polygon
  + MultiPolygon
  + GeometryCollection
* These GeoJSON-specific geospatial objects:

  + Feature
  + FeatureCollection

### Specifying the output format for result sets[¶](#specifying-the-output-format-for-result-sets "Link to this heading")

The session parameters [GEOGRAPHY\_OUTPUT\_FORMAT](parameters.html#label-geography-output-format) and
[GEOMETRY\_OUTPUT\_FORMAT](parameters.html#label-geometry-output-format) control the rendering of GEOGRAPHY and GEOMETRY columns in
result sets (respectively).

These parameters can have one of the following values:

| Parameter value | Description |
| --- | --- |
| `GeoJSON` (default) | The GEOGRAPHY / GEOMETRY result is rendered as an OBJECT in GeoJSON format. |
| `WKT` | The GEOGRAPHY / GEOMETRY result is rendered as a VARCHAR in WKT format. |
| `WKB` | The GEOGRAPHY / GEOMETRY result is rendered as a BINARY in WKB format. |
| `EWKT` | The GEOGRAPHY / GEOMETRY result is rendered as a VARCHAR in EWKT format. |
| `EWKB` | The GEOGRAPHY / GEOMETRY result is rendered as a BINARY in EWKB format. |

For `EWKT` and `EWKB`, the SRID is always 4326 in the output. See [EWKT and EWKB handling for GEOGRAPHY values](#label-a-note-on-ewkt-ewkb-handling).

This parameter affects all clients, including the Snowflake UI and the SnowSQL command-line client, as well as the
JDBC, ODBC, Node.js, Python, and so on drivers and connectors.

For example, the JDBC Driver returns the following metadata for a GEOGRAPHY-typed result column (column `i` in this
example):

* If `GEOGRAPHY_OUTPUT_FORMAT='GeoJSON'` or `GEOMETRY_OUTPUT_FORMAT='GeoJSON'`:

  + `ResultSetMetaData.getColumnType(i)` returns `java.sql.Types.VARCHAR`.
  + `ResultSetMetaData.getColumnClassName(i)` returns `"java.lang.String"`.
* If `GEOGRAPHY_OUTPUT_FORMAT='WKT'` or `'EWKT'`, or if: `GEOMETRY_OUTPUT_FORMAT='WKT'` or `'EWKT'`:

  + `ResultSetMetaData.getColumnType(i)` returns `java.sql.Types.VARCHAR`.
  + `ResultSetMetaData.getColumnClassName(i)` returns `"java.lang.String"`.
* If `GEOGRAPHY_OUTPUT_FORMAT='WKB'` or `'EWKB'`, or if `GEOMETRY_OUTPUT_FORMAT='WKB'` or `'EWKB'`:

  + `ResultSetMetaData.getColumnType(i)` returns `java.sql.Types.BINARY`.
  + `ResultSetMetaData.getColumnClassName(i)` returns `"[B"` (array of byte).

Note

APIs for retrieving database-specific type names (`getColumnTypeName` in JDBC and the
`SQL_DESC_TYPE_NAME` descriptor in ODBC) always return `GEOGRAPHY` and `GEOMETRY` for the type name,
regardless of the values of the `GEOGRAPHY_OUTPUT_FORMAT` and `GEOMETRY_OUTPUT_FORMAT` parameters. For details, see:

* [Snowflake-specific behavior](../developer-guide/jdbc/jdbc-api.html#label-jdbc-resultset-meta-data-snowflake-specific-behavior) in the JDBC Driver documentation.
* [Retrieving results and information about results](../developer-guide/odbc/odbc-api.html#label-odbc-api-result-functions) in the ODBC Driver documentation.

### Examples of inserting and querying GEOGRAPHY data[¶](#examples-of-inserting-and-querying-geography-data "Link to this heading")

The code below shows sample input and output for the GEOGRAPHY data type. Note the following:

* For the coordinates in WKT, EWKT, and GeoJSON, longitude appears before latitude (for example, `POINT(lon lat)`).

* For the WKB and EWKB output, it is assumed that the [BINARY\_OUTPUT\_FORMAT](parameters.html#label-binary-output-format) parameter
  is set to `HEX` (the default value for the parameter).

The following example creates a table with a GEOGRAPHY column, inserts data in WKT format, and returns
the data in different output formats.

```
CREATE OR REPLACE TABLE geospatial_table (id INTEGER, g GEOGRAPHY);
INSERT INTO geospatial_table VALUES
  (1, 'POINT(-122.35 37.55)'),
  (2, 'LINESTRING(-124.20 42.00, -120.01 41.99)');
```

Copy

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='GeoJSON';
```

Copy

```
SELECt g
  FROM geospatial_table
  ORDER BY id;
```

Copy

```
+------------------------+
| G                      |
|------------------------|
| {                      |
|   "coordinates": [     |
|     -122.35,           |
|     37.55              |
|   ],                   |
|   "type": "Point"      |
| }                      |
| {                      |
|   "coordinates": [     |
|     [                  |
|       -124.2,          |
|       42               |
|     ],                 |
|     [                  |
|       -120.01,         |
|       41.99            |
|     ]                  |
|   ],                   |
|   "type": "LineString" |
| }                      |
+------------------------+
```

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='WKT';
```

Copy

```
SELECt g
  FROM geospatial_table
  ORDER BY id;
```

Copy

```
+-------------------------------------+
| G                                   |
|-------------------------------------|
| POINT(-122.35 37.55)                |
| LINESTRING(-124.2 42,-120.01 41.99) |
+-------------------------------------+
```

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='WKB';
```

Copy

```
SELECt g
  FROM geospatial_table
  ORDER BY id;
```

Copy

```
+------------------------------------------------------------------------------------+
| G                                                                                  |
|------------------------------------------------------------------------------------|
| 01010000006666666666965EC06666666666C64240                                         |
| 010200000002000000CDCCCCCCCC0C5FC00000000000004540713D0AD7A3005EC01F85EB51B8FE4440 |
+------------------------------------------------------------------------------------+
```

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='EWKT';
```

Copy

```
SELECt g
  FROM geospatial_table
  ORDER BY id;
```

Copy

```
+-----------------------------------------------+
| G                                             |
|-----------------------------------------------|
| SRID=4326;POINT(-122.35 37.55)                |
| SRID=4326;LINESTRING(-124.2 42,-120.01 41.99) |
+-----------------------------------------------+
```

```
ALTER SESSION SET GEOGRAPHY_OUTPUT_FORMAT='EWKB';
```

Copy

```
SELECt g
  FROM geospatial_table
  ORDER BY id;
```

Copy

```
+--------------------------------------------------------------------------------------------+
| G                                                                                          |
|--------------------------------------------------------------------------------------------|
| 0101000020E61000006666666666965EC06666666666C64240                                         |
| 0102000020E610000002000000CDCCCCCCCC0C5FC00000000000004540713D0AD7A3005EC01F85EB51B8FE4440 |
+--------------------------------------------------------------------------------------------+
```

## Using geospatial data in Snowflake[¶](#using-geospatial-data-in-snowflake "Link to this heading")

The following sections cover the supported standard formats and object types when reading and writing geospatial data.

* [Understanding the effects of using different SRIDs with GEOMETRY](#label-geometry-store-srid)
* [Changing the spatial reference system (SRS) and SRID of a GEOMETRY object](#label-geometry-change-srs)
* [Performing DML operations on GEOGRAPHY and GEOMETRY columns](#label-data-types-geospatial-dml-operations)
* [Loading geospatial data from stages](#label-data-types-geospatial-stages)
* [Using geospatial data with Java UDFs](#label-data-types-geospatial-udf-java)
* [Using geospatial data with JavaScript UDFs](#label-data-types-geospatial-udf-javascript)
* [Using geospatial data with Python UDFs](#label-data-types-geospatial-udf-python)
* [Using GEOGRAPHY objects with H3](#label-data-types-geospatial-h3)

### Understanding the effects of using different SRIDs with GEOMETRY[¶](#understanding-the-effects-of-using-different-srids-with-geometry "Link to this heading")

In a GEOMETRY column, you can insert objects that have different [SRIDs](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier). If the column contains more than one SRID, some of the
important performance optimizations aren’t applied. This can result in slower queries, in particular when joining on a geospatial
predicate.

### Changing the spatial reference system (SRS) and SRID of a GEOMETRY object[¶](#changing-the-spatial-reference-system-srs-and-srid-of-a-geometry-object "Link to this heading")

To change the [SRS](https://en.wikipedia.org/wiki/Spatial_reference_system) and [SRID](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) of an existing GEOMETRY object, call the [ST\_TRANSFORM](functions/st_transform) function,
passing in the new SRID. The function returns a new GEOMETRY object with the new SRID and the coordinates converted to use the
SRS. For example, to return a GEOMETRY object for `geometry_expression` that uses the SRS for SRID 32633, execute the following
statement:

```
SELECT ST_TRANSFORM(geometry_expression, 32633);
```

Copy

If the original SRID isn’t set correctly in the existing GEOMETRY object, specify the original SRID as an additional argument.
For example, if `geometry_expression` is a GEOMETRY object that uses the SRID 4326, and you want to transform this to use the
SRID 28992, execute the following statement:

```
SELECT ST_TRANSFORM(geometry_expression, 4326, 28992);
```

Copy

If a GEOMETRY object uses the correct coordinates for a SRS but has the wrong SRID, you can fix the SRID by calling the
[ST\_SETSRID](functions/st_setsrid) function. For example, the following statement sets the SRID for
`geometry_expression` to 4326, while leaving the coordinates unchanged:

```
SELECT ST_SETSRID(geometry_expression, 4326);
```

Copy

### Performing DML operations on GEOGRAPHY and GEOMETRY columns[¶](#performing-dml-operations-on-geography-and-geometry-columns "Link to this heading")

When a GEOGRAPHY or GEOMETRY column is the target of a DML operation (INSERT, COPY, UPDATE, MERGE, or CREATE TABLE AS…), the
column’s source expression can be any of the following types:

* GEOGRAPHY or GEOMETRY : An expression of type GEOGRAPHY or GEOMETRY is usually the result of a parsing function, a constructor
  function, or an existing GEOGRAPHY or GEOMETRY column. For a complete list of supported functions and categories of functions,
  see [Geospatial functions](functions-geospatial).
* VARCHAR: Interpreted as a WKT, WKB (in hex format), EWKT, EWKB (in hex format), or GeoJSON formatted string (see
  [TO\_GEOGRAPHY(VARCHAR)](functions/to_geography)).
* BINARY: Interpreted as a WKB binary (see [TO\_GEOGRAPHY(BINARY)](functions/to_geography) and
* [TO\_GEOMETRY(BINARY)](functions/to_geometry)).
* VARIANT: Interpreted as a GeoJSON object (see [TO\_GEOGRAPHY(VARIANT)](functions/to_geography) and
  [TO\_GEOMETRY(VARIANT)](functions/to_geometry)).

### Loading geospatial data from stages[¶](#loading-geospatial-data-from-stages "Link to this heading")

You can load data from CSV or JSON/AVRO files in a stage directly (that is, without copy transforms) into a
GEOGRAPHY column.

* CSV: String values from the corresponding CSV column are parsed as GeoJSON, WKT, EWKT, WKB, or EWKB (see
  [TO\_GEOGRAPHY(VARCHAR)](functions/to_geography)).
* JSON/AVRO: The JSON values in the file are interpreted as GeoJSON (see
  [TO\_GEOGRAPHY(VARIANT)](functions/to_geography)).

  See also [GeoJSON handling for GEOGRAPHY values](#label-a-note-on-geojson-handling).

Loading data from other file formats (Parquet, ORC, and so on) is
possible through a [COPY](sql/copy-into-table) transform.

### Using geospatial data with Java UDFs[¶](#using-geospatial-data-with-java-udfs "Link to this heading")

Java UDFs allow the GEOGRAPHY type as an argument and as a return value. See [SQL-Java Data Type Mappings](../developer-guide/udf-stored-procedure-data-type-mapping.html#label-sql-java-data-type-mappings) and
[Passing a GEOGRAPHY value to an in-line Java UDF](../developer-guide/udf/java/udf-java-cookbook.html#label-udf-java-passing-geo) for details.

### Using geospatial data with JavaScript UDFs[¶](#using-geospatial-data-with-javascript-udfs "Link to this heading")

JavaScript UDFs allow the GEOGRAPHY or GEOMETRY type as an argument and as a return value.

If a JavaScript UDF has an argument of type GEOGRAPHY or GEOMETRY, that argument is visible as a JSON object in GeoJSON
format inside the UDF body.

If a JavaScript UDF returns GEOGRAPHY or GEOMETRY, the UDF body is expected to return a JSON object in GeoJSON format.

For example, these two JavaScript UDFs are roughly equivalent to the built-in functions ST\_X and ST\_MAKEPOINT:

```
CREATE OR REPLACE FUNCTION my_st_x(g GEOGRAPHY) RETURNS REAL
LANGUAGE JAVASCRIPT
AS
$$
  if (G["type"] != "Point")
  {
     throw "Not a point"
  }
  return G["coordinates"][0]
$$;

CREATE OR REPLACE FUNCTION my_st_makepoint(lng REAL, lat REAL) RETURNS GEOGRAPHY
LANGUAGE JAVASCRIPT
AS
$$
  g = {}
  g["type"] = "Point"
  g["coordinates"] = [ LNG, LAT ]
  return g
$$;
```

Copy

### Using geospatial data with Python UDFs[¶](#using-geospatial-data-with-python-udfs "Link to this heading")

Python UDFs allow the GEOGRAPHY and GEOMETRY type as an argument and as a return value.

If a Python UDF has an argument of type GEOGRAPHY or GEOMETRY, that argument is represented as a
GeoJSON object, which is converted to a Python `dict` object inside the UDF body.

If a Python UDF returns GEOGRAPHY or GEOMETRY, the UDF body is expected to return a Python `dict` object
that complies with the structure of GeoJSON.

For example, this Python UDF returns the number of distinct geometries that constitute a composite GEOGRAPHY type:

```
CREATE OR REPLACE FUNCTION py_numgeographys(geo GEOGRAPHY)
RETURNS INTEGER
LANGUAGE PYTHON
RUNTIME_VERSION = 3.10
PACKAGES = ('shapely')
HANDLER = 'udf'
AS $$
from shapely.geometry import shape, mapping
def udf(geo):
    if geo['type'] not in ('MultiPoint', 'MultiLineString', 'MultiPolygon', 'GeometryCollection'):
        raise ValueError('Must be a composite geometry type')
    else:
        g1 = shape(geo)
        return len(g1.geoms)
$$;
```

Copy

Check [Snowflake Labs](https://github.com/Snowflake-Labs/sf-samples/tree/main/samples/geospatial/Python%20UDFs) for more samples
of Python UDFs. Some of them enable complex spatial manipulations or simplify data ingestion. For example,
[this UDF](https://github.com/Snowflake-Labs/sf-samples/blob/main/samples/geospatial/Python%20UDFs/PY_LOAD_GEOFILES.sql) allows
reading formats that aren’t supported natively, such as Shapefiles (.SHP), TAB, KML, GPKG, and others.

Note

The code samples in Snowflake Labs are intended solely for reference and educational purposes. These code samples aren’t covered
by any Service Level Agreement.

### Using GEOGRAPHY objects with H3[¶](#using-geography-objects-with-h3 "Link to this heading")

[H3](https://h3geo.org/docs/) is a [hierarchical geospatial index](https://h3geo.org/docs/highlights/indexing) that partitions
the world into hexagonal cells in a [discrete global grid system](https://en.wikipedia.org/wiki/Discrete_global_grid).

Snowflake provides SQL functions that enable you to use H3 with [GEOGRAPHY](#label-data-types-geography) objects. You can
use these functions to:

* Get the H3 cell ID ([index](https://h3geo.org/docs/core-library/h3Indexing)) for a GEOGRAPHY object that represents a Point (and vice versa).
* Get the IDs of the minimal set of H3 cells that cover a GEOGRAPHY object.
* Get the IDs of the H3 cells that have centroids within a GEOGRAPHY object that represents a Polygon.
* Get the GEOGRAPHY object that represents the boundary of an H3 cell.
* Get the parents and children of a given H3 cell.
* Get the longitude and latitude of the centroid of an H3 cell (and vice versa).
* Get the [resolution](https://h3geo.org/docs/core-library/restable) of an H3 cell.
* Get the hexadecimal representation of an H3 cell ID (and vice versa).

For more information about these functions, see [Geospatial functions](functions-geospatial).

## Choosing the geospatial data type to use (GEOGRAPHY or GEOMETRY)[¶](#choosing-the-geospatial-data-type-to-use-geography-or-geometry "Link to this heading")

The next sections explain the differences between the GEOGRAPHY and GEOMETRY data types:

* [Understanding the differences between GEOGRAPHY and GEOMETRY](#label-geometry-geography-diffs)
* [Examples comparing the GEOGRAPHY and GEOMETRY data types](#label-geometry-geography-diffs-examples)
* [Understanding the differences in input data validation](#label-geometry-geography-validate)

### Understanding the differences between GEOGRAPHY and GEOMETRY[¶](#understanding-the-differences-between-geography-and-geometry "Link to this heading")

Although both the GEOGRAPHY and GEOMETRY data types define geospatial features, the types use different models. The following
table summarizes the differences.

| GEOGRAPHY data type | GEOMETRY data type |
| --- | --- |
| * Defines features on a sphere. * Only the WGS84 coordinate system. [SRID](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) is always 4326. * Coordinates are latitude (-90 to 90) and longitude (-180 to 180) in degrees. * Results of measurement operations (ST\_LENGTH, ST\_AREA, and so on) are in meters. * Segments are interpreted as great circle arcs on the Earth’s surface. | * Defines features on a plane. * Any coordinate system is supported. * Unit of coordinate values are defined by the spatial reference system. * Results of measurement operations (ST\_LENGTH, ST\_AREA, and so on) are in the same unit as coordinates. For example, if the   input coordinates are in degrees, the results are in degrees. * Segments are interpreted as straight lines on the plane. |

### Examples comparing the GEOGRAPHY and GEOMETRY data types[¶](#examples-comparing-the-geography-and-geometry-data-types "Link to this heading")

The following examples compare the output of the geospatial functions when using the GEOGRAPHY and GEOMETRY data types as input.

#### Example 1: Querying the distance between Berlin and San Francisco[¶](#example-1-querying-the-distance-between-berlin-and-san-francisco "Link to this heading")

The following table compares the output of [ST\_DISTANCE](functions/st_distance) for GEOGRAPHY types and GEOMETRY types:

| ST\_DISTANCE using . GEOGRAPHY input | ST\_DISTANCE using . GEOMETRY input |
| --- | --- |
| ``` SELECT ST_DISTANCE(     ST_POINT(13.4814, 52.5015),     ST_POINT(-121.8212, 36.8252))   AS distance_in_meters; ```  Copy  ``` +--------------------+ | DISTANCE_IN_METERS | |--------------------| |   9182410.99227821 | +--------------------+ ``` | ``` SELECT ST_DISTANCE(     ST_GEOMPOINT(13.4814, 52.5015),     ST_GEOMPOINT(-121.8212, 36.8252))   AS distance_in_degrees; ```  Copy  ``` +---------------------+ | DISTANCE_IN_DEGREES | |---------------------| |       136.207708844 | +---------------------+ ``` |

As shown in the example above:

* With GEOGRAPHY input values, the input coordinates are in degrees, and the output value is in meters. (The result is 9,182 km.)
* With GEOMETRY input values, the input coordinates and output value are degrees. (The result is 136.208 degrees.)

#### Example 2: Querying the area of Germany[¶](#example-2-querying-the-area-of-germany "Link to this heading")

The following table compares the output of [ST\_AREA](functions/st_area) for GEOGRAPHY types and GEOMETRY types:

| ST\_AREA using . GEOGRAPHY input | ST\_AREA using . GEOMETRY input |
| --- | --- |
| ``` SELECT ST_AREA(border) AS area_in_sq_meters   FROM world_countries   WHERE name = 'Germany'; ```  Copy  ``` +-------------------+ | AREA_IN_SQ_METERS | |-------------------| |  356379183635.591 | +-------------------+ ``` | ``` SELECT ST_AREA(border) as area_in_sq_degrees   FROM world_countries_geom   WHERE name = 'Germany'; ```  Copy  ``` +--------------------+ | AREA_IN_SQ_DEGREES | |--------------------| |       45.930026848 | +--------------------+ ``` |

As shown in the example above:

* With GEOGRAPHY input values, the input coordinates are in degrees, the output value is in square meters. (The result is
  356,379 km^2.)
* With GEOMETRY input values, the input coordinates in degrees, and the output value is in square degrees. (The result is
  45.930 square degrees.)

#### Example 3: Querying the names of countries overlapping the line from Berlin to San Francisco[¶](#example-3-querying-the-names-of-countries-overlapping-the-line-from-berlin-to-san-francisco "Link to this heading")

The following table compares the output of [ST\_INTERSECTS](functions/st_intersects) for GEOGRAPHY types and GEOMETRY types:

| ST\_INTERSECTS using . GEOGRAPHY input | ST\_INTERSECTS using . GEOMETRY input |
| --- | --- |
| ``` SELECT name FROM world_countries WHERE   ST_INTERSECTS(border,     TO_GEOGRAPHY(       'LINESTRING(13.4814 52.5015, -121.8212 36.8252)'     )); ```  Copy  ``` +--------------------------+ | NAME                     | |--------------------------| |                  Germany | |                  Denmark | |                  Iceland | |                Greenland | |                   Canada | | United States of America | +--------------------------+ ``` | ``` SELECT name FROM world_countries_geom WHERE   ST_INTERSECTS(border,     TO_GEOMETRY(       'LINESTRING(13.4814 52.5015, -121.8212 36.8252)'     )); ```  Copy  ``` +--------------------------+ | NAME                     | |--------------------------| |                  Germany | |                  Belgium | |              Netherlands | |           United Kingdom | | United States of America | +--------------------------+ ``` |
| [Countries intersecting when using GEOGRAPHY](../_images/st_intersect-example-geography.png) | [Countries intersecting when using GEOMETRY](../_images/st_intersect-example-geometry.png) |

### Understanding the differences in input data validation[¶](#understanding-the-differences-in-input-data-validation "Link to this heading")

To create a GEOMETRY or GEOGRAPHY object for an input shape, you must use a shape that is well-formed and valid, according to the
[OGC rules for Simple Features](https://www.ogc.org/standards/sfa). The next sections explain how the validity of input data differs between GEOMETRY and GEOGRAPHY.

#### A shape can be valid GEOGRAPHY but invalid GEOMETRY[¶](#a-shape-can-be-valid-geography-but-invalid-geometry "Link to this heading")

A given shape can be a valid GEOGRAPHY object but an invalid GEOMETRY object (and vice versa).

For example, self-intersecting polygons are disallowed by the OGC rules. A given set of points might define edges that intersect in
Cartesian domain but not on a sphere. Consider the following polygon:

```
POLYGON((0 50, 25 50, 50 50, 0 50))
```

Copy

In the Cartesian domain, this polygon degrades to a line and, as a result, is invalid.

However, on a sphere, this same polygon doesn’t intersect itself and is valid:

[![POLYGON((0 50, 25 50, 50 50, 0 50)) invalid geometry, but valid geography](../_images/geography-valid-geometry-invalid-example.png)](../_images/geography-valid-geometry-invalid-example.png)

#### Conversion and constructor functions handle validation differently[¶](#conversion-and-constructor-functions-handle-validation-differently "Link to this heading")

When the input data is invalid, the GEOMETRY and GEOGRAPHY functions handle validation in different ways:

* Some of the functions for constructing and converting to GEOGRAPHY objects might attempt to repair the shape to handle problems
  such as unclosed loops, spikes, cuts, and self-intersecting loops in polygons. For example, when either the
  [TO\_GEOGRAPHY](functions/to_geography) function or the
  [ST\_MAKEPOLYGON](functions/st_makepolygon) function is used to
  construct a polygon, the function corrects the orientation of the loop to prevent the creation of polygons that span more than half of the
  globe. However, the [ST\_MAKEPOLYGONORIENTED](functions/st_makepolygonoriented) function doesn’t attempt to correct the orientation of
  the loop.

  If the function is successful in repairing the shape, the function returns a GEOGRAPHY object.
* The functions for constructing and converting to GEOMETRY objects (for example, [TO\_GEOMETRY](functions/to_geometry)) don’t
  support the ability to repair the shape.

## Converting between GEOGRAPHY and GEOMETRY[¶](#converting-between-geography-and-geometry "Link to this heading")

Snowflake supports converting from a GEOGRAPHY object to a GEOMETRY object (and vice versa). Snowflake also supports
transformations of objects that use different spatial reference systems (SRS).

The following example converts a GEOGRAPHY object that represents a point to a GEOMETRY object with the [SRID](https://en.wikipedia.org/wiki/Spatial_reference_system#Identifier) 0:

```
SELECT TO_GEOMETRY(TO_GEOGRAPHY('POINT(-122.306100 37.554162)'));
```

Copy

To set the SRID of the new GEOMETRY object, pass the SRID as an argument to the constructor function. For example:

```
SELECT TO_GEOMETRY(TO_GEOGRAPHY('POINT(-122.306100 37.554162)', 4326));
```

Copy

If you need to set the SRID of an existing GEOMETRY object, see [Changing the spatial reference system (SRS) and SRID of a GEOMETRY object](#label-geometry-change-srs).

## Specifying how invalid geospatial shapes are handled[¶](#specifying-how-invalid-geospatial-shapes-are-handled "Link to this heading")

By default, when you use a [geospatial conversion function](functions-geospatial) to convert
[data in a supported input format](#label-data-types-geospatial-io-formats) to a GEOGRAPHY or GEOMETRY object, the function
does the following:

1. The function attempts to validate the shape in the input data.
2. The function determines if the shape is valid according to the
   [Open Geospatial Consortium’s Simple Feature Access / Common Architecture](https://www.ogc.org/standards/sfa) standard.
3. If the shape is invalid, the function attempts to repair the data (for example, fixing polygons by closing the rings).
4. If the shape is still invalid after the repairs, the function reports an error and doesn’t create the GEOGRAPHY or GEOMETRY
   object. (For the TRY\_\* functions, the functions return NULL, rather than reporting an error.)

With this feature, you have more control over the validation and repair process. You can:

* Allow these conversion functions to create GEOGRAPHY and GEOMETRY objects for invalid shapes.
* Determine if the shape for a GEOGRAPHY or GEOMETRY object is invalid.

### Understanding the effects of invalid shapes on geospatial functions[¶](#understanding-the-effects-of-invalid-shapes-on-geospatial-functions "Link to this heading")

Different [geospatial functions](functions-geospatial) have different effects when you pass in a GEOGRAPHY
or GEOMETRY object for an invalid shape.

#### Effects on GEOMETRY objects[¶](#effects-on-geometry-objects "Link to this heading")

For GEOMETRY objects:

* The following functions return results based on the original invalid shape:

  + [ST\_AREA](functions/st_area)
  + [ST\_ASGEOJSON](functions/st_asgeojson)
  + [ST\_ASWKB](functions/st_aswkb)
  + [ST\_ASWKT](functions/st_aswkt)
  + [ST\_CENTROID](functions/st_centroid)
  + [ST\_CONTAINS](functions/st_contains)
  + [ST\_DIMENSION](functions/st_dimension)
  + [ST\_DISTANCE](functions/st_distance)
  + [ST\_ENVELOPE](functions/st_envelope)
  + [ST\_INTERSECTS](functions/st_intersects)
  + [ST\_LENGTH](functions/st_length)
  + [ST\_NPOINTS , ST\_NUMPOINTS](functions/st_npoints)
  + [ST\_PERIMETER](functions/st_perimeter)
  + [ST\_SETSRID](functions/st_setsrid)
  + [ST\_SRID](functions/st_srid)
  + [ST\_X](functions/st_x)
  + [ST\_XMAX](functions/st_xmax)
  + [ST\_XMIN](functions/st_xmin)
  + [ST\_Y](functions/st_y)
  + [ST\_YMAX](functions/st_ymax)
  + [ST\_YMIN](functions/st_ymin)
* The following functions validate the shape and fail with an error if the shape is invalid:

  + [ST\_MAKELINE](functions/st_makeline)
  + [ST\_MAKEPOLYGON](functions/st_makepolygon)

#### Effects on GEOGRAPHY objects[¶](#effects-on-geography-objects "Link to this heading")

For GEOGRAPHY objects:

* The following functions return results based on the original invalid shape:

  + [ST\_ASWKB](functions/st_aswkb)
  + [ST\_ASWKT](functions/st_aswkt)
  + [ST\_ASGEOJSON](functions/st_asgeojson)
  + [ST\_AZIMUTH](functions/st_azimuth)
  + [ST\_COLLECT](functions/st_collect)
  + [ST\_DIMENSION](functions/st_dimension)
  + [ST\_GEOHASH](functions/st_geohash)
  + [ST\_HAUSDORFFDISTANCE](functions/st_hausdorffdistance)
  + [ST\_MAKELINE](functions/st_makeline)
  + [ST\_NPOINTS , ST\_NUMPOINTS](functions/st_npoints)
  + [ST\_POINTN](functions/st_pointn)
  + [ST\_SRID](functions/st_srid)
  + [ST\_ENDPOINT](functions/st_endpoint)
  + [ST\_STARTPOINT](functions/st_startpoint)
  + [ST\_X](functions/st_x)
  + [ST\_Y](functions/st_y)
* The following functions validate the shape and fail with an error if the shape is invalid:

  + [ST\_COLLECT](functions/st_collect)
  + [ST\_MAKEPOLYGON](functions/st_makepolygon)
  + [ST\_MAKEPOLYGONORIENTED](functions/st_makepolygonoriented)
* The following functions return NULL if it isn’t possible to compute the value:

  + [ST\_AREA](functions/st_area)
  + [ST\_CENTROID](functions/st_centroid)
  + [ST\_CONTAINS](functions/st_contains)
  + [ST\_COVERS](functions/st_covers)
  + [ST\_DIFFERENCE](functions/st_difference)
  + [ST\_DISTANCE](functions/st_distance)
  + [ST\_DWITHIN](functions/st_dwithin)
  + [ST\_ENVELOPE](functions/st_envelope)
  + [ST\_INTERSECTION](functions/st_intersection)
  + [ST\_INTERSECTION\_AGG](functions/st_intersection_agg)
  + [ST\_INTERSECTS](functions/st_intersects)
  + [ST\_LENGTH](functions/st_length)
  + [ST\_PERIMETER](functions/st_perimeter)
  + [ST\_SIMPLIFY](functions/st_simplify)
  + [ST\_SYMDIFFERENCE](functions/st_symdifference)
  + [ST\_UNION](functions/st_union)
  + [ST\_UNION\_AGG](functions/st_union_agg)
  + [ST\_XMAX](functions/st_xmax)
  + [ST\_XMIN](functions/st_xmin)
  + [ST\_YMAX](functions/st_ymax)
  + [ST\_YMIN](functions/st_ymin)

### Working with invalid shapes[¶](#working-with-invalid-shapes "Link to this heading")

The next sections explain how to allow functions to create invalid shapes and how to determine if a GEOGRAPHY or GEOMETRY object
represents an invalid or repaired shape.

#### Allowing conversion functions to create invalid shapes[¶](#allowing-conversion-functions-to-create-invalid-shapes "Link to this heading")

To allow the following conversion functions to create invalid geospatial objects, pass `TRUE` for the second argument
(`allowInvalid`):

```
TO_GEOGRAPHY( <input> [, <allowInvalid> ] )
```

Copy

```
ST_GEOGFROMWKB( <input> [, <allowInvalid> ] )
```

Copy

```
ST_GEOGFROMWKT( <input> [, <allowInvalid> ] )
```

Copy

```
TO_GEOMETRY( <input> [, <allowInvalid> ] )
```

Copy

```
ST_GEOMFROMWKB( <input> [, <allowInvalid> ] )
```

Copy

```
ST_GEOMFROMWKT( <input> [, <allowInvalid> ] )
```

Copy

By default, the `allowInvalid` argument is `FALSE`.

When you pass `TRUE` for the `allowInvalid` argument, the conversion function returns a GEOGRAPHY or GEOMETRY
object, even when the input shape is invalid and can’t be repaired successfully.

For example, the following input shape is a LineString that consists of the same two Points. Passing `TRUE` for the
`allowInvalid` argument returns a GEOMETRY object that represents an invalid shape:

```
SELECT TO_GEOMETRY('LINESTRING(100 102,100 102)', TRUE);
```

Copy

#### Determining if a shape is invalid[¶](#determining-if-a-shape-is-invalid "Link to this heading")

To determine if a GEOGRAPHY or GEOMETRY object is invalid, call the [ST\_ISVALID](functions/st_isvalid) function.

The following example checks if an object is valid:

```
SELECT TO_GEOMETRY('LINESTRING(100 102,100 102)', TRUE) AS g, ST_ISVALID(g);
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

1. [Data types](#data-types)
2. [Geospatial input and output](#geospatial-input-and-output)
3. [Using geospatial data in Snowflake](#using-geospatial-data-in-snowflake)
4. [Choosing the geospatial data type to use (GEOGRAPHY or GEOMETRY)](#choosing-the-geospatial-data-type-to-use-geography-or-geometry)
5. [Converting between GEOGRAPHY and GEOMETRY](#converting-between-geography-and-geometry)
6. [Specifying how invalid geospatial shapes are handled](#specifying-how-invalid-geospatial-shapes-are-handled)

Related content

1. [Geospatial functions](/sql-reference/functions-geospatial)
2. [Data type conversion](/sql-reference/data-type-conversion)