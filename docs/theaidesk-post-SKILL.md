---
name: "theaidesk-post"
description: "Research, write, image, and post daily content for the AI-news brand @theaidesk.io (Instagram, Threads) / @theaideskio (X): verifying claims, generating brand-system images, drafting/scheduling to Buffer, and logging to the Notion Content Calendar. Use this whenever Kush asks for a regular daily AI-news post, or pastes in a rough AI news digest / roundup for an 'AI Daily Signal' post, or mentions theaidesk.io content, Buffer drafts for the AI desk brand, or the Content Calendar. Trigger even if he doesn't say the word 'skill' — a pasted block of AI news bullet points around late morning Sydney time is very likely a Signal-mode request. Oct 2026 flow: commit images to the repo, self-merge the PR, then schedule Buffer from main raw URLs; lowercase hashtags; one short bulleted X/Threads post; mode buffer-from-main."
---

# The AI Desk — daily content pipeline

One pipeline, three entry points. All produce the same deliverable — a verified, brand-voice post, logged to Notion and staged in Buffer — they differ in where the story comes from, which platforms it hits, and which cadence slot it lands in.

**Mode A — research.** Used by the daily scheduled task. Claude finds today's AI news itself, picks two well-sourced stories, generates the images, commits them to the GitHub repo, opens and squash-merges its own PR, and only then posts them to Buffer as `Regular`-tagged, Day-numbered, three-platform posts (images on all three) in the existing 11:30 UTC / 20:00 UTC rhythm. See Step 4b for the git flow. Breaking is never run from this path.

**Mode B — signal.** Ad-hoc, triggered when Kush pastes a rough multi-story digest (usually ~11am Sydney). Claude verifies every claim, reframes it into brand voice, and posts it as an `AI Daily Signal`-tagged post at 1:30pm Sydney local time.

**Mode C — breaking.** Invoked as `Skill(theaidesk-post, args: {mode: "breaking"})` by a scheduled task that fires several times a day. Claude scans for genuinely new stories inside a hard 48-hour window and, if one clears the bar, ships a `Breaking`-tagged post to **X and Threads only, text only, never Instagram, never images**. Most cycles find nothing, and that is the healthy outcome — see Step 7 on staying silent.

**Mode D — buffer-from-main.** Invoked as `Skill(theaidesk-post, args: {mode: "buffer-from-main", date: "YYYY-MM-DD", posts: ["post-1", ...]})` or with `pr: <number>`. No research and no image generation: it reads captions and manifests from `posts/<date>/<post>/` on `main` and schedules Buffer from the existing raw image URLs. Use it for post-only runs and for re-scheduling assets that are already merged. It still checks Buffer and Notion for the same story first and never double-posts. See Step 5.

Figure out which mode from context: an explicit `mode: "breaking"` arg is Breaking mode. A pasted block of loose news bullets with figures and story fragments is Signal mode. A bare "run today's post" / the daily scheduled trigger firing is Research mode.

## Why this exists

Buffer's API has no image-upload mutation — every asset needs a URL its servers can fetch, and there's no such host available from this sandbox. That single constraint shapes almost every mechanical decision below (drafting Instagram instead of scheduling it, sending images as files instead of attaching them). Don't try to route around it — it's been tested and confirmed, not assumed.

## Step 1 — Get the story

**Research mode:** query the Content Calendar (below) for the highest Day number and recent Companies, then web-search today's real AI news, checking primary sources. Prefer stories that concretely affect a non-technical reader's job or wallet over pure hype.

**Pick TWO stories, not one.** Kush asked for this on 29 Aug 2026 and had to ask again on 2 Sep
when a run shipped a single post. Two is the floor for a research run: two separate posts, two
consecutive Day numbers, the 11:30 UTC and 20:00 UTC slots. Go to three or four only when the
day genuinely holds that many distinct stories; four is the hard ceiling, because he attaches
every image by hand and each post costs him three uploads. Pick stories that stand apart from
each other, and rotate companies — three posts about the same lab in a week reads as a fan
account, not a desk.

**Rotation is a tiebreaker, never a veto.** Kush corrected this on 7 Sep 2026 after a Breaking
run declined a clean, primary-sourced OpenAI story purely because OpenAI had run twice the day
before. When two stories both clear the sourcing bar, take the one that rotates. When only one
clears it, run it whatever the logo says. The rule exists to stop *filler* — thin stories about
a favourite lab, padded in to fill a slot — not to make the desk skip real news because the
same company made news yesterday. A news desk does not spike a story for that reason.
What stays hard: the freshness ceiling, the sourcing bar, and never running the same *story* twice.

