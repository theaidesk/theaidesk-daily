# Claude prompt — theaidesk daily images → GitHub → Buffer

Copy everything below the line into Claude. Do **not** paste a GitHub token into this prompt.

This repo is public so Buffer can fetch JPEG URLs from `main`. That does not change write rules: you still need the PAT to push a branch and open a PR. Do **not** put security instructions, allowlists, or “do not open PRs” warnings in any public PR title, body, comment, commit message, or file. Keep public surfaces boring and asset-only.

---

You ship daily AI-news creatives for **theaidesk.io** into https://github.com/theaidesk/theaidesk-daily.

## Auth
Use the fine-grained PAT you were given (HTTPS only; this repo; Contents + Pull requests). Prefer GitHub identity **`aakarkun`** for commits and the PR author (same house path as other product repos). Never put the PAT in chat, commits, or files. No SSH. Never push or merge `main`.

## Roles (GitHub text = roles only)
Author opens the PR and stops. Architect / Engineer review and merge. Delivery may triage. Owner is not in the day-to-day merge loop. Never put seat or agent names on GitHub — roles only.

## Workflow each run
1. Pull latest `main`. Never commit on `main`.
2. Branch: `posts/YYYY-MM-DD` (Sydney calendar date).
3. For each post `N` write:

```
posts/YYYY-MM-DD/post-N/
  manifest.json
  instagram.jpg
  x.jpg
  threads.jpg
  instagram.txt
  x.json
  threads.json
```

4. Never overwrite an existing dated path.
5. Commit (as `aakarkun` when the PAT allows), e.g. `posts: YYYY-MM-DD post-N AI daily creatives`.
6. Push the **branch** over HTTPS.
7. Open a PR into `main` titled `posts: YYYY-MM-DD (N posts)` with a short, neutral body (theme + post count + Buffer URL samples after merge). No security / allowlist / “author” banners.
8. **Stop.** Do not merge, self-approve, or ping by seat name.

## Image rules
JPEG, sRGB, ~85, under 1MB. Instagram 1080×1350 → `instagram.jpg`. X/Threads 1600×900 → `x.jpg` / `threads.jpg`. Captions: `instagram.txt`; `x.json` / `threads.json` with `{"text":"..."}`.

## manifest.json
```json
{
  "date": "YYYY-MM-DD",
  "post": N,
  "theme": "short theme",
  "status": "ready",
  "platforms": ["instagram", "threads", "x"],
  "urls": {
    "instagram": "https://raw.githubusercontent.com/theaidesk/theaidesk-daily/main/posts/YYYY-MM-DD/post-N/instagram.jpg",
    "x": "https://raw.githubusercontent.com/theaidesk/theaidesk-daily/main/posts/YYYY-MM-DD/post-N/x.jpg",
    "threads": "https://raw.githubusercontent.com/theaidesk/theaidesk-daily/main/posts/YYYY-MM-DD/post-N/threads.jpg"
  }
}
```

## After merge (Buffer)
URLs work only on `main`. Keep assets 7 days past scheduled send, then prune.

## Input each run
News brief, `N`, tone. End with the PR URL and Buffer URLs (valid after merge).
