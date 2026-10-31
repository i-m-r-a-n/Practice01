# Shakwat factory: realistic room images with GPT

Pictures of every room of the Bengal Earth Lab virtual tour, turned into photorealistic images by
OpenAI's image model. Source tour: https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/bengal-earth-lab/

Drive: `Imran — Main Folder / shakwat factory / <NN room name>` (folder ids in `drive_folders.json`).

## Needs

- An OpenAI API key in the cloud environment settings, as a Network secret for `api.openai.com`
  or as the environment variable `OPENAI_API_KEY`. A new session picks it up. Never paste the key in chat.
- Node with Playwright (pre-installed in Claude Code cloud sessions), Python 3 with `requests` and `Pillow`.

## Steps

1. Capture the rooms (about 45 minutes, resumable):
   `node capture_rooms.js shots`
2. Drop blank wall frames:
   `python3 select_frames.py shots`
3. Check what will be generated, no API call:
   `python3 gpt_realistic.py --images shots/selected --out realistic --select roomview --dry-run`
4. Generate. Start with one image per room, then widen:
   `python3 gpt_realistic.py --images shots/selected --out realistic --select roomview`
   `--select best3` (about 3 per room) or `--select all` (every picture).

Output: `realistic/<NN room name>/*.png`, plus `realistic/ledger.jsonl` with one line per call.
Already generated images are skipped on a re-run.

## Note

The images are AI-made illustrations of a concept design. GPT can change small details such as
logos, signage text or fittings, so check each image before showing it to a client.
