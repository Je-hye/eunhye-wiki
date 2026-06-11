# ADR 001: Separate Public and Private Trust Zones

- Status: Accepted
- Date: 2026-06-10
- Issue: https://github.com/Je-hye/eunhye-wiki/issues/1

## Context

The product serves two audiences from one codebase:

- Public visitors explore approved portfolio content.
- The owner searches private notes and project documents.

A missing application-level visibility filter must not expose private content
through the public service.

## Decision

Run the shared FastAPI core through two thin entrypoints:

- `public-api` connects only to `public-db`.
- `private-api` connects only to `private-db` and may mount local notes.

Local development starts both trust zones with one `docker compose up` command.
The public deployment includes only public services.

The public service receives no private database hostname, credentials, local
notes mount, or private routes. The two databases use separate internal Docker
networks, and the public API is not attached to the private network.

The web container uses a third frontend network and does not bridge the API
networks. Browser-side requests use the API ports explicitly exposed on the
local host. Local development ports bind to loopback so the unauthenticated
private foundation is not reachable from other devices on the LAN.

## Alternatives

### One database with a visibility column

- Pros: simplest migrations, deployment, and cross-document operations.
- Cons: one missing filter can expose private documents.

### One database with separate schemas

- Pros: clearer ownership with less operational cost than two databases.
- Cons: the API process can still reach both schemas with excessive privileges.

### Separate API and database instances

- Pros: credentials and network paths enforce the trust boundary outside
  application query logic.
- Cons: more containers, duplicated migrations, and higher local resource use.

## Consequences

- API business logic remains shared; only composition roots and capabilities
  differ.
- Migrations must run against both databases.
- Public and private routing require regression tests.
- Public data promotion needs an explicit publishing workflow.
- Private notes remain local and are never part of the public deployment.
