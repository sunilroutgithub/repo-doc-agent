---
name: GitHub 404 diagnostics
description: Guidance for distinguishing GitHub repository, file, branch, and permission failures.
---

GitHub and PyGithub may return 404 both for a nonexistent resource and for a private resource the token cannot see. A repository lookup that succeeds proves only repository read access; a later file, branch, commit, or pull-request operation can fail separately.

**Why:** The same generic `404 Not Found` string previously obscured whether the request used the wrong owner/repository, an invalid case-sensitive file path, or insufficient write permissions.

**How to apply:** Test repository lookup and file lookup independently, then check write permissions for branch/commit/PR operations. Use explicit token authentication and stage-specific, secret-safe error messages.