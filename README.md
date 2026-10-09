# EAS 510 - Assignment 1: Digital Forensics Apprentice

A rule-based expert system that matches modified images back to their originals.

This is the **starter repository** for Project 1. Two repositories matter:

| Repository | Role |
|------------|------|
| `delveccj/EAS510_Assignment1_starter` (this repo) | Your **code** lives here. You will fork it, work in your fork, and push your final submission here. |
| `delveccj/EAS510_Assignment1` | The **dataset** (read-only). Clone it for the images; never commit it to your fork. |

## Setup on your Codio box

```bash
# 1. Fork this repo on GitHub, then in your box:
git clone https://github.com/YOUR-USERNAME/EAS510_Assignment1_starter.git
cd EAS510_Assignment1_starter

# 2. Clone the read-only dataset as a sibling folder (images live there):
cd ~/workspace
git clone https://github.com/delveccj/EAS510_Assignment1.git

# 3. Install dependencies:
cd ~/workspace/EAS510_Assignment1_starter
python3 -m pip install -r requirements.txt

# 4. Point this box at YOUR fork (run once):
./setup_git.sh
```

## Repository layout

```
forensics_detective.py   SimpleDetector: register targets + find_best_match
rules.py                 Rule functions (Rule 1: Metadata, Rule 2: Histogram, Rule 3: Template)
test_system.py           Runs the detector over the data folders and writes results_*.txt
scripts/check_output_format.py   Validates a results file against the required format
setup_git.sh, submit.sh  One-time setup + commit/push helper ("backup button")
```

## The task in one paragraph

Implement three interpretable rules (metadata, color histogram, template matching)
that combine into a 0-100 confidence score. Run your system on `modified_images/`
and `random/` and save the full output as `results_v1.txt`. In Phase 2, run on
`hard/`, diagnose a systematic failure, add a **Rule 4**, and save
`results_v1_hard.txt` and `results_v2.txt`. Full instructions are in the Codio guide
and in the assignment PDF in UBLearns.

## Running

```bash
# Phase 1 (easy + random) -> results_v1.txt
python3 test_system.py --modified --random --output results_v1.txt

# Phase 1 on hard cases -> results_v1_hard.txt
python3 test_system.py --hard --output results_v1_hard.txt

# Phase 2 (everything) -> results_v2.txt
python3 test_system.py --modified --hard --random --output results_v2.txt

# Validate any results file against the required format:
python3 scripts/check_output_format.py results_v1.txt
```

The data folders are resolved from a sibling clone of `EAS510_Assignment1`.
If your data is elsewhere, pass `--data-dir /path/to/EAS510_Assignment1`.

## Output format (do not alter)

```
Processing: modified_image_01.jpg
Rule 1 (Metadata): FIRED - Size ratio 0.85 -> 20/30 points
Rule 2 (Histogram): FIRED - Correlation 0.92 -> 25/30 points
Rule 3 (Template): FIRED - Match score 0.76 -> 30/40 points
Final Score: 75/100 -> MATCH to original_03.jpg
```

## Backup doctrine

Your Codio box can be reset at any time. **Your fork on GitHub is the only safe
copy.** After every milestone run `./submit.sh "describe what you did"`. A box
restart never touches GitHub.

## License

Apache 2.0. See `LICENSE`.
## My notes
Student: radyagnik. Work in progress for Project 1.
Setup complete: git identity configured.

## Observed weakness in V1: what failed and why
the crop combinations of v1 and v2 matched 0 out of 10 images each and crops matched only 5 out of 30 overall 
like original_09__crop_keep60__bright__compress__q40__v2.jpg scored 16 cropping probably also affects how the template is aligned with the image so it makes rules 1-3 less effective 
## Design decision for V2: what Rule 4 is and why you chose it
rule 4 finds distinctive features in the image and checks that they line up consistently, which works even when the image is cropped. rules 1-3 did poorly on crops so I gave rule 4 40 of the 100 points and cut rules 1-3 to 15, 15 and 30  
## Effect of the change: accuracy before/after on easy vs hard
accuracy improved from 31 out of 60 to 50 out of 60 on the easy set. on the hard set it improved from 29 to 56 out of 60 so the hard test improved more. the highest random score dropped from 48 to 31 with no wrong matches 
## Trade-offs: what new costs or risks did Rule 4 introduce
one limitation is that the image can still fail to match even if rule 4 detects similar features like ..._q40__v2 scored 32 out of 100 because only rule 4 contributed, since matching cutoff is 50 the image was not matched, also the modified_00_crop_25pct.jpg had a keypoint score of only 0.13 under rule 4, shows that feature matching can also fail when too much of the original img is removed (so it cannot guarantee that every crop will be recognized) 