**Breaking mode:** query the Content Calendar for the highest Day number and the stories and
companies of the last day or two, then scan wide. Two hard gates, then a judgement call.

*Gate 1 — freshness.* Nothing published more than 48 hours ago ships. No exceptions, however
well-sourced. Compute the window from the actual clock (`date -u`), not from the cycle's nominal
fire time, because a delayed or resumed run can be hours late.

*Gate 2 — sourcing.* **A primary source is not the same thing as a news site, and in AI it
usually isn't one.** All of these are primary and all of them are fair game, generally *earlier*
than the news outlets, which is exactly what this mode wants:

- a company blog, newsroom post, or release notes
- a model card, system card, or technical report
- a GitHub release, changelog, or commit
- docs, pricing, rate-limit, deprecation and status pages
- an arXiv paper or a lab's own technical write-up
- a regulatory filing, court document, or government release
- a company exec, founder or researcher posting **about their own product or their own work**

Day 39 already ran this way, sourced to a Google exec's X post plus support docs, with the
thinness of that sourcing stated in the copy. That is the pattern.

*Where an influencer sits.* A commentator with a big following talking about **someone else's**
product is **not** a source, they are a lead. Follow the lead to the underlying artifact, verify
that, and cite that — the same way aggregator front pages get used. Never report an influencer's
characterisation as the story itself. The desk's whole voice rests on sourcing claims and
separating a vendor's number from a verified one; one bad call there costs more trust than a
fortnight of quiet slots ever buys.

The real exception: when the influencer **is** the primary source — they built the thing, ran
the benchmark, got hit by the outage, or received the email — they are a named first-hand
account. That is postable, cited by name, with the caveat stated plainly that it is one person's
report and nobody else has confirmed it yet.

*The prefix bar.* `BREAKING:` and `JUST IN:` require a primary source from the list above. A
story that is fresh and real but rests on thinner sourcing still runs, just in honest plain text
with the sourcing named and its limits stated. Never buy a prefix with sourcing you don't have.

*If the queue looks thin, widen the aperture, never lower the bar.* Announcements are the rarest
source type on that list. Pricing and rate-limit changes, changelogs, model deprecations, docs
updates, open-source drops, benchmark results and regulatory filings happen most days, are fully
primary, and are the actual answer to a thin queue — along with the desks that need no breaking
news at all (`Explainer`, `The Number`, `Free Tier`, `Ask the Desk`). Volume comes from looking
in more places, not from trusting weaker ones.

**Signal mode:** Kush's pasted text is a draft, not a source. Before writing anything, verify every factual claim in it with web search against primary or reputable secondary sources — funding rounds, price changes, outages, security incidents, all of it. Drop anything you can't corroborate rather than publishing it anyway (past instance: a "vibe-coding minigame" and some vague "agent harness repos" bullets had no findable source and were cut). If a claim is directionally true but the framing is loaded or mis-attributed, fix the framing — don't just parrot it. A past example: the source draft said an "OpenAI agent under testing escaped its sandbox and breached Hugging Face infrastructure," which was accurate, but needed one added distinction to be responsible — that this was OpenAI's own internal red-teaming going further than intended, not an external attacker or a customer's deployed agent. Getting attribution like that right is the entire point of a caveat tweet; don't skip it for expediency. Strip out anything that isn't caption content, like image-prompt notes the source draft included for itself.

## Step 2 — Read the brand context

Fetch these Notion pages fresh each run rather than relying on memory — they get edited:

- **Brand System** (page `3c4c18505d1281c29709fe0593598103`) — voice rules: lead with what changed, source every claim, separate a company's own number from an independently verified one, no hype adjectives, say when something doesn't matter.
- **X Threads** (page `3c4c18505d1281a1ac90d94502c5528d`) — thread structure: tweet 1 = the news, complete, no teaser (people quote it standalone); 2–3 = mechanism; 4 = the caveat, vendor claim vs. verified — this is the tweet that earns trust; 5 = practical read, including "nothing to do yet" if that's honest; last = source + handle. Threads mirrors this, slightly less newsy tone allowed, posts can run longer.
- **Image Generation Recipe** (page `3c5c18505d12817493dae24e5691f9cd`) — the full visual system: canvas sizes, company accent colors, fonts, handle rules, and the reference `build_html()` used in `scripts/build.py` here. If the page has changed the recipe since `scripts/build.py` was bundled, prefer the page — update the script to match rather than silently diverging from brand.

## Step 3 — Write the copy

Instagram caption (longer-form, sourced, structured like the brand voice examples on the
Content Calendar template page below), X, and Threads.

**Breaking mode writes X and Threads only** — no Instagram caption, because Breaking posts carry
no image and Instagram cannot be scheduled without one. Everything else in this step still
applies, and the caveat discipline applies double: when every figure in a story is the company's
own internal measurement, say so in the post rather than repeating the number as though someone
had checked it.

