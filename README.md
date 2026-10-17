# llama-branding

Master copy of lla.ma brand files. Apps copy what they need from here
(partner-facing files go to `llama-partners/public/kit/`).

## lla.ma colors and type

- Olive (brand green): `#7d9944`
- Ink (near-black): `#0a0a0b`
- Wordmark font: DM Mono, weight 500, letter-spacing -0.025em; the dot is olive

## llama/logos

| File | Use |
|---|---|
| `llama-mark-{olive,white,black}-1024.png` | Llama only, transparent |
| `llama-lockup-for-dark-bg-2000w.png` | Llama + "lla.ma", white text, on dark backgrounds |
| `llama-lockup-for-light-bg-2000w.png` | Llama + "lla.ma", black text, on light backgrounds |
| `llama-lockup-{white,black}-2000w.png` | One-color lockups |
| `llama-avatar-olive-on-{black,white}-1024.png` | Profile pictures (safe for circle crops) |

Don't stretch, recolor or crowd the logos.

## Regenerating

Source: `logos/logo-1024-white-bg.png` (flat llama on white, exported from Canva).

```bash
python3 tools/make_marks.py         # marks + avatars, recolored to exact brand colors
node tools/make_lockups.mjs         # renders lockups in Chromium (DM Mono from Google Fonts)
python3 tools/finish_lockups.py     # trims, adds clear space, sizes to 2000 px
```
