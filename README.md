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

A US number like `+1 (202) 285-1684` might render as:

> **Business line:**
> +(h¹¹(ℙ¹)) ( (lim 2(s−1)ζ(s)) (Tr(Tᵃ)) (χ(ℂP²)−1) ) ∑ b₂ᵢ(ℂP¹) (dim(e₇)−125) (rank(e₇)−2) — (lk(L2a1)) (rank(e₈)−2) (∫dx/(1+x²)⁴ · 128/5π) (rank(e₇)−3)

Every expression is mathematically verified to evaluate to its digit.
The bank covers Weyl group orders, class numbers of imaginary quadratic fields,
Euler characteristics, Betti numbers, residues, Bessel function Wronskians,
and more — over 200 templates across all ten digits.

---

## Features

- **249+ countries supported** — full UN M49 geoscheme (continent → subregion → country),
  with per-country digit limits and display formatting
- **200+ verified equation templates** — 20–25 per digit, spanning eight areas of
  graduate mathematics, all mathematically audited
- **Uniqueness guarantee** — no expression repeats within a single number
- **LaTeX rendering pipeline** — `pdflatex` + `pdftoppm`, standalone document,
  auto-cropped to content
- **PNG output** — sized for email signatures and business cards, saved to Downloads
- **Desktop GUI** — Tkinter, country/subregion dropdowns, signature line picker,
  custom text support
- **Optional file logging** — checkbox-controlled, single unified log in Downloads

---

## Output

Each run saves one file to `~/Downloads`:

| File | Format | Best for |
|---|---|---|
| `Dialogorithm_Contact.png` | PNG at 150 DPI | Email signatures, business cards, social profiles |

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

# Launch the app
python dialogorithm.py
```

Then:

1. Choose a **continent → subregion → country** from the dropdowns
2. Enter your local phone number in the entry field
3. Pick a **signature line** (random, preset, or custom)
4. Click **Generate LaTeX Image**

Your PNG appears in `~/Downloads/Dialogorithm_Contact.png`.

---

## Project structure

```
dialogorithm/
├── dialogorithm.py          # Desktop GUI (Tkinter) and app entry point
└── support_files/
    ├── equation_bank.py     # 200+ LaTeX equation templates, digits 0–9
    ├── latex_processor.py   # Document assembly, pdflatex pipeline, PNG output
    └── phone_formats.py     # 249+ countries, UN geoscheme, digit limits
```

---

## Requirements

- Python 3.10+
- `pillow` — image handling in the GUI
- **TeX Live** (or MacTeX) — `pdflatex` and `pdftoppm` must be on your PATH

No internet connection required after install. Everything runs locally.

---

## Security and privacy

- **Nothing leaves your machine.** No API calls, no telemetry, no network
  requests of any kind. The app is entirely local.
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