**X and Threads: one short post, the same text, in bullets.** Kush set this on 4 Oct 2026, building on the earlier "keep it short" asks (29 Aug, 1 Sep, 3 Sep). Each of X and Threads gets exactly **one single post, never a second post and never a thread**, and X and Threads carry the **same text** (only the follow-line handle differs: **X is `@theaideskio`, no dot; Threads and Instagram are `@theaidesk.io`**, never swap them). Keep it as short as the Breaking / JUST IN posts, but readable: no long paragraph. Layout:

```
<one lead line: what changed, plain words>

• <key fact>
• <key fact, or the mechanism>
• <the caveat: vendor claim vs verified, or what we could not confirm>

Source: <name, date>

Follow @theaideskio for more AI updates!
```

Two to three bullets, one short line each. The last bullet is the trust bullet (own number vs verified, one study vs a verdict, or "nothing to do yet"). If it runs long, cut a bullet or tighten the words; never spill into a second post. A digest with more than one story is still a reason for a second Day number, not a longer post.

**Length is not optional to check by eye.** Count characters in Python before posting:
```python
assert len(x_text) <= 280, f"X post is {len(x_text)} chars"
assert len(threads_text) <= 500, f"Threads post is {len(threads_text)} chars"
```
X must stay at or under 280 characters (this account isn't confirmed to have extended limits), counted over the whole post including bullets, Source, Follow line and any hashtags. A post that is 1 character over gets rejected or truncated later; catch it now.

**Hashtags (revised 4 Oct 2026).** All hashtags are **always all lowercase, never TitleCase or camelCase**: write `#openai`, `#theaidesk`, `#chatgptpro`, `#aimode`, not `#OpenAI`, `#TheAIDesk`, `#ChatGPTPro`. Check every hashtag line for capitals before posting.
- **Instagram:** at least 5 hashtags, on their own line at the very end after the Follow line, with a blank line before: one or two broad tags (`#ai`, `#technews`, `#artificialintelligence`), one or two story-specific ones (`#openai`, `#anthropic`), and a brand tag (`#theaidesk`, or `#aidailysignal` for Signal mode). Five is a floor; never pad with tags that don't fit the story.
- **Threads: no hashtags at all.**
- **X:** same text as Threads. A lowercase hashtag line is optional and only when it fits inside the 280 characters; never trade a bullet or the Source line for hashtags.

**Instagram layout.** The caption keeps the warmer, fuller register, but uses short paragraphs and `•` bullets for the key facts and the caveat instead of one dense block, then the Source line, the Follow line and the hashtag line, each separated by a blank line.

**Never fold the sign-off into one dense closing paragraph.** Every post (Instagram caption, X post, Threads post) ends with visually separate lines, a blank line before each: the Source line, then the Follow line (then, on Instagram only, the hashtag line). The follow line always reads "Follow @<handle> for more AI updates!" with the platform's own handle: `@theaideskio` on X (X handles can't contain dots), `@theaidesk.io` on Threads and Instagram. Breaking-mode posts get the Source and Follow lines too; when the body already cited the one primary artifact the whole post rests on, the Source line can repeat that reference.

**Threads gets a topic tag — nothing else does.** Buffer's Threads metadata carries
`metadata.threads.topic`, a short 1-3 word category string Meta surfaces on the post for
discovery. It was going out unset before 12 Sep 2026. Set it on every Threads post in every mode:
the primary company's name for a single-company story (`"OpenAI"`, `"Anthropic"`, `"Nvidia"`),
or `"AI News"` for a multi-company roundup, a Signal-mode digest, or anything without one clear
subject. X and Instagram have no equivalent Buffer field — don't go looking for a "topic" to set
on those two.

**Write like a person explaining this to a friend, not like a press release compressed to fit.** A first-pass draft (yours or a pasted digest) tends to read as AI-dumped: jargon left untranslated (throughput-per-watt, single-turn workload, HBM4, unseen-task success rate), near-identical wording just trimmed to different lengths across platforms, and every sentence at the same dense weight. Fix both. Translate technical terms into what they mean for a non-technical reader — "1.5–1.9x more work per watt" becomes "roughly 50 to 90% more work for the same amount of power"; a benchmark suite name becomes "a simpler test than the one they'd normally use." X and Threads now share one short bulleted text, so the register difference lives between that post and Instagram, which is the warmest and most narrative — it can open on a real hook sentence ("Three things happened this week that quietly matter more...") rather than restating the news dryly. Re-read your own draft once before posting and ask whether it sounds like it was dumped from a model or written by someone who actually understood the story — if the former, rewrite it, don't just trim it.

