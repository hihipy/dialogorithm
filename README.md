# dialogorithm

**Turn phone numbers into PhD-level mathematical art.**

`dialogorithm` takes any international phone number and replaces each digit
with a rigorous, graduate-level mathematical expression — drawing from Lie
theory, algebraic geometry, topology, number theory, complex analysis, and
mathematical physics. The result is rendered as a high-quality PNG you can
drop straight into an email signature, business card, or anywhere else you
want to look unreasonably impressive.

---

## What it does

Every digit in your phone number becomes a distinct mathematical expression
that evaluates to that digit. No two expressions in a single number repeat.
The output is typeset in LaTeX and rendered as a clean, single-line image
sized for practical use.

A US number like `+1 (555) 867-5309` might render as:

> **Business line:**
> +(h¹¹(ℙ¹)) ( (lim 2(s−1)ζ(s)) (Tr(Tᵃ_{su(n)})) (χ(ℂP²)−1) ) ∑ b₂ᵢ(ℂP¹) (dim(e₇)−125) (rank(e₇)−2) — (lk(L2a1)) (rank(e₈)−2) (∫dx/(1+x²)⁴ · 128/5π) (rank(e₇)−3)

Every expression is mathematically verified to evaluate to its digit.
The bank covers Weyl group orders, class numbers of imaginary quadratic fields,
Euler characteristics, Betti numbers, residues, Bessel function Wronskians,
and more — over 200 templates across all ten digits, all mathematically audited.

---

## Features

- **249+ countries supported** — full UN M49 geoscheme (continent → subregion → country),
  with per-country digit limits and display formatting that matches the country's own template as you type
- **Special number prefixes** — toll-free, premium, business, and shared rate prefixes
  for 56 countries (184 prefixes total), selectable from a dropdown after choosing a country
- **200+ verified equation templates** — 20–25 per digit, spanning Lie theory,
  algebraic geometry, topology, number theory, complex analysis, and mathematical
  physics; all mathematically audited with zero incorrect expressions
- **Uniqueness guarantee** — no expression repeats within a single number
- **LaTeX rendering pipeline** — `pdflatex` + `pdftoppm`, standalone document,
  auto-cropped to content, rendered at 250 DPI
- **Preview popout** — see the result before committing; save with a custom filename
  to any folder, or discard with nothing written to disk
- **Smart paste** — paste any phone number format (`(786) 212-6394`, `786-212-6394`,
  `+1 786 212 6394`) and digits are extracted automatically
- **Desktop GUI** — Tkinter, country/subregion dropdowns, signature line picker,
  custom text support, clear button
- **Optional file logging** — checkbox-controlled, single unified log in Downloads

---

## Output

Each run opens a preview popout. If you save:

| File | Format | Best for |
|---|---|---|
| `<your filename>.png` | PNG at 250 DPI | Email signatures, business cards, social profiles |

The file is only written to disk if you click **Save**. Discarding deletes the
temp file — nothing stays on your computer.

---

## How many unique outputs are possible?

Each digit is drawn from a pool of 22–25 verified mathematical expressions.
No expression repeats within a single number. Every time you generate the same
number you will almost certainly get a completely different image.

The number of possible outputs scales with total digit count — longer numbers
(more digits in the country code + local number) produce astronomically more
combinations.

**Examples by country:**

| Country | Number | Unique outputs |
|---|---|---|
| 🇺🇸 US | +1 (555) 867-5309 | ~1.16 quadrillion |
| 🇫🇷 France | +33 6 12 34 56 78 | ~1.45 quadrillion |
| 🇪🇸 Spain | +34 612 345 678 | ~1.51 quadrillion |
| 🇦🇺 Australia | +61 412 345 678 | ~1.32 quadrillion |
| 🇿🇦 South Africa | +27 82 123 4567 | ~31.9 quadrillion |
| 🇬🇧 UK | +44 7700 900123 | ~25.2 quadrillion |
| 🇯🇵 Japan | +81 90 1234 5678 | ~31.7 quadrillion |
| 🇮🇳 India | +91 98765 43210 | ~33.1 quadrillion |
| 🇧🇷 Brazil | +55 11 91234-5678 | ~606 quadrillion |
| 🇩🇪 Germany | +49 151 2345 6789 | ~793 quadrillion |

Germany and Brazil top the list simply because their numbers have more total
digits — each additional digit multiplies the combinations by another 20–25.

---

## Getting started

```bash
# Install Python dependencies
pip install pillow

# Install LaTeX (required for rendering)
# macOS
brew install --cask mactex

# Ubuntu/Debian
sudo apt install texlive-full

# Windows
# 1. MiKTeX (pdflatex): https://miktex.org/download
# 2. Poppler (pdftoppm): https://github.com/oschwartz10612/poppler-windows/releases
#    Extract and add the bin/ folder to your system PATH

# Launch the app
python dialogorithm.py
```

Then:

1. Choose a **continent → subregion → country** from the dropdowns
2. Optionally select a **number type** (toll-free, premium, etc.) to pre-fill the prefix
3. Enter your local phone number — or paste any formatted number and it will be cleaned automatically
4. Pick a **signature line** (random, preset, or custom)
5. Click **Generate LaTeX Image**
6. Review the preview, set your filename and save location, then click **Save**

---

## Project structure

```
dialogorithm/
├── dialogorithm.py          # Desktop GUI (Tkinter) and app entry point
└── support_files/
    ├── equation_bank.py     # 200+ LaTeX equation templates, digits 0–9
    ├── latex_processor.py   # Document assembly, pdflatex pipeline, PNG output
    └── phone_formats.py     # 249+ countries, UN geoscheme, digit limits, special prefixes
```

---

## Requirements

- Python 3.10+
- `pillow` — image preview and handling in the GUI
- **TeX Live** (or MacTeX) — `pdflatex` and `pdftoppm` must be on your PATH

No internet connection required after install. Everything runs locally.

---

## Security and privacy

- **Nothing leaves your machine.** No API calls, no telemetry, no network
  requests of any kind. The app is entirely local.
- **Files are only saved if you choose to.** Generated images are written to a
  system temp folder first. Clicking Save copies to your chosen location.
  Discarding deletes the temp file.
- **Logging is off by default.** Enable it with the checkbox in the GUI.
  When enabled, logs write to `~/Downloads/dialogorithm.log`.

---

## License

Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

You are free to use, share, and adapt this work — including for your job —
under these terms:

- **Attribution** — Credit the original author
- **NonCommercial** — Not for selling or commercial products
- **ShareAlike** — Derivatives must use the same license