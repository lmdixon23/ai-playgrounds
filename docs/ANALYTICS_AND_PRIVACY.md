# Analytics and privacy

AI Playgrounds has no learner accounts, student-upload endpoint, assignment-submission backend, or grading service. The following describes the project's technical data boundary; it is not a claim of universal legal compliance.

## Learner responses and experiment state

Answers remain in the learner's browser unless deliberately copied, exported, printed, or submitted through the teacher's usual classroom system. Local draft storage is not a cloud backup. Copying an HTML file does not copy saved answers; preserve work before clearing browser data or changing devices.

Supported share links can contain experiment configurations, but not worksheet responses. A local experiment URL is specific to the device; distribute the standalone HTML itself for offline teaching. Do not put private information in formulas, experiment labels, or links intended for sharing.

## Optional public-site measurement

The public website can send coarse usage signals to GoatCounter using a first-party wrapper and image requests. It does not require a third-party runtime script. The wrapper permits measurement only on the canonical public host. Standalone downloads opened offline, localhost, and noncanonical copies send no project analytics.

The project request payload is limited to canonical page paths without arbitrary query strings or fragments, page titles, fixed event categories, and allow-listed campaign categories. Event categories can describe opening a lab or a resource, following a repository link, or the first substantive applet interaction in a tab session.

The project code excludes learner answers, Quick Assign responses, names, email addresses, school identifiers, free text, grades, experiment values, saved state, arbitrary URL parameters, general referrer URLs, keystrokes, and time-on-task recordings from analytics payloads. It does not set analytics cookies or a project tracking identifier. Analytics image requests use a no-referrer policy.

A network request necessarily exposes ordinary connection metadata, such as an IP address and User-Agent, to the receiving service. Excluding those fields from an explicit payload is not the same as making a network request anonymous.

## Controls

The measurement wrapper sends no request when:

- Global Privacy Control is enabled;
- Do Not Track is enabled;
- the page URL includes `?analytics=off`;
- the homepage privacy control has stored the local opt-out; or
- the page is not on the canonical public host.

Use the [homepage privacy controls](https://lmdixon23.github.io/ai-playgrounds/) or open the [site with analytics disabled](https://lmdixon23.github.io/ai-playgrounds/?analytics=off). A browser-local choice applies to that browser, not automatically to other devices.

## Evidence and reporting

Page views and interaction events are not unique people, students, classes, completed assignments, or learning outcomes. A first interaction in a browser tab does not establish sustained engagement or learning. Human validation remains a separate evidence requirement; see [Quality](../QUALITY.md).

For a defect, follow [Contributing](../CONTRIBUTING.md). For a sensitive disclosure, follow [Security](../SECURITY.md). Do not include raw student records or credentials.