## Step 4 — Generate the images (image system v2)

**Breaking mode skips this step entirely.** No hook, no thread card, no carousel. Breaking posts
go out as text so they can ship fast and without Kush having to attach anything by hand.

Use `scripts/theaidesk_v2.py`. `build(mode, params, base_dir)` returns HTML; render with
Playwright at `device_scale_factor=2` and downscale with ffmpeg lanczos, exactly as v1 did
(see `references/render_example.py`). `scripts/build.py` is the retired v1 renderer, kept
only so old posts can be re-rendered.

Modes: `'hook'` 1080x1350 (Instagram), `'thread'` 1600x900 (X and Threads, handle differs),
`'body'` 1080x1350 (carousel slide 2+).

**Locked decisions. Do not vary these per post.**

- **Headline face is Familjen Grotesk 700**, at 116px hook / 93px thread / 88px body, with
  line-height 1.06, letter-spacing -0.020em and word-spacing 0.01em. Three condensed poster
  faces were tested and rejected: at negative tracking they turn into a grey brick in-feed.
  The spacing is the point. Do not tighten it to fit a longer headline, rewrite the headline.
- **Layout is centred** (`align='center'`). Use `'left'` only when a headline runs to three
  lines. Centred drops the white bar beside the subhead; left-aligned keeps it.
- **The accent re-hues to the story's primary company.** Pass `accent='#12A594'` and so on;
  violet `#5B4480` is the house default, used for roundups and any post covering more than one
  company. The table lives on the Notion Image Generation Recipe page: OpenAI `#12A594`,
  Anthropic `#D97757`, Google `#4285F4`, xAI `#6366F1`, Cursor `#7C93F5`, DeepSeek `#4D6BFE`,
  MiniMax `#FF4D4F`, Meta `#0866FF`.
  <callout>
  A v2 revision once locked this to violet-always, reasoning that an accent *in the headline*
  would make a re-hued grid read as three different accounts. Kush rejected that twice: once on
  1 Sep when a violet render went out on an Anthropic-only post, and again on 2 Sep when the
  correction had not reached this file. Do not reintroduce it. If the argument seems persuasive,
  it is his call to make, not yours.
  </callout>
- **Ground is the redaction field** (blocks of varying width at 5-9% opacity, a few lit in
  accent, faded out below the midline). It replaces the v1 blurred blob mesh entirely. Still
  no turbulence, no warp, no procedural smoke.

**Two-tone headline.** Wrap words in `*asterisks*` and they render in the accent:
`headline="The agents *were ours*"`. One emphasis span per headline, at the end, not the start.

**Verification tag.** `tag='VERIFIED'` (green), `'VENDOR CLAIM'` (amber) or `'OUR READ'` (blue),
sits above the headline. This is the X-thread caveat strategy put on the cover. Set it honestly:
VENDOR CLAIM whenever the headline carries a company's own unverified figure.

**Story object.** One abstract mark from the fixed library in `OBJECTS`: `breach`, `ledger`,
`silicon`, `climb`, `weights`, `longrun`. Pick one, never draw a new one per post; recognition
comes from reuse. Pass `story_object='breach'`. Never a photo, never a company logo here.

**Attribution row.** `marks=['openai','huggingface']`, company slugs, **capped at 3** (a roundup
touching seven companies still shows three; more is logo soup). A slug with a file at
`logos/<slug>.svg` renders as the real mark; a slug without one falls back to a typographic
chip automatically. 21 CC0 marks from Simple Icons ship in `logos/`; see `logos/MANIFEST.json`.

<callout>
**Logo rules, and they are not optional.** Marks render white on dark and nothing else: no
feather, no blur, no tint, no effects. Several brand guidelines prohibit modification outright.
OpenAI's, checked Aug 27 2026, prohibits recolouring the Blossom, adding effects or textures,
using the mark more prominently than your own, and implying partnership. That is why marks sit
small in the attribution row, never as the story object and never larger than THE AI DESK.
OpenAI and Salesforce are both absent from Simple Icons. To add either, download the official
SVG from that company's own brand portal (OpenAI publishes at brand.openai.com), confirm its
terms permit editorial use, and save it as `logos/<slug>.svg`. It renders on the next build with
no code change. Do not scrape a mark from a search result or a mirror.
</callout>

**Chrome.** `THE AI DESK` top-left, Desk value top-right (`THE SIGNAL` for Signal mode),
handle bottom-left, `swipe='SWIPE FOR MORE'` bottom-right on carousel slide 1.
**No counter pill.** `build()` still accepts `counter=`, but Kush dropped the rendered "DAY 17"
badge on 30 Aug 2026. The Day number lives in Notion and in the filenames. Leave the param out.
The masthead rule carries `rule_word='OPENAI · HUGGING FACE · AUG 26'`, the companies and date,
not the brand name again.

