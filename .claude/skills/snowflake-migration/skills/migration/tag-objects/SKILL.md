---
name: tag-objects
description: Tag and untag code units in the registry with free-form labels, and find objects by tag. Triggers: tag this object, tag these tables, untag, label objects, add a tag, show tagged objects, which objects are tagged.
license: Proprietary. See License-Skills for complete terms
---

# Tag objects

Tags are the user's own labels on a code unit — `pii`, `finance`, `needs-review`. They mean nothing
to the state machine and gate nothing: no task reads them, and tagging never changes an object's
stage. They exist so a person can group objects the registry has no field for.

Tags live at `extensions.tags` as an array of objects:

```json
[{ "id": "pii", "details": {} }, { "id": "finance", "details": { "owner": "ap" } }]
```

`id` is the label the app renders as a chip. `details` is a free-form map for anything the user
wants to carry with the tag; leave it `{}` when there is nothing to put in it.

## Tagging

`update_registry`'s `value` writes raw JSON at an `extensions.<path>` field. It **replaces** the
whole array, so read the current tags before writing:

1. `query_registry(where="<filter>", fields="id,source,extensions")` — `extensions` is not in the
   default projection, so it must be named or the current tags come back empty and you will drop
   them.
2. Merge: add the new tag (or drop the one being removed) to the array you just read.
3. `update_registry(field="extensions.tags", value=<the merged array>, objects="<id>")`

Untagging is the same three steps with the tag removed. To clear every tag, write `[]`.

Tag one object per call when the tag sets differ — `objects="a,b"` and `where=` write the *same*
array to every match, which is right for applying a shared tag to a batch and wrong for merging
into objects that already have different tags.

## Finding tagged objects

The registry filter has no array-contains operator; an array compares as its JSON text, so match a
tag with `LIKE`:

```
query_registry(where="extensions.tags LIKE '%\"pii\"%'", fields="id,source,extensions")
```

Quote the id as it appears in the JSON (`"pii"`, with the quotes inside the `%`) — a bare `%pii%`
also matches a tag named `pii-review` and any `details` value containing the word.

## Reporting back

Say which objects you tagged and with what. Mention that tags show as chips on the object rows in
the app's Objects panel, so the user can see them without asking.
