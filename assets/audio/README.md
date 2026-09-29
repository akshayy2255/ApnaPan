# Explainer recordings

Drop recordings here and rebuild (`python3 _build/build.py`).

    <scheme>-<lang>.mp3        e.g.  mudra-kn.mp3   mudra-hi.mp3   mudra-en.mp3

* `scheme` — the slug, i.e. the folder name under `schemes/`:
  `mudra`, `stand-up-india`, `ayushman-bharat`, `nrlm-shg`, `pm-vishwakarma`, `odop`
* `lang` — `kn` (Kannada), `hi` (Hindi), `en` (English)

You do not have to record all eighteen. The build checks which files exist, so
each card plays the recording for the language the woman is reading in, and where
there is none it says so and the phone reads the card aloud instead. Nothing needs
changing in the app — just add the file and rebuild.

Aim for 60–90 seconds. The script is the card's own four lines: what the scheme is,
what she gets, who qualifies, and how to apply — so whoever records only has to
read what is already on screen, in the same order.

Recordings are cached on her phone with the rest of the section, so they play
with no network too.
