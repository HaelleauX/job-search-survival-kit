# Decode the job (recruiter-side thinking, applicant-side advantage)

**You need:** the complete job description. **You get:** a decision-oriented breakdown of requirements, likely business goals, and possible screening questions. This is an **inference**, not the employer's secret scorecard.

## Copy this prompt

```text
Act as an evidence-focused career analyst. I am a job seeker. Decode the following job posting so I can decide whether it is worth my time and prepare an accurate application.

JOB POSTING:
[PASTE JOB DESCRIPTION]

RULES:
- Separate (A) requirements the employer explicitly states, (B) reasonable hypotheses about its priorities, and (C) unanswered questions.
- Never claim access to an employer's internal screening algorithm, private interview guide, or ATS score.
- Flag vague or contradictory requirements. Do not invent qualifications.
- Evaluate requirements based on job relevance, not protected personal characteristics.

RETURN ONLY:
1. In one sentence: the business problem this hire probably addresses. Label it inferred.
2. The 5 most important stated requirements, with short quotations/paraphrases from the posting.
3. The 3 most important preferred requirements.
4. Up to 5 likely interview themes, labeled hypotheses.
5. Any unclear requirements or legitimate dealbreakers to verify before applying.
6. An honest go / investigate / skip checklist I can use once I paste my background.
Keep the output under 500 words.
```

**Now act:** if the role looks viable, go to [Reality-check my fit](02-fit-and-gaps.md).
