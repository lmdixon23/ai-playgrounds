# Uptake reporting protocol

## Metric definitions

| Metric | Operational definition | Permitted interpretation | Prohibited interpretation |
|---|---|---|---|
| Landing-page views | Counted canonical requests to the project landing page | Public interest in the landing page | Unique people or educators |
| Applet views | Counted canonical requests to an applet path | Applet pages opened | Algorithms completed or lessons learned |
| Engaged applet sessions | First qualifying in-app interaction per tab session | Sessions with at least one substantive interaction | Unique users, successful runs, or time on task |
| Resource opens | Clicks from measured pages to fixed resource links | Interest in a resource | Download completion or classroom use |
| Repository visits | Clicks from measured pages to the GitHub repository | Movement from product to source | Stars, clones, or code use |
| Campaign source | Allow-listed `ap_src` code | Aggregate acquisition channel | Person-level journey or inferred identity |
| GitHub stars/forks/clones | GitHub-reported repository metrics | Repository attention and reuse signals | Educational adoption |

## Reporting rules

1. State the exact date range, release version, and metric definition.
2. Report page views and engaged sessions separately.
3. Use “observed” rather than “users” unless a platform supplies a defensible unique-visitor measure and its limitations are stated.
4. Report coarse geography only at country level and suppress small cells in public research outputs.
5. Identify bot filtering, shared-device effects, blocked analytics, offline use, and missing campaign attribution as sources of uncertainty.
6. Preserve a private monthly aggregate export plus a checksum; do not publish low-count geographic cells or granular campaign data.
7. Triangulate telemetry with repository traffic, release downloads, educator feedback, and opt-in classroom reports.
8. Do not use public telemetry as evidence of learning effectiveness.

## Recommended future-writing language

> Between [date] and [date], the public v[version] site recorded [N] applet page views and [M] engaged applet sessions under the project’s aggregate, opt-out analytics definition. These counts exclude offline use and blocked analytics and should not be interpreted as unique learners or classrooms.
