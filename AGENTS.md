# gitlab-group-forker

Single-file Python utility for recursively forking GitLab groups into another group hierarchy.

## Verify

`mise run check`: compile the Python entrypoint. No unit-test suite exists yet.

CI also runs actionlint, zizmor, and strict Renovate validation. The required gate is `check`.

## Stack

Follows https://github.com/BlackDark/agent-presets/blob/main/stack/core.md. This repo intentionally stays a small requirements-based script; no pyproject migration is needed.

## Map

- `fork_gitlab_group.py`: CLI, group traversal, and fork operations.
- `requirements.txt`: runtime dependencies.

## Git

- Conventional Commits, one topic per PR.
- Squash unless commits need separate review.
- Force-push only with `--force-with-lease` on own branches.

## Boundaries

- Tools come from `mise.toml`; no global installs.
- Never use a personal GitLab token or create/delete real groups and projects from a local session.
