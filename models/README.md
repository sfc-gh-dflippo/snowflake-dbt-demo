# Snowflake Data Cloud Deployment Framework

- Snowflake Professional Services has developed a reference architecture to describe best practices
- This project has models broken down into folders for the different kinds of DB/schema seen as repeatable, flexible patterns
- Please engage with Snowflake PS for additional information but a high level description is provided below

## Snowflake has seen consistent success when customers break down databases and schemas into the following categories

- A Raw layer replicates sources, enables data acquisition agility, and facilitates intuitive data cataloging.
- An Integration layer enables the centralization of well governed business rules, data integration across source systems and derivation of enterprise measures.
- A Presentation layer delivers optimized data models for end-user consumption. These may be views against the raw and integration layers or tables depending on performance requirements.
- A Share layer is used for objects that will be shared to other business entities in the same account and external customers/partners through secure data sharing.
- A common database contains reusable objects such as UDF's, stored procedures, file formats, external stages, pipes, etc.
- A workspace database is used by analysts, data scientists, engineers to build objects for data self service.
