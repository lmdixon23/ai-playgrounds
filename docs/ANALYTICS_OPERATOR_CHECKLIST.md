# Analytics operator checklist

## Before launch

- Confirm the GoatCounter site endpoint belongs to the project owner and uses a strong, unique account credential.
- Keep the detailed analytics dashboard private unless a disclosure review confirms that low-count geography or other detail is safe to disclose.
- Build the exact release artifact and verify **every public HTML page** contains exactly one AI Playgrounds analytics wrapper, including generated applets and Activity Pack pages.
- Verify the landing page, one inherited applet, Lab 13, Lab 14, one support page, and one Activity Pack each produce one page view—not two.
- Verify page-view payloads use the canonical path and a nonempty page title; canonical `/index.html` aliases must not fragment the same page into separate dashboard rows.
- Verify synthetic applet/resource/outbound/engaged interactions are sent as GoatCounter events with `e=1`, not ordinary page views.
- Verify an allow-listed `?ap_src=linkedin`-style source produces GoatCounter campaign query data and an arbitrary `ap_src` value produces none.
- Verify `?analytics=off`, Global Privacy Control, Do Not Track, localhost, `file://`, and non-canonical mirrors produce no analytics request.
- Verify arbitrary query values, hashes, experiment controls, saved states, worksheet answers, free text, and learner identifiers are absent from analytics requests.
- Verify the project still sends no general referrer URL and does not load third-party analytics JavaScript.

## After publication

- Open the live landing page and one newly generated page in a clean browser and confirm one expected page-view request per page.
- Confirm GoatCounter shows the new page titles instead of `(no title)` for newly counted traffic.
- Confirm a controlled allow-listed campaign link appears under Campaigns rather than only as a synthetic page path.
- Confirm a controlled interaction appears as an event and does not inflate the ordinary page-path total.
- Do not infer that historic rows collected under earlier instrumentation have been retroactively reclassified.

## Monthly

- Export only aggregates needed for the uptake protocol.
- Record release, date range, metric definitions, analytics-code version, provider-setting changes, and export checksum.
- Compare actual page visits with event counts, engaged tab sessions, repository traffic, release downloads, and educator feedback.
- Investigate sudden spikes for bots or embeds before reporting.
- Suppress low-count country/referrer cells in public writing.
- Treat a dashboard total as a path/session metric under GoatCounter's definitions, not as a unique-person count.

## Quarterly

- Review every custom event against the data-minimization rule.
- Delete detailed data that is no longer needed for the stated uptake purpose.
- Confirm privacy copy still matches the implementation and GoatCounter account configuration.
- Reassess whether browser, operating-system, language, location, and screen-size aggregates remain necessary; disable anything that does not serve a defined maintenance or adoption question.
- Reassess whether analytics remains proportionate; remove it if it no longer serves a defined research, maintenance, or adoption purpose.

## Claim discipline

Never convert page views, visits, engaged tab sessions, campaign counts, or synthetic events into “students,” “teachers,” “classrooms,” “runs,” “learning time,” or “learning gains.”
