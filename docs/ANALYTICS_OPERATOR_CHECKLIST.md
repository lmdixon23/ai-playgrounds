# Analytics operator checklist

## Before launch

- Confirm the GoatCounter site endpoint belongs to the project owner and uses a strong, unique account credential.
- Keep the detailed analytics dashboard private unless a disclosure review confirms that referrers and low-count geographic cells are safe.
- Verify the landing page, one applet, one resource page, and the portfolio case study each produce one page view—not two.
- Verify `?analytics=off`, Global Privacy Control, Do Not Track, localhost, `file://`, and non-canonical mirrors produce no analytics request.
- Verify arbitrary query values are absent from page paths and event names.
- Verify only allow-listed `ap_src` values create campaign events.
- Inspect network payloads to confirm experiment controls, saved states, free text, and hash fragments are not transmitted.

## Monthly

- Export only aggregates needed for the uptake protocol.
- Record release, date range, metric definitions, filter changes, and export checksum.
- Compare page views with engaged sessions, repository traffic, release downloads, and educator feedback.
- Investigate sudden spikes for bots or embeds before reporting.
- Suppress low-count country/referrer cells in public writing.

## Quarterly

- Review every custom event against the data-minimization rule.
- Delete detailed data that is no longer needed for the stated uptake purpose.
- Confirm privacy copy still matches the implementation and analytics provider configuration.
- Reassess whether analytics remains proportionate; remove it if it no longer serves a defined research, maintenance, or adoption purpose.

## Claim discipline

Never convert page views, engaged tab sessions, or campaign events into “students,” “teachers,” “classrooms,” “runs,” “learning time,” or “learning gains.”
