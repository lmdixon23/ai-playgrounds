# Show HN readiness

## Pre-submit gate

- Use the direct live-site URL, not a campaign redirect.
- Verify the first interactive opens in one click on a signed-out desktop and phone browser.
- Confirm README, release, source, license, evidence, and privacy links are public.
- Keep the title descriptive and omit unsupported superlatives.
- Be available for the first two hours to answer technical questions.

## First-comment content

Explain the standalone-file architecture, why no framework was used, what the deterministic tests cover, which mechanisms are simplified, and why public analytics count only aggregate page/engagement signals. State that v1.0.0 remains immutable and v1.0.1 is a launch-hardening release.

## Anticipated critiques

1. **“This is twelve large HTML files.”** Correct; portability and offline inspectability were chosen over shared runtime dependencies. The public deployment is still generated deterministically.
2. **“The algorithms are simplified.”** Correct; every applet states its pedagogical scope and limitations. The product is not presented as a production solver or model.
3. **“Tests do not prove learning.”** Correct; software assurance and educational efficacy are explicitly separated.
4. **“Why bilingual?”** The suite was designed for an international-school context in which English and Simplified Chinese support materially lowers classroom friction.
5. **“Why analytics at all?”** Aggregate uptake signals help distinguish public interest from actual applet engagement while avoiding user-entered data, cookies, or cross-site profiles. Offline copies remain unmeasured.
