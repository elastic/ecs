---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-converting.html
applies_to:
  stack: all
  serverless: all
---

# Map custom data to ECS [ecs-converting]

A common schema helps you correlate and use data from various sources.

Fields for most Elastic modules and solutions (version 7.0 and later) are mapped to the Elastic Common Schema. You may want to map data from other implementations to ECS to help you correlate data across all of your products and solutions.


## Before you start [ecs-converting-before-you-start]

Before you start a conversion, be sure that you understand the basics below.


### Core and extended levels [core-or-ext]

Make sure you understand the distinction between Core and Extended fields, as explained in the [Guidelines and Best Practices](/reference/ecs-guidelines.md).

Core and Extended fields are documented in the [*ECS Field Reference*](/reference/ecs-field-reference.md) or, for a single page representation of all fields, please see the [generated CSV of fields](https://github.com/elastic/ecs/blob/master/generated/csv/fields.csv).


### An approach to mapping an existing implementation [ecs-conv]

Here’s the recommended approach for converting an existing implementation to ECS.

1. Review each field in your original event and map it to the relevant ECS field.

    * Start by mapping your field to the relevant ECS Core field.
    * If a relevant ECS Core field does not exist, map your field to the relevant ECS Extended field.
    * If no relevant ECS Extended field exists, consider keeping your field with its original details, or possibly renaming it using ECS naming guidelines and attempt to map one or more of your original event fields to it.

2. Review each ECS Core field, and attempt to populate it.

    * Review your original event data again
    * Consider populating the field based on additional meta-data such as static information (e.g. add `event.category:authentication` even if your auth events don’t mention the word "authentication")
    * Consider capturing additional environment meta-data, such as information about the host, container or cloud instance.

3. Review other extended fields from any field set you are already using, and attempt to populate it as well.
4. Set `ecs.version` to the version of the schema you are conforming to. This will allow you to upgrade your sources, pipelines and content (like dashboards) smoothly in the future.


### Use a spreadsheet to plan your migration [ecs-conv-spreadsheet]

Using a spreadsheet to plan the migration from pre-existing source fields to ECS is a common practice. It’s a good way to address each of your fields methodically among colleagues.

To help you plan your migration, Elastic offers a [spreadsheet template](https://ela.st/sample-pipeline-mapping). You can use a CSV version of this spreadsheet to [automatically create an {{es}} ingest pipeline](#ecs-map-custom-data-to-ecs-es-pipeline). This is the easiest and most consistent way to map your custom data to ECS, regardless of your ingest method.


## Map custom data to ECS using an {{es}} ingest pipeline [ecs-map-custom-data-to-ecs-es-pipeline]

Use {{kib}}'s **Create pipeline from CSV** feature to create an {{es}} ingest pipeline from a CSV file that maps custom data to ECS fields.

Before you start, ensure you meet the [prerequisites](docs-content://manage-data/ingest/transform-enrich/ingest-pipelines.md#ingest-prerequisites) to create ingest pipelines in {{kib}}.

1. Download or make a copy of the [spreadsheet template](https://ela.st/sample-pipeline-mapping).
2. Use the spreadsheet to map your custom data to ECS fields. While you can include additional columns, {{kib}} only processes the following supported columns. Other columns are ignored.

:::::{dropdown} Supported columns
`source_field`
:   (Required) JSON field key from your custom data. Supports dot notation. Rows with an empty `source_field` are skipped.

 `destination_field`
:   (Required) ECS field name. Supports dot notation. To perform a `format_action` without renaming the field, leave `destination_field` empty.

If the `destination field` is `@timestamp`, a `format_action` of `parse_timestamp` and a `timestamp_format` of `UNIX_MS` are used, regardless of any provided values. This helps prevent downstream conversion problems.

`format_action`
:   (Optional) Conversion to apply to the field value.

::::{dropdown} Valid values
(empty)
:   No conversion.

`parse_timestamp`
:   Formats a date or time value. To specify a format, use `timestamp_format`.

`to_array`
:   Converts to an array.

`to_boolean`
:   Converts to a boolean.

`to_float`
:   Converts to a floating point number.

`to_integer`
:   Converts to an integer

`to_string`
:   Converts to a string.

`lowercase`
:   Converts to lowercase.

`uppercase`
:   Converts to uppercase.
::::

`timestamp_format`
:   (Optional) Time and date format to use with the `parse_timestamp` format action. Valid values are `UNIX`, `UNIX_MS`, `ISO8601`, `TAI64N`, and [Java time patterns](elasticsearch://docs/reference/elasticsearch/mapping-reference/mapping-date-format.md). Defaults to `UNIX_MS`.

`copy_action`
:   (Optional) Action to take on the `source_field`. Valid values are:

::::{dropdown} Valid values
(empty)
:   (Default) Uses the default action. You’ll specify the default action later on {{kib}}'s **Create pipeline from CSV** page.

`copy`
:   Makes a copy of the `source_field` to use as the `destination_field`. The final document contains both fields.

`rename`
:   Renames the `source_field` to the `destination_field`. The final document only contains the `destination_field`.

::::
:::::

3. Save and export your spreadsheet as a CSV file.

    ::::{note}
    {{kib}}'s **Create pipeline from CSV** feature only supports CSV files up to 100 MB.
    ::::

4. In {{kib}}, open the main menu and click **Stack Management > Ingest Pipelines > Create pipeline > New pipeline from CSV**.

   :::{image} ../images/kib-create-pipeline-from-csv.png
   :alt: Create Pipeline from CSV in Kibana
   :class: screenshot
   :::

5. On the **Create pipeline from CSV** page, upload your CSV file.
6. Under **Default action**, select the **Copy field name** or **Rename field** option.

    For the **Copy field name** option, {{kib}} makes a copy of the `source_field` to use as the `destination_field` by default. The final document contains both fields.

    For the **Rename field** option, renames the `source_field` to the `destination_field` by default. The final document only contains the `destination_field`.

    You can override this default using the `copy_action` column of your CSV.

7. Click **Process CSV**.

   {{kib}} displays a JSON preview of the ingest pipeline generated from your CSV file.

   :::{image} ../images/kib-create-pipeline-from-csv-preview.png
   :alt: Preview pipeline from CSV in Kibana
   :class: screenshot
   :::

8. To create the pipeline, click **Continue to create pipeline**.
9. On the **Create pipeline** page, you can add additional ingest processors to your pipeline.

    When you’re done, click **Create pipeline**.
