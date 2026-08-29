# theaidesk-daily

Public media host for [Buffer](https://buffer.com). Brand: **theaidesk.io**. Owner: [github.com/theaidesk](https://github.com/theaidesk).

This repo stores dated JPEG assets and captions so Buffer can fetch a public URL at publish time.

## Claude daily job

Use **HTTPS only**. Do not use SSH, do not use `gh`, and do not put a PAT in the prompt.

1. Attach this repo as the Claude GitHub session source while connected as **theaidesk**.
2. Commit unique dated paths under `posts/`.
3. `git push` over HTTPS.
4. Pass Buffer a public JPEG URL (GitHub raw, or the jsDelivr fallback).

## Humans

Push with SSH **ed25519** to:

```
git@github.com:theaidesk/theaidesk-daily.git
```

- Not a deploy key.
- Not RSA unless a host forbids ed25519.

## Retention

Buffer fetches files at publish time. Keep files until **7 days after the scheduled send**, then prune.

## Image rules

- Format: JPEG
- Color: sRGB
- Quality: ~85
- Size: under 1MB
- Instagram: 1080×1350 (4:5)
- X / Threads: 1600×900

## Buffer URL pattern

```
https://raw.githubusercontent.com/theaidesk/theaidesk-daily/main/posts/YYYY-MM-DD/post-N/instagram.jpg
```

Fallback if Buffer rejects GitHub raw:

```
https://cdn.jsdelivr.net/gh/theaidesk/theaidesk-daily@main/posts/YYYY-MM-DD/post-N/instagram.jpg
```

Use unique dated paths. Never overwrite the same filename.
