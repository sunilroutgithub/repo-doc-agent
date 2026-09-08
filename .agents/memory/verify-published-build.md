---
name: Verify published build
description: How to confirm that Replit's live deployment contains the current source.
---

A successful deployment status does not by itself prove the live service contains the latest workspace changes. A safe public contract endpoint such as `/openapi.json` can expose an old schema and reveal that a previous build is still serving.

**Why:** Runtime errors can appear inconsistent with current code when publishing was not actually performed after the latest edits.

**How to apply:** Compare the live OpenAPI schema or another non-mutating endpoint with the current source before debugging production behavior. Republish, then verify the schema changed before retrying mutation endpoints.