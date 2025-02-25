---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-macho.html
applies_to:
  stack: all
  serverless: all
---

# Mach-O header fields [ecs-macho]

These fields contain Mac OS Mach Object file format (Mach-O) metadata.

::::{warning}
These fields are in beta and are subject to change.
::::



## Mach-O header field details [_mach_o_header_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-macho-go-import-hash$$$[macho.go_import_hash](#field-macho-go-import-hash) | A hash of the Go language imports in a Mach-O file excluding standard library imports. An import hash can be used to fingerprint binaries even after recompilation or other code-level transformations have occurred, which would change more traditional hash values.<br><br>The algorithm used to calculate the Go symbol hash and a reference implementation are available here: [https://github.com/elastic/toutoumomoma](https://github.com/elastic/toutoumomoma)<br><br>type: keyword<br><br>example: `10bddcb4cee42080f76c88d9ff964491`<br> | extended |
| $$$field-macho-go-imports$$$[macho.go_imports](#field-macho-go-imports) | List of imported Go language element names and types.<br><br>type: flattened<br> | extended |
| $$$field-macho-go-imports-names-entropy$$$[macho.go_imports_names_entropy](#field-macho-go-imports-names-entropy) | Shannon entropy calculation from the list of Go imports.<br><br>type: long<br> | extended |
| $$$field-macho-go-imports-names-var-entropy$$$[macho.go_imports_names_var_entropy](#field-macho-go-imports-names-var-entropy) | Variance for Shannon entropy calculation from the list of Go imports.<br><br>type: long<br> | extended |
| $$$field-macho-go-stripped$$$[macho.go_stripped](#field-macho-go-stripped) | Set to true if the file is a Go executable that has had its symbols stripped or obfuscated and false if an unobfuscated Go executable.<br><br>type: boolean<br> | extended |
| $$$field-macho-import-hash$$$[macho.import_hash](#field-macho-import-hash) | A hash of the imports in a Mach-O file. An import hash can be used to fingerprint binaries even after recompilation or other code-level transformations have occurred, which would change more traditional hash values.<br><br>This is a synonym for symhash.<br><br>type: keyword<br><br>example: `d41d8cd98f00b204e9800998ecf8427e`<br> | extended |
| $$$field-macho-imports$$$[macho.imports](#field-macho-imports) | List of imported element names and types.<br><br>type: flattened<br><br>Note: this field should contain an array of values.<br> | extended |
| $$$field-macho-imports-names-entropy$$$[macho.imports_names_entropy](#field-macho-imports-names-entropy) | Shannon entropy calculation from the list of imported element names and types.<br><br>type: long<br> | extended |
| $$$field-macho-imports-names-var-entropy$$$[macho.imports_names_var_entropy](#field-macho-imports-names-var-entropy) | Variance for Shannon entropy calculation from the list of imported element names and types.<br><br>type: long<br> | extended |
| $$$field-macho-sections$$$[macho.sections](#field-macho-sections) | An array containing an object for each section of the Mach-O file.<br><br>The keys that should be present in these objects are defined by sub-fields underneath `macho.sections.*`.<br><br>type: nested<br><br>Note: this field should contain an array of values.<br> | extended |
| $$$field-macho-sections-entropy$$$[macho.sections.entropy](#field-macho-sections-entropy) | Shannon entropy calculation from the section.<br><br>type: long<br> | extended |
| $$$field-macho-sections-name$$$[macho.sections.name](#field-macho-sections-name) | Mach-O Section List name.<br><br>type: keyword<br> | extended |
| $$$field-macho-sections-physical-size$$$[macho.sections.physical_size](#field-macho-sections-physical-size) | Mach-O Section List physical size.<br><br>type: long<br> | extended |
| $$$field-macho-sections-var-entropy$$$[macho.sections.var_entropy](#field-macho-sections-var-entropy) | Variance for Shannon entropy calculation from the section.<br><br>type: long<br> | extended |
| $$$field-macho-sections-virtual-size$$$[macho.sections.virtual_size](#field-macho-sections-virtual-size) | Mach-O Section List virtual size. This is always the same as `physical_size`.<br><br>type: long<br> | extended |
| $$$field-macho-symhash$$$[macho.symhash](#field-macho-symhash) | A hash of the imports in a Mach-O file. An import hash can be used to fingerprint binaries even after recompilation or other code-level transformations have occurred, which would change more traditional hash values.<br><br>This is a Mach-O implementation of the Windows PE imphash<br><br>type: keyword<br><br>example: `d3ccf195b62a9279c3c19af1080497ec`<br> | extended |


## Field reuse [_field_reuse_15]

The `macho` fields are expected to be nested at:

* `file.macho`
* `process.macho`

Note also that the `macho` fields are not expected to be used directly at the root of the events.

