#!/usr/bin/env python3
"""Render The AI Desk creatives to JPEG (no Python Playwright needed).

Usage: render_posts.py SPEC.json OUT_DIR

SPEC.json is a list of jobs:
  {"out": "post-1/instagram.jpg", "mode": "hook"|"thread"|"body",
   "params": {headline, tag, story_object, marks, accent, rule_word, subhead,
              desk_label, handle, ...}}   # same params as theaidesk_v2.build()

Needs: node + Playwright (/opt/node-tools), Chromium (/opt/pw-browsers), ffmpeg,
and the theaidesk-post skill folder (theaidesk_v2.py, logos/). Fonts are fetched
with npm on first run. Output is sRGB JPEG, about quality 85, 1080x1350 (hook/body)
or 1600x900 (thread).
"""
import glob, json, os, subprocess, sys, tempfile

SKILL = os.environ.get("SKILL_DIR") or next(iter(sorted(glob.glob("/root/.claude/skills/synced/*/theaidesk-post"))), None)
if not SKILL:
    sys.exit("theaidesk-post skill folder not found; set SKILL_DIR")
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import theaidesk_v2 as v  # noqa: E402

spec = json.load(open(sys.argv[1]))
out_dir = os.path.abspath(sys.argv[2])
work = tempfile.mkdtemp(prefix="aidesk_render_")
os.symlink(os.path.join(SKILL, "logos"), os.path.join(work, "logos"))
os.makedirs(os.path.join(work, "fonts"))

# fonts via npm (once per run)
subprocess.run(["npm", "install", "--silent", "@fontsource/familjen-grotesk", "@fontsource/caveat",
                "@fontsource/space-grotesk"], cwd=work, check=True)
for f in ("familjen-grotesk/files/familjen-grotesk-latin-700-normal", "caveat/files/caveat-latin-600-normal",
          "space-grotesk/files/space-grotesk-latin-400-normal", "space-grotesk/files/space-grotesk-latin-700-normal"):
    src = os.path.join(work, "node_modules/@fontsource", f + ".woff2")
    os.link(src, os.path.join(work, "fonts", os.path.basename(src)))

jobs = []
for i, j in enumerate(spec):
    mode = j.get("mode", "hook")
    W, H = (1600, 900) if mode == "thread" else (1080, 1350)
    html = os.path.join(work, f"_{i}.html")
    open(html, "w").write(v.build(mode, j["params"], base_dir=work))
    jobs.append({"html": html, "png": os.path.join(work, f"raw_{i}.png"), "w": W, "h": H,
                 "out": os.path.join(out_dir, j["out"])})

shot = os.path.join(work, "shot.js")
open(shot, "w").write("""
const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined }).catch(() => chromium.launch());
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 2 });
    await p.goto('file://' + j.html); await p.waitForTimeout(700);
    await p.screenshot({ path: j.png }); await p.close();
  }
  await b.close();
})();
""")
subprocess.run(["node", shot, json.dumps(jobs)], check=True)
for j in jobs:
    os.makedirs(os.path.dirname(j["out"]), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", j["png"], "-vf",
                    f"scale={j['w']}:{j['h']}:flags=lanczos", "-q:v", "4", "-pix_fmt", "yuvj420p", j["out"]], check=True)
    size = os.path.getsize(j["out"])
    assert size < 1_000_000, f"{j['out']} is {size} bytes (limit 1MB)"
    print("built", j["out"], f"{j['w']}x{j['h']}", size, "bytes")
