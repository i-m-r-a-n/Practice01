"""Storyboard sheets from the low-sample preview renders (start / middle / end frame of every shot, before final rendering).
python3 make_storyboard.py STORY_DIR   (STORY_DIR = work/story written by render_shots.py --story)"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '04_BLENDER_ANIMATION', 'scripts'))
import shots as S
story = sys.argv[1]
F = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 18)
FS = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 15)
TW, TH = 400, 225
for video, names in (('A_client_pitch', S.PITCH_ORDER), ('B_full_tour', S.TOUR_ORDER)):
    rows = []
    for n in names:
        d = os.path.join(story, n)
        fr = sorted(os.listdir(d)) if os.path.isdir(d) else []
        if fr:
            rows.append((n, [Image.open(os.path.join(d, f)).convert('RGB').resize((TW, TH), Image.LANCZOS) for f in fr[:3]]))
    per = 10
    for p in range(0, len(rows), per):
        chunk = rows[p:p + per]
        sheet = Image.new('RGB', (40 + 3 * (TW + 10) + 260, 60 + len(chunk) * (TH + 16)), (246, 243, 238))
        d = ImageDraw.Draw(sheet)
        d.text((20, 18), f'Storyboard {video.replace("_", " ")}  -  start / middle / end frame of each camera move (preview renders)', font=F, fill=(30, 30, 28))
        y = 56
        by = {s['name']: s for s in S.SHOTS}
        for n, ims in chunk:
            s = by[n]
            for i, im in enumerate(ims):
                sheet.paste(im, (20 + i * (TW + 10), y))
            x = 20 + 3 * (TW + 10) + 10
            d.text((x, y + 4), n, font=F, fill=(38, 103, 61))
            d.text((x, y + 32), f"{s['scene']}", font=FS, fill=(60, 60, 58))
            d.text((x, y + 54), f"{s['label'] or '-'}", font=FS, fill=(60, 60, 58))
            d.text((x, y + 76), f"{s['kind']}, {s['dur']} s", font=FS, fill=(60, 60, 58))
            y += TH + 16
        sheet.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'storyboard_{video}_{p // per + 1}.jpg'), quality=86)
print('storyboard sheets written')
