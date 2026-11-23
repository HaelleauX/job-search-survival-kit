# Market Evidence Watch: how it stays current

**Purpose:** detect newly published hiring and labor-market research and invite human review. The repo does not invent or automatically publish statistics.

## What it watches

- **Greenhouse:** [Recruiting benchmarks](https://www.greenhouse.com/recruiting-benchmarks), including *The Hire Standard*.
- **Ashby:** [Talent Trends reports](https://www.ashbyhq.com/talent-trends-report), useful for application and interviewing funnels.
- **Indeed Hiring Lab:** [Research and labor-market snapshots](https://hiringlab.indeed.com/), useful for job posting trends and wages. Their underlying data differs from Greenhouse's applicant pipeline data.
- **LinkedIn Economic Graph:** [Workforce reports](https://pulse.linkedin.com/research-and-trends/workforce-reports/), which should be read with its own definitions and platform biases.
- **U.S. Bureau of Labor Statistics:** [JOLTS releases](https://www.bls.gov/jlt/), the official survey of job openings, hires and separations. JOLTS is **not** a count of online applications or offers.

## Automated process

1. **Every Monday**, GitHub Actions checks these public official index pages. You can also click **Run workflow** to trigger a check.
2. It compares report-style links against the last committed baseline in `automation/seen-links.json`.
3. When it finds newly linked reports, it creates a dated review note in `evidence/inbox/` and proposes the changes in a **pull request**.
4. The maintainer reads the publisher's actual report and checks every proposed statistic before merging any changes to `evidence/hiring-market-numbers.md`.
5. If an official site is unavailable, the checker logs the failure and **retains** the previous baseline; it does not falsely conclude a report was deleted.

**Limits:** This is a link-discovery tool, not a database subscription. It may miss reports published without a link on the source landing page, JavaScript-rendered links, login-gated reports, or sites that block automated access. Monitor failures in GitHub Actions. It never bypasses paywalls or tries to access someone's LinkedIn account.

## How to activate in GitHub

1. Upload these files to a GitHub repository.
2. In **Settings → Actions → General**, allow Actions to create pull requests where supported; confirm `GITHUB_TOKEN` has repository content and pull-request write permissions.
3. Open **Actions → Watch hiring-market reports → Run workflow** for the first baseline scan. The first scan initializes the list of already visible links rather than calling everything a new report.
4. Review the baseline pull request. Merge it, then later checks flag genuinely new linked reports.
5. Keep `automation/sources.json` under review if a publisher changes the report landing page.

## Publishing checklist for a report statistic

- [ ] Publisher and original URL verified.
- [ ] Report title, publication date, sample period and geography documented.
- [ ] Sample size and *who is represented* recorded.
- [ ] Exact numerator and denominator understood. E.g., "hire conversion of job board applicants" ≠ "chance an individual gets hired."
- [ ] Methodology and conflicts of interest explained.
- [ ] Any comparison uses matching populations, definitions and time periods, or warns when they differ.
- [ ] Exact page/table cited (link if available).
- [ ] Counterclaims or contradictory evidence handled fairly.
- [ ] Dated summary kept short; don't paste full copyrighted reports.

People deserve reliable information. A scheduled hallucination would rather defeat the point.
