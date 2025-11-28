# Setup Steps for Before/After Slider
[![GitHub stars](https://img.shields.io/github/stars/hkommula/before_after_slider.svg)](https://github.com/hkommula/before_after_slider/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/hkommula/before_after_slider.svg)](https://github.com/hkommula/before_after_slider/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/hkommula/before_after_slider/blob/main/LICENSE)
[![Top language](https://img.shields.io/github/languages/top/hkommula/before_after_slider.svg)](https://github.com/hkommula/before_after_slider)
[![Repo size](https://img.shields.io/github/repo-size/hkommula/before_after_slider.svg)](https://github.com/hkommula/before_after_slider)


## **What is this tool?**
This is a simple browser-based before/after image comparison tool. You place your images into the `images` folder, and the tool automatically builds interactive sliders so you can visually compare the before and after versions.

## **What does it do?**
It loads your image pairs, generates a `sets.json` file, and displays them in a clean slider UI through `index.html`. Everything updates automatically when you add or change images.

## Example: 
You can see a working example here: https://hkommula.github.io/before_after_slider/

## **Steps**
1. **Clone the repository**
   * Open a terminal and run:

```
git clone https://github.com/hkommula/before_after_slider.git
```
2. **Add your images** inside the `images` folder.
   * Images must follow this naming format: `XXXX_before.jpg` and `XXXX_after.jpg`
   * Supported formats: `.jpg`, `.png`, `.JPG`, `.JPEG`. Each folder or pair of files becomes a slider set.

3. **The tool runs from `index.html`**, which reads `sets.json` to know what image sets to load.

4. **`sets.json` is auto-generated** whenever the images folder changes (add/remove).

5. **Set up GitHub Actions** to auto-generate `sets.json`:
   * Go to **GitHub**  → **Actions** →  Click **New workflow** →  Choose **Set up a workflow yourself**
   * Paste the following code:

```
name: Generate image sets

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # needed if you want auto-commits

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install dependencies (if any)
        run: |
          python -m pip install --upgrade pip
          # pip install -r requirements.txt  # if you ever need it

      - name: Generate sets.json
        run: |
          python generate_sets.py

      - name: Commit updated sets.json
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: update generated images/sets.json"
          file_pattern: images/sets.json
```

6. **Enable GitHub Pages** so the tool is available publicly:
   * Go to **Settings → Pages**
   * Select your main branch and root folder
   * Save and open the published link.

7. **Wait for updates to apply**:
   * After adding new images, **GitHub Actions takes ~1 minute** to generate the new `sets.json`.
   * GitHub Pages then takes **about 1-2 minutes** to deploy the updated site.

8. **Done!** Your before/after slider is now live and updates automatically whenever you add or change images.


## Limitations
- Does **not** work well on mobile devices.
- Large image files (**>​25MB**) may cause slow performance or heavy browser load.
  
## Open Source License
This project uses the **MIT License** - you can use it freely for personal or commercial projects with proper attribution.
