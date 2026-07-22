# Release checklist

## Automated checks

Run from the repository root:

```bash
python tools/release_check.py --json release-evidence/release-check.json
python tools/browser_qa.py --no-screenshots
python tools/browser_qa.py --screenshots
```

The source checker verifies the twelve applets, public routes, bilingual controls, featured experiments, scenario galleries, four learning modes, shareable state links, local response packets, text-state support, metadata, public repository boundaries, and JavaScript syntax.

The browser matrix checks every public page at mobile, tablet, and desktop widths. It also exercises language switching, learning-mode tabs, scenario URLs, live regions, and horizontal-overflow detection.

## Manual checks

Before a tagged release:

1. Use a real phone to inspect the landing page and at least five applets.
2. Complete a keyboard-only pass on the same pages.
3. Test the site with a screen reader.
4. Print the Teacher Pack, student lab sheet, release notes, and several applet response packets.
5. Verify exact experiment links in a second browser.
6. Test the deployed site with a hard refresh and analytics opt-out parameters.
7. Confirm that the public package contains no `_local`, generated evidence, or internal workflow records.

## Manual screen-reader walkthrough

A manual screen-reader walkthrough means opening representative pages with a real assistive-technology reader, then navigating without a mouse. It checks whether the page is understandable when the visual layout is replaced by spoken structure.

Test at least the homepage, Pathfinding, Bayes Rule, K-Means, Q-Learning, Teacher Pack, and Student Lab Packet.

1. Use NVDA with Firefox or Chrome on Windows, or VoiceOver with Safari on macOS/iPhone.
2. Navigate by headings and landmarks. Confirm the order matches the visual page.
3. Tab through controls. Confirm every control has a useful spoken name and no keyboard trap.
4. Change a slider, scenario, or algorithm. Confirm the live status announces the meaningful result without repeating continuously.
5. Switch English and Chinese. Confirm labels and page language update coherently.
6. Open each learning mode. Confirm hidden panels are not read as visible content.
7. Check the text-state summary against the current visual state.
8. Record confusing labels, missing announcements, repeated content, and focus loss as defects.

Passing this walkthrough supports a statement that the pages were manually tested with a named screen reader. It does not by itself establish WCAG conformance.