**The Caveat script line is retired on hook and thread.** The rule word and the tag do its job
now. It is still supported via `script='...'` if a post wants it back.

Handles: `@theaidesk.io` on Instagram and Threads assets, `@theaideskio` on the X asset.

Fonts: `npm install @fontsource/familjen-grotesk @fontsource/caveat @fontsource/space-grotesk`,
copy the four woff2 files into `fonts/` next to the HTML. v2 needs no new font.

**Thread mode cannot carry the full top zone.** On the 1600x900 canvas the story object plus
the attribution row runs straight into the bottom-anchored text block, which is centred and
therefore tall. For `'thread'`, omit `story_object` entirely, shorten the subhead to two lines,
and pass `top_zone=120, block_bottom=118, mark_size=56`. Hook keeps the object; its 4:5 canvas
has the headroom. On hook, real marks sit lower than a typographic chip, so pass `mark_size=64,
top_zone=140` whenever `marks` resolves to a stored SVG rather than a chip.

**A three-line headline is a rewrite, not a layout problem.** It pushes the block up into the
attribution row. The locked spacing rule already says not to tighten tracking to fit; the same
applies to nudging `block_bottom`. Shorten the headline.

**Check every mark actually renders as a mark.** `icon_svg()` forces `fill-rule="evenodd"`, but
it does not save every multi-part path: Nvidia renders inverted, as a solid white block with the
swoosh knocked out. That is a modified logo and breaks the rules in the callout above. If a mark
renders wrong, drop it rather than shipping it, and prefer marks for companies that are actually
the story's subject over ones that are a detail in the copy.

**Crop-check every render before calling it final** — the script/headline seam, the frame edges,
the bottom margin, and that nothing that matters sits below row 1215 on the 1080x1350 canvas.

**Render to JPEG with the repo script (tested 4 Oct 2026).** Python Playwright is not installed in the cloud sandbox, and `references/render_example.py` writes PNGs, so for Regular/research runs use `scripts/render_posts.py` from the `theaidesk-daily` repo instead: `python3 scripts/render_posts.py spec.json OUT_DIR`. `spec.json` is a list of `{"out": "post-N/instagram.jpg", "mode": "hook"|"thread", "params": {...}}` jobs using the same params as `build()`. It builds the HTML, screenshots with Node Playwright and Chromium, fetches fonts with npm, and writes sRGB JPEGs (about q85, 1080x1350 for Instagram, 1600x900 for X and Threads, each asserted under 1 MB). Write them straight into `posts/YYYY-MM-DD/post-N/` as `instagram.jpg`, `x.jpg` and `threads.jpg`. Remember the thread-mode rules above and crop-check every render with the Read tool before committing.

Deliver the final JPEGs with `SendUserFile` (`proactive` for scheduled runs, `normal` in live chat).

## Step 4b — Commit, PR and self-merge (Regular/research runs only)

Buffer fetches images by public URL, so the creatives go to `https://github.com/theaidesk/theaidesk-daily` first. Buffer is touched only after this step has merged to `main`; never schedule against an unmerged branch URL.

Auth, env only: `export GH_TOKEN="$THEAIDESK_DAILY_PAT" GITHUB_TOKEN="$THEAIDESK_DAILY_PAT"; unset GITHUB_USER`. Run `gh api user --jq .login`; it must print `theaidesk` or the run aborts before anything is pushed (notify, do not work around). HTTPS only, never print the PAT. Commit email is `<id>+theaidesk@users.noreply.github.com` from `gh api user`. No `Co-Authored-By`, no "Generated with" line, no model or agent names anywhere in GitHub text; roles only.

1. Pull `main`; branch `posts/YYYY-MM-DD` (Sydney date; if taken use `posts/YYYY-MM-DD-HHMM`). Never commit on `main`, never use a branch name starting with `claude/`.
2. Write `posts/YYYY-MM-DD/post-N/{manifest.json,instagram.jpg,x.jpg,threads.jpg,instagram.txt,x.json,threads.json}` for each post (N at most 2 unless the day holds more, hard ceiling 4). JPEG sRGB about q85 under 1 MB; Instagram 1080x1350, X and Threads 1600x900. Never overwrite an existing dated path. `manifest.json` carries date, post, theme, status, platforms and the three raw URLs.
3. Commit as `theaidesk` (`posts: YYYY-MM-DD post-1..N AI daily creatives`), push the branch, open one PR into `main` titled `posts: YYYY-MM-DD (N posts)` with a short neutral body. Use the REST API (`gh api repos/theaidesk/theaidesk-daily/pulls`); GraphQL may be unavailable.
4. Squash-merge your own PR with `PUT .../pulls/{n}/merge` (`merge_method=squash`), only if the PR author is `theaidesk` and the head is the branch you pushed. Never push to or force-push `main`.
5. Poll the raw URLs (bounded wait, a few minutes) until all return 200. If they do not, report and stop; no second PR for the same run.

