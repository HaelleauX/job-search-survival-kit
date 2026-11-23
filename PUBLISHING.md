# Maintainer launch checklist

## Create the dedicated repository

The GitHub account owner must create a **new public repository** named `job-search-survival-kit`
(or choose another unused name) under the intended account. Do not reuse an existing
professional or personal project repository. **Do not initialize** the new repository
with a README, license, or `.gitignore`, because those are included here.

Upload **the contents of this folder**, including `.github/workflows/` (hidden directories
must be included), into the repository's root.

**No-code option:** Open [GitHub's new-repository page](https://github.com/new),
choose the repository name and **Public**, and leave *Add a README*, *.gitignore*,
and *license* unchecked. After creating it, use **uploading an existing file**
(or **Add file → Upload files**) and upload the extracted release files. Before
committing, confirm GitHub shows the directory paths for `prompts/`, `guides/`,
`automation/`, `tests/`, and `.github/workflows/`. If your browser will not preserve
folder structures, use the GitHub Desktop app or the command-line method below.
Do not upload the ZIP as one file; GitHub does not automatically unpack it into
a usable repository.

**Command-line option:** From the extracted release folder:

```bash
git init
git add .
git commit -m "Launch Career OS public beta"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/job-search-survival-kit.git
git push -u origin main
```

This repository has no developer dependencies for reading its content. Python 3.12+
is needed only for automated watchers and their tests.

## Enable watchers with review safeguards

1. Open repository **Settings → Actions → General**. Review permitted actions, repository
   workflow permissions, and whether GitHub Actions is enabled for this repository.
2. If you want the watchers to create review pull requests, configure GitHub Actions
   settings to permit read/write repository access and workflow-created pull requests
   where the platform offers those controls. Don't add a personal access token unless
   needed; the workflows use the scoped built-in `GITHUB_TOKEN`.
3. Open **Actions** and manually trigger each watcher once. **First run creates a
   baseline**, not a list of current verified deals. Check the run logs and any PR.
4. Review detected links and offer language manually. Check the source's original
   methodology/terms before merging updates. Merging the watched state files alone
   does not publish any new statistics as fact.
5. Periodically review third-party GitHub Actions versions and official source URLs.

GitHub scheduled workflows can be delayed or disabled after repository inactivity.
Failures and monitoring gaps must not be described as proof that no new offers exist.

## Beta acceptance criteria

- [ ] The [one-job quickstart](START_HERE.md) makes sense without GitHub experience.
- [ ] No confidential resume or private account data is committed.
- [ ] No paid-program template or derived material is committed.
- [ ] All relative Markdown links work.
- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] At least three **real volunteer** job seekers have tried the workflow **without coaching**.
- [ ] Accessibility and mobile readability reviewed.
- [ ] Watchers are observed succeeding on GitHub, and PR permissions are verified.

**Release distinction:** Automated tests and fictional walkthroughs are prelaunch checks.
They are not substitutes for actual independent user testing. The public beta can be
labeled "early access" until user testing is complete; don't claim proven outcomes.