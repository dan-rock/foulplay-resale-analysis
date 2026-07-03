# Foulplay Resale Market Analysis

Using secondary-market resale data as a **demand signal** for the streetwear brand
[Foulplay](https://foulplay.co) — to answer a question the brand's own storefront analytics can't:
*which past designs does the market still want badly enough to justify bringing back?*

**[View the analysis notebook →](Foulplay_Resale_Analysis.ipynb)**

---

## TL;DR — what the data says

- **The resale market is stable.** Foulplay's median resale price has held near **$45 for
  five years (2021–2026)**. That flat, predictable baseline is what makes the outliers meaningful.
- **A handful of pieces break dramatically from that baseline.** The **"You're Being Robbed"**
  line is the clear standout — selling for **~22× the typical accessory price**, recurring across
  hats, a day hat, and even a rug, and commanding those premiums *even in used condition*.
- **Collaborations carry a durable premium.** Collab pieces (FTP, TeamSesh, G59-adjacent,
  Cultgloria) sell at roughly a **1.4× median premium** over solo pieces, years after release.

Read as product strategy: the resale market is quietly telling the brand what to re-drop.

---

## Why this project

Storefront analytics tell a brand what it *did* sell. They can't see the secondary market —
which is exactly where surviving demand shows up, priced in real dollars, long after a drop
sells out. This project treats Grailed sold listings as that missing demand signal, then
isolates the pieces the market prizes far above the norm as candidate re-releases.

It's also a personal one: I've followed Foulplay since I was young, and wanted to point my
data-science training at a brand I actually care about.

## Key findings, in more detail

**1. Price stability (the baseline).**
Median sold price by year sits within a few dollars of $45 across the whole window. Rather than
force a "prices are rising" narrative the data doesn't support, the analysis reports the stability
honestly — and uses it as the reference line for detecting genuine outliers.

**2. Outlier detection (the centerpiece).**
Within each garment category, pieces are scored two ways that cross-check each other: a simple
"multiple of category median" ratio and a log-price z-score robust to the market's heavy right
skew. Both agree on the top pieces. Condition is held in view throughout, so a premium driven by
a pristine example is distinguished from one driven by pure demand for the design (the "You're
Being Robbed" hats command top dollar *while worn* — pure demand).

**3. Collab premium (a supporting cut).**
A keyword pass flags collaboration pieces and compares their sold prices to solo pieces,
quantifying the premium collabs retain on the secondary market.

## Method & data

- **Source:** Sold listings for Foulplay on Grailed (one resale channel), collected via the
  site's public search API. Reverse-engineered by inspecting the network requests the site's own
  front end makes, then querying that endpoint directly and paginating the results. Collection was
  done at a polite request rate for personal analysis.
- **Volume:** 736 sold listings spanning September 2021 – June 2026.
- **Cleaning** (`clean_data.py`): de-duplication, date parsing, splitting Grailed's encoded
  `type.value` category/size fields, condition normalization, and filtering out unrelated brands
  ("Foreplay"/"ForPlay") caught by fuzzy search.

### Honesty & limitations
Good analysis is explicit about what it can't claim:
- This is **Grailed only** — one channel, not the entire secondary market.
- `sold_price` is a real clearing price, but the seller's listing price is **not** the brand's
  retail price, so this data **cannot** measure true retail-to-resale premium.
- Yearly listing counts are an imperfect proxy for brand momentum and are read cautiously.
- The collab premium uses a title-keyword heuristic — directional, not a precise census.

*Note: The raw dataset and collection script are intentionally not committed to this repo, out
of respect for the platform's terms of service and the brand. The notebook's saved outputs
(charts and tables) let you read every result without re-running it.*

## Repo contents

| File | What it is |
|------|-----------|
| `Foulplay_Resale_Analysis.ipynb` | The full analysis, with rendered charts and written interpretation |
| `clean_data.py` | The cleaning/structuring step, documented |
| `requirements.txt` | Python dependencies |

## Tech

Python · pandas · NumPy · matplotlib · Jupyter

## Where this could go next

With a brand's first-party data, the same demand lens extends well past what resale can show:
true retail-to-resale premium, buyer-location mapping for pop-up planning, size-curve production
planning, and content-to-sales attribution linking social posts to orders.

---

*Daniel Rocha — M.S. Applied Statistics & Data Science, UCLA*

