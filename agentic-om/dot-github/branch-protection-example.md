# Branch Protection Example for `main`

Recommended GitHub settings for the `main` branch:

- Require a pull request before merging.
- Require status checks to pass before merging.
- Require at least one approval.
- Dismiss stale pull request approvals when new commits are pushed.
- Block force pushes.
- Block branch deletions.
- (Optional) Require linear history.

These settings align with the trunk-based, PR-first workflow
described in `docs/branching-workflow-standard.md`.
