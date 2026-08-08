# Analytics and privacy specification

**Scope:** AI Playgrounds public pages hosted at `lmdixon23.github.io`. **Release:** v1.0.1. **Analytics endpoint:** `https://lmdixon23.goatcounter.com/count`.

## Design decision

The project uses a deliberately small aggregate measurement layer so public interest can be described without building learner profiles. Every public HTML page contains the same first-party inline wrapper. The wrapper sends a 1x1 image request directly to the GoatCounter `/count` endpoint; it does **not** load GoatCounter's JavaScript or any other third-party runtime script. It runs only on the canonical GitHub Pages host. Downloaded files, `file://` use, localhost, mirrors, and school intranets send no project analytics.

## Signals sent by the project code

1. The canonical page path, without query strings or fragments.
2. Synthetic aggregate paths for an applet launch, resource link, repository link, first substantive applet interaction in a tab, and an allow-listed campaign source.
3. No referrer URL is sent by the project code: each analytics image uses `referrerPolicy = "no-referrer"`.

The “first substantive interaction” is an **engaged applet session**, not an algorithm run, learner, classroom, completion, or learning outcome. It is deduplicated with session storage within that browser tab and therefore cannot be interpreted as a person count.

## Signals explicitly excluded from the request payload

The project code does not transmit names, email addresses, school identifiers, free text, experiment values, model parameters, saved states, answers, grades, query strings, fragments, referrer URLs, exact coordinates, keystrokes, mouse trajectories, or time-on-task recordings. It does not set analytics cookies or a project tracking identifier.

A network request necessarily exposes ordinary connection metadata such as an IP address and User-Agent to the receiving server. GoatCounter's published privacy documentation states that hosted analytics store aggregate tables rather than IP addresses or full User-Agent strings; its session mechanism temporarily maps site + IP + User-Agent in memory for up to eight hours. Browser, operating-system, language, and country aggregates can be disabled in GoatCounter settings. The project's own wrapper also sends no screen-width field.

## Controls

Analytics is disabled before any request is sent when:

- Global Privacy Control is enabled;
- Do Not Track is enabled;
- `?analytics=off` is present;
- the local opt-out control has stored `ai-playgrounds-analytics=off`; or
- the page is not on `lmdixon23.github.io`.

Campaign attribution uses only the custom `ap_src` parameter and a fixed allow-list, for example `?ap_src=linkedin`. Arbitrary values are ignored. Standard advertising-style campaign parameters are neither required nor parsed by the project wrapper.

## Recommended GoatCounter account configuration

- Keep **individual pageviews disabled**.
- Keep the analytics dashboard private.
- Disable browser, operating-system, language, and screen-width collection unless a specific maintenance question requires them.
- Keep only country-level location if geographic uptake is genuinely useful, and suppress low-count country cells in public reports.
- Retain sessions if deduplicated aggregate visits are useful; disclose that GoatCounter's session mechanism temporarily uses IP + User-Agent in memory.
- Never create person-specific, student-specific, classroom-specific, or school-specific campaign codes.

## Governance

- Review this specification before adding any event.
- Never encode user-entered content in an event path.
- Never claim unique people, students, classrooms, or learning gains from these data.
- Keep only the granularity required for aggregate uptake reporting.
- Record material analytics changes in the changelog and research provenance log.
- Treat legal compliance as jurisdiction-specific; this document describes the technical design rather than a universal legal conclusion.

See [Analytics operator checklist](ANALYTICS_OPERATOR_CHECKLIST.md) for live payload inspection, duplicate-count checks, retention review, and reporting discipline.
