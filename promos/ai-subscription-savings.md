# AI subscription savings: don't pay if you don't have to

**Last manually reviewed: November 23, 2026.** This is a practical guide, not a promise of any deal. Eligibility changes. A deal that appeared in somebody else's PayPal app may not be in yours. **You can complete all six Career OS workflows using free AI plans (subject to their usage limits).**

## Where to look first (free, 2-minute check)

| Service | Legitimate place to check | What to verify |
|---|---|---|
| ChatGPT Plus | Your ChatGPT account offers, the [official promotion rules](https://help.openai.com/en/articles/10492689-chatgpt-plus-promotions-and-referrals), and any **targeted offer in your PayPal account** | New/existing subscriber eligibility, checkout channel, whether it is cashback or a reduced price, renewal date |
| Perplexity Pro | [Perplexity's official partner promotion rules](https://www.perplexity.ai/help-center/en/articles/11385821-partner-promotions-and-referral-programs), verified partner apps, and [Education Pro](https://www.perplexity.ai/help-center/en/articles/12590157-what-is-education-pro) | Partner-specific eligibility, whether a payment method is required, cancellation method |
| Claude Pro | [Claude's official individual-plan help](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan) and offers shown in your account or on official channels | No permanent standard individual discount; time-limited deals may appear; prior subscriber and app-store restrictions |
| PayPal / other payment partners | Your **own logged-in** offers or rewards dashboard, plus authentic vendor announcements | The exact payment instrument, enrollment link, cashback cap, payout timeline, and whether the offer was saved/activated |

### Evidence snapshot: November 23, 2026

- **ChatGPT Plus via PayPal, reported:** A publicly shared U.S. account-targeted promotion describes **50% cashback for up to six monthly payments**, not necessarily a 50%-off checkout price. The Reddit report says $20 charged and $10 paid back for each eligible payment, and reports a December 31, 2026 or enrollment-cap ending. **Not independently confirmed by public PayPal terms; check your personal PayPal offer before switching billing.** [Community report](https://www.reddit.com/r/ChatGPT/comments/1x0sjwm/us_only_paypal_offering_50_cashback_on_plus_tier/). Individual users have reported success, but visibility and eligibility differ.
- **Perplexity Education Pro, official:** $10/month for **verified students and educators**, billed on `perplexity.ai` only. Cannot be applied to PayPal, Google Play or App Store billing. [Official help article](https://www.perplexity.ai/help-center/en/articles/12590157-what-is-education-pro).
- **Perplexity partner promotions, official process:** Perplexity says it regularly issues codes through authorized partners. Promotions commonly require an eligible payment method and renew unless canceled. The older 'Give a month, Get a month' program **ended October 6, 2025**, and Comet Referral **ended November 6, 2025**. Don't recommend old referral hacks. [Official help article](https://www.perplexity.ai/help-center/en/articles/11385821-partner-promotions-and-referral-programs).
- **Claude, official policy:** No standard discounted pricing for individual Pro/Max/Ultra, but Anthropic occasionally announces limited-time promotions. Its eligibility page notes that active/prior paid users may be excluded and app-store subscriptions may not qualify. **No verified generally available Claude Pro promotional price found during this review.** [Pricing/promotions](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan) | [Eligibility](https://support.claude.com/en/articles/11107691-why-is-a-coupon-or-promotion-not-available-for-my-account).

**Expired example, not a current recommendation:** PayPal announced a Perplexity Pro 12-month free offer in 2025. Historical offers are useful for knowing which accounts to inspect, not evidence that the same deal is redeemable today.

## The checklist before you click Subscribe

- [ ] **Is it real?** Open the offer from the official provider/partner app or an authenticated official domain. Avoid resale codes, unsolicited DMs, and login links from strangers.
- [ ] **Who qualifies?** Existing or new subscribers; region, age, student, educator, card, account tenure, other exclusions.
- [ ] **What am I actually paying?** Discount at checkout, free trial, statement credit, or *cashback after full-price billing*? Tax? How many qualifying monthly payments?
- [ ] **Do I need to activate it first?** Some targeted offers require saving the offer and using a special checkout path. Paying with a branded debit card alone may not satisfy that condition.
- [ ] **Are my accounts compatible?** Apple, Google Play, and direct web billing are separate subscriptions. Cancel old-platform billing and wait until that period ends before resubscribing to avoid duplicate charges.
- [ ] **Proof:** Screenshot the exact terms, eligible checkout path, receipt and reward confirmation. Do not post personal account details publicly.
- [ ] **Calendar:** Record the first full-price renewal or trial end date. Set reminders **seven days and three days beforehand**, then confirm cancellation before the provider's deadline. Some free trials end access immediately when canceled.
- [ ] **Track cashback:** Add a separate reminder to verify that the promised credit was actually issued. A claim of '50% cashback' is not a 50% saving until the cash reaches you.

**Calendar-event title you can copy:** `Check / cancel [AI SERVICE] promotion before renewal — [DATE]`.

### If you're switching a ChatGPT subscription from Google Play to direct billing

OpenAI recommends **canceling the Google Play subscription first and waiting for that paid period to end** before subscribing through chatgpt.com. Otherwise you could be billed twice. Follow the partner-specific promo flow only after checking eligibility. [Official billing guidance](https://help.openai.com/en/articles/20001043-how-do-i-avoid-being-charged-twice-if-i-subscribe-to-chatgpt-on-ios-android-and-the-web).

### Please do not pay just to use the toolkit

Use a free plan first. Upgrade only if you are hitting a real limit that materially affects the job search. Even a genuinely good discount is money you didn't need to spend if the free tier does the work.

## Contributing a newly found deal

When filing an issue, share only: provider, official URL, region, offer type, price/credit, eligibility, end date if known, date checked, and whether it appeared only inside your account. **Never share a referral code that is private, single-use, or not authorized for redistribution. Never share payment details or screenshots with personal information.**

## How the daily watcher works

[AI promo watcher](../automation/watch_ai_promos.py) monitors the configured public official pages [listed here](../automation/ai_promo_sources.json) for linked promotions and meaningful changes to promotion-related page text. On GitHub, [the scheduled workflow](../.github/workflows/ai-subscription-promo-watch.yml) creates a **review pull request** for detected changes. **It cannot log into PayPal, inspect personalized discounts, verify checkout prices, or claim a deal is live.** The first run creates a baseline; changes begin being flagged on subsequent runs. No personal account data is sent anywhere.
