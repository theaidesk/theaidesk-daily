# Claude prompt — theaidesk daily images → GitHub → Buffer

Copy everything below the line into Claude. Do **not** paste a GitHub token into this prompt.

---

You are shipping daily AI-news creatives for **theaidesk.io** into the public Buffer media repo.

## Repo
- https://github.com/theaidesk/theaidesk-daily
- Brand: theaidesk.io
- Default branch: `main` (Buffer reads **only** `main`)

## Auth (pick one; never put a PAT in chat or in files)
1. Preferred: Claude GitHub connected as user **theaidesk**, repo attached as the session source.
2. Else: use a **fine-grained PAT** scoped only to `theaidesk/theaidesk-daily` with Contents: Read and write (and Pull requests: Read and write if you open PRs). HTTPS only. Never commit the token. Never use SSH. Never use `gh` if the session already has git+HTTPS.

## Workflow each run
1. Pull latest `main`.
2. Create branch: `posts/YYYY-MM-DD` (Sydney calendar date for the campaign day).
3. For each scheduled post `N` (1-based), write under:

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

4. Never overwrite an existing dated path. If the folder exists, use `post-(N+1)` or a new date folder.
5. Commit with a clear message, e.g. `posts: YYYY-MM-DD post-N AI daily creatives`.
6. Push the branch over HTTPS.
7. Open a PR into `main` titled `posts: YYYY-MM-DD (N posts)` with a short body: what news theme, how many posts, Buffer URL samples.
8. Stop after the PR is open. A human reviews and merges to `main`. Do not force-push `main`. Do not merge yourself unless explicitly told.

## Image rules
- JPEG, sRGB, quality ~85, under 1MB each
- Instagram: 1080×1350 (4:5) → `instagram.jpg`
- X and Threads: 1600×900 → `x.jpg` and `threads.jpg` (may be identical pixels if the crop is the same; still write both files)
- Captions: `instagram.txt` plain text; `x.json` / `threads.json` with at least `{"text":"..."}` (keep platform limits in mind)

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
Status stays `ready` until after Buffer has published; a human may later set `published`.

## After merge (for Buffer)
Public URLs (only valid once on `main`):

```
https://raw.githubusercontent.com/theaidesk/theaidesk-daily/main/posts/YYYY-MM-DD/post-N/instagram.jpg
https://raw.githubusercontent.com/theaidesk/theaidesk-daily/main/posts/YYYY-MM-DD/post-N/x.jpg
https://raw.githubusercontent.com/theaidesk/theaidesk-daily/main/posts/YYYY-MM-DD/post-N/threads.jpg
```

Fallback if Buffer rejects GitHub raw:

```
https://cdn.jsdelivr.net/gh/theaidesk/theaidesk-daily@main/posts/YYYY-MM-DD/post-N/instagram.jpg
```

Paste those URLs into Buffer for the Instagram / Threads / X scheduled posts. Keep assets until **7 days after** the scheduled send, then prune.

## Input you will receive each run
- News brief / sources for the day
- How many posts (`N`)
- Any brand tone notes

Generate the images and captions from that brief, then follow the workflow above. End with the PR link and the three Buffer URLs per post (noting they resolve after merge).
