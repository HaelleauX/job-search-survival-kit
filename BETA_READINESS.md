# Beta readiness and testing status

**Status: prepared for public beta; not yet published.** Do not mistake this
file for a user testimonial, an effectiveness study, or proof that job outcomes
improve. Last local check: November 23, 2026.

## Scope

- One-job quickstart: a single copy-and-paste prompt for fit, evidence, resume edits,
  outreach, and interview preparation.
- Six optional focused prompts, LinkedIn and AI deal guides, Greenhouse metrics.
- Two review-first GitHub Actions workflows. Scheduling starts **only after** a
  repository is created, Actions is enabled, and a first run succeeds.
- Original sources only; paid-coaching program files excluded.

## Fictional scenario walkthroughs: design checks, not human usability tests

These are design review cases created to challenge the *instructions* and expected
outputs. We did not recruit people or run a controlled AI-model evaluation.

| Fictional persona | Main test | Acceptable behavior | Failure to watch for |
| --- | --- | --- | --- |
| A recent graduate without a resume | Missing work history | Ask for activities, projects, and evidence; avoid declaring unsupported experience | Inventing a job or claiming full fit |
| A library coordinator transitioning to customer operations | Transferable skills and a work-model conflict | Note coordination evidence, missing Salesforce, and verify office days | Treating a preferred skill as a hard requirement or inventing CRM experience |
| An experienced service manager with no tracked metrics | Seniority without numbers | Surface credible qualitative outcomes and [VERIFY] prompts | Fabricating ARR, growth percentages, or ATS scores |

The fictional library-coordinator walkthrough is shown in
[the example](examples/FICTIONAL-EXAMPLE.md).

## Actual prelaunch checks

- [x] Repository file and privacy scan for obvious names, private Drive links, and
      common restricted-workbook filenames. **This cannot prove all derivative rights.**
- [x] Independent source policy and private exclusion register separated.
- [x] A beginner-facing one-job workflow and fictional walkthrough supplied.
- [x] Original content and software license files supplied.
- [x] Local Python tests for source checks, source-watch parsing, offer-watch parsing,
      file completeness and relative links.
- [ ] Three real volunteers independently complete the quickstart.
- [ ] Human review of clarity/accessibility on phones.
- [ ] Dedicated repository created and GitHub Actions test-run verified.
- [ ] First public beta release and announcement.

## What to collect from a volunteer (without collecting their resume)

Ask the volunteer to use the [quickstart](START_HERE.md) privately and answer:

1. Could you begin without help? (yes/no)
2. At what exact instruction did you get stuck, if anywhere?
3. Did the output make a specific application decision/action easier?
4. Did the assistant invent anything or make a claim it couldn't support?
5. Would you use it again, and why?

Keep feedback anonymous unless a tester explicitly consents to being named.
Do not ask people to share their full resumes, salary records, or job-search history
for a usability test.