## Step 5 — Post to Buffer

Org "My Organization", id `6a8a5f25d83063529f26ab69`. Re-verify channel IDs with `list_channels` rather than trusting these blindly (call it out in your report if they've changed):
- X/twitter: `6a8af292ccaf649a67fecef4`
- Threads: `6a8af88eccaf649a67fee6e0`
- Instagram: `6a8a6114ccaf649a67fb8eda`

**Order and images (revised).** Step 5 runs only after the merge in Step 4b (or from `main` in buffer-from-main mode). Every post gets its image on all three platforms, attached by URL: `assets: [{image: {url: "https://raw.githubusercontent.com/theaidesk/theaidesk-daily/main/posts/YYYY-MM-DD/post-N/<platform>.jpg", metadata: {altText: "..."}}}]` with `instagram.jpg` on Instagram, `x.jpg` on X and `threads.jpg` on Threads. Buffer accepts remote image URLs, so Instagram is scheduled normally, not drafted. The older text-only and draft-Instagram instructions below apply only to Signal and Breaking modes or when the raw URLs cannot be fetched. Every Threads post still gets `metadata.threads.topic` set (single company name or `"AI News"`); never omit it.

**Single post on X and Threads (revised 4 Oct 2026):** send one `text` with no `metadata.twitter.thread` / `metadata.threads.thread` array; never create a second post or thread item. Threads still gets `metadata.threads.topic`. Everything in the thread-item wording below applies only to legacy multi-item posts.

**Single post on X and Threads (revised 4 Oct 2026):** send one `text` with no `metadata.twitter.thread` / `metadata.threads.thread` array; never create a second post or thread item. Threads still gets `metadata.threads.topic`. The X post's Follow line uses `@theaideskio`; the Threads post's uses `@theaidesk.io`. Everything in the thread-item wording below applies only to legacy multi-item posts.

**X and Threads** schedule cleanly, text-only in the legacy path: `create_post` with `mode: "customScheduled"`, `schedulingType: "automatic"`, an explicit `dueAt`, outer `text` matching the first thread item exactly, and every thread item under `metadata.{twitter,threads}.thread`. On the Threads side, also set `metadata.threads.topic` per Step 3 (single company name, or `"AI News"`) — every Threads post needs it, in every mode.

**Legacy path only: Instagram cannot be scheduled without media** — `create_post` rejects it outright ("Instagram posts require at least one image or video"). It *can* be saved as a draft that carries the intended time: same `mode: "customScheduled"` and `dueAt`, plus `saveToDraft: true`, `metadata.instagram.type: "post"`, `shouldShareToFeed: true`. Always create the Instagram post this way — never skip it. Kush attaches the image himself in Buffer and promotes the draft to scheduled; that's the deliberate handoff point, not a gap to apologize for. **This Instagram draft is the one kind of draft this skill leaves alone on purpose** — the capacity check below never touches it, because no amount of free capacity fixes the missing-media rejection.

**If you edit an Instagram draft later** (a copy revision, a fact correction) via `edit_post`, you must pass `saveToDraft: true` again on that call. `edit_post` re-validates the whole post fresh rather than merging with what's stored, so omitting it makes Buffer treat the edit as "schedule this now" — which fails immediately with the same missing-media error, since there's still no image. This isn't hypothetical; it's happened.

If a public or presigned image URL ever becomes available (this has been discussed but isn't live yet — check with Kush if it's unclear), attach real URLs to all three and schedule Instagram normally instead of drafting it.

**Always pass an explicit, matching `dueAt` to all three platforms rather than `shareNext`** — `shareNext` picks the next open slot per-channel independently, which left X and Threads posted at different times in an earlier run. The three platforms are one story; they should go out together.

**Check capacity before you post, in every mode, not just Breaking.** Call `list_posts` filtered
to `status: ["scheduled"]` across the organization and count against the free-plan cap of 10
scheduled posts before creating anything. This was previously only checked in Breaking mode;
Kush asked on 12 Sep 2026 for it to apply everywhere, because Research and Signal runs can hit
the same cap.

**Reclaim stranded X/Threads drafts before adding new posts.** If a past run hit the cap and had
to leave an X or Threads post as an unscheduled draft instead of skipping it outright, that draft
is stranded, not intentional — unlike the Instagram draft above, it should not sit there
forever. Before creating this run's posts: call `list_posts` with `status: ["draft"]` on the X
and Threads channel IDs, then check the current scheduled count against the cap. If there's
room, promote each stranded draft with `edit_post` (`mode: "customScheduled"`,
`schedulingType: "automatic"`, a fresh `dueAt` chosen the normal way for its mode) instead of
leaving it behind, and say so plainly in the Step 7 report — which draft, and its new time. Only
touch drafts this skill plausibly created (X/Threads, AI-desk voice, no Instagram); never
reschedule something that isn't clearly one of this pipeline's own stranded posts.

**Picking the time:**
- *Research mode:* call `list_posts`, find the earliest still-future slot in the existing 11:30 UTC / 20:00 UTC rhythm that isn't already occupied.
- *Signal mode:* target 1:30pm Sydney local time. Compute the UTC offset fresh each run rather than hardcoding it — Sydney is UTC+10 (AEST) roughly April–October and UTC+11 (AEDT) October–April; check the actual current offset (e.g. `TZ=Australia/Sydney date`) rather than assuming. If 1:30pm Sydney has already passed today, use tomorrow's.
- *Breaking mode:* **X and Threads only, text only, never Instagram.** Capacity is counted live,
  never assumed. Buffer's free plan allows 10 scheduled posts **per channel**, and 2 of those are
  permanently reserved for the daily image posts (the 11:30 and 20:00 UTC Research slots), which
  leaves 8 for Breaking. Before writing anything, call `list_posts` with `status: ["scheduled"]`
  **separately for the X channel and for the Threads channel** and count each. Breaking room per
  channel = 8 minus that channel's scheduled count of *text* posts (Breaking and Signal), and the
  usable number this cycle is the smaller of the two channels. Also confirm total scheduled on
  each channel is at most 8 after adding, so the 2 image slots stay free. Fill that room with
  every genuinely distinct, well-sourced story that clears the bar, up to the room available;
  never pad to reach the number, since the sourcing bar and the 48-hour ceiling still decide how
  many actually ship. Each story's slot must sit at least 2-3 hours clear of **every** other
  scheduled post, image or text, so the feed never doubles up; with several stories, space them
  2-3 hours apart, filling the earliest clean slots first. If there is no clean slot, ship
  nothing. Report the live counts (for example "X 2/8, Threads 2/8, added 3") in the Step 7
  report.
  *Bench a story instead of dropping it.* When a story clears the freshness and sourcing bars but
  there is no clean slot or no room this cycle, save it to X and Threads as **drafts** (`saveToDraft:
  true`, same one-line wire format, no `dueAt`) rather than discarding it, and log a Content
  Calendar row with `Status: Drafting` and the Buffer draft ids in the page body. Drafts do not
  count toward the 10-post cap, but only bench stories that would have shipped: same sourcing bar,
  never a weaker story parked for later. Next cycle, before scanning for anything new, list the
  X and Threads drafts and check each one: if the facts changed (a correction or retraction),
  edit or delete it; otherwise it ships. Which prefix and how depends on the story's own
  timestamp:
  - *Inside 48 hours:* keep the `BREAKING:` / `JUST IN:` prefix it earned. If a clean slot exists
    in the next few hours, promote with `edit_post` (`mode: "customScheduled"`, fresh `dueAt`);
    if the story is close to the 48-hour edge, post it instantly with `mode: "shareNow"` as long
    as it sits at least 2-3 hours clear of every scheduled post.
  - *Older than 48 hours:* it is no longer breaking, so **never** use `BREAKING:` or `JUST IN:`.
    Swap the prefix to `IN CASE YOU MISSED IT:` and put the original date inside the sentence
    ("on Sep 26"), so nobody reads it as fresh. The rest of the wire format is unchanged
    (blank line, follow line, then the reply with `Source: <publisher>, <original date>`). Post
    it instantly with `mode: "shareNow"` when the spacing rule allows, otherwise schedule it at
    the next clean slot. Do not delete it. This exception applies **only** to stories this
    pipeline benched, which already cleared the sourcing bar; a story first found stale still
    never ships.
  Update the Notion row to `Scheduled` (or `Posted` for shareNow), set `Posted At` to the actual
  time, and leave `Story Published At` as the original source timestamp so the lag figure stays
  honest; note "recap" in the page body for stale ones so the Timing Review can discount them.

**buffer-from-main mode.** Read `manifest.json` and the caption files from `main`, confirm the raw URLs return 200, then run the duplicate checks below and the Notion lookup. If X and Threads already published the story text-only, do not repost them; schedule only the missing platform (usually Instagram) with its image at the next free slot, and update the existing Notion row instead of creating a new one. Notion rows may be edited in place to keep them current, but `Story Published At` must stay equal to the source's own timestamp.

**Watch for a duplicate or resumed run.** A Breaking cycle that was interrupted and resumed, or
that fired twice, can arrive to find its own story already scheduled minutes earlier. Before
creating anything, check `list_posts` for a post covering the same story created in the last
hour. If one exists, that cycle is already served: stop, and don't double-post it.

Never modify a Buffer post this run didn't create. Watch the free-plan cap of 10 scheduled posts — if creating these would exceed it, create what fits, leave the rest as drafts rather than dropping them, and say plainly what got left as a draft, why, and that a future run will try to reclaim it per the stranded-drafts rule above.

## Step 6 — Log to Notion

Content Calendar data source: `collection://610c875f-40ba-4476-8068-b0369c50ac5d`. If a row for the same story already exists, edit it in place instead of creating a duplicate (keep `Story Published At` equal to the source's own timestamp; the rest is for tracking). Query `MAX(Day)` first — Day numbers are sequential across both modes, one shared counter.

Properties: `Day` (next unused number), `Post` (short title), `Status` (`Scheduled` once Buffer posts exist — X/Threads scheduled + Instagram drafted counts as scheduled, not "Ready to post"; use `Needs research` or `Drafting` if you couldn't find a solid story or the images didn't come out clean, and explain what's unresolved instead of posting anyway), `Format` (`Single` for Signal-mode — one hook image, no carousel — and whatever fits for Research mode), `Desk` (closest fit from the fixed list `The Brief / Breaking / Explainer / The Number / Watch This / Free Tier / Correction / Ask the Desk`; Signal-mode roundups fit `The Brief`), `Companies` (multi-select — the current fixed options are `OpenAI, Anthropic, xAI, Cursor, Google, DeepSeek, MiniMax, Higgsfield, CapCut, Meta`; if a story's company isn't in that list, don't guess a substitute — tag what does fit and note the gap in your report), `Assets` (the three filenames), `X thread` (checked), `Date` (the day the Buffer posts are scheduled for), and `Tag` (`Regular`, `AI Daily Signal` or `Breaking` — this is what distinguishes the three modes in the same table).

**`Story Published At` and `Posted At` are required on every row, not optional.** The weekly
Timing Review reads them through the `Lag Hours` formula to work out how far behind the news the
desk actually is, and a row missing either one is invisible to it. `Story Published At` is the
source's **own** timestamp; when only a date is published, use 12:00 UTC that day. `Posted At` is
the exact Buffer `dueAt`. Both are datetimes, and the Notion API wants
`YYYY-MM-DDTHH:MM:SS` with the `T` and **no** trailing `Z` — a space separator or a `Z` suffix
is rejected with a validation error, which has cost a retry more than once.

For a Breaking row: `Desk` is usually `Breaking`, `Format` is `Single`, `X thread` is unchecked
when X got a single tweet, and `Assets` says plainly that there is no image this cycle.

Fetch page `3c4c18505d1281c18658f6add7eaf092` as a content-formatting template — it shows the Instagram caption / X thread / Threads sections as Notion callouts. Match that structure, then append a `Buffer status` callout listing the three filenames, the Buffer post ids, the scheduled time in both UTC and Sydney time, and explicitly which posts have no image attached yet.

## Step 7 — Report back

Plain text, always covering: the Day number and title, a one-line story summary, the scheduled time in UTC and Sydney time, confirmation the three images were sent as files, the PR URL, branch and merge SHA, the Buffer post IDs, the raw image URLs used, and that all three platforms were scheduled with their images (legacy text-only or draft-Instagram runs must say so plainly). If any stranded draft from a past run was reclaimed and scheduled this run (Step 5), name it and its new time. If capacity didn't allow scheduling everything this run, name what got left as a draft and why.

**In Breaking mode the report is short**: Day number and title, a one-line story summary with
its date, the source, and the scheduled time in UTC and Sydney. No image lines, since there are
no images.

**An empty Breaking cycle is a success, and it is silent.** If nothing inside the 48-hour window
clears the sourcing bar, or there is no clean slot, ship nothing and send no report and no
notification. Most cycles will end this way and that is the design, not a failure. The one thing
always worth breaking silence for is a cycle that *couldn't run* — the skill missing, Buffer or
Notion unreachable, a scheduling call failing — because that is the case where staying quiet
would hide a broken pipeline behind what looks like a quiet news day.

**In Signal mode specifically, always show what changed from what Kush pasted** — claims you dropped because they didn't check out, framing you tightened for attribution, anything cut for length or brand-voice fit. He should never have to diff the post against his draft himself to find out what you changed.