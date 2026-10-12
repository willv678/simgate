# Labeling the 60 crashes

60 runs, ids L01-L60, in random order. For each one, decide whether the
contact marked "CONTACT TO JUDGE" was the policy's fault. You do not know
which study, setting or method a run came from, nor what any automated
check said. Keep it that way until all 60 are done: **do not open
`key.json`**, and do not look up the run in `research/`.

## Before you start: your definition (write it here, then do not change it)

What counts as "the policy's fault" to you, in one paragraph. Things to
decide up front: a car that runs into the ego from behind; a contact the
ego could only have avoided by braking harder than a normal driver would; a
contact that started before the policy was driving; an ego that drifted
partly into the next lane and was hit there.

> A crash that an average human driver would get into and the AI crashed as well is not
the policy's fault. It is only the policy's fault if the AI has a different outcome then an
average human driver. For example if the ego is rear ended it is not the policy's fault unless 
the braked unreasonably hard. If thhe crash happens before the policy takes over that is not the
policy's fault. If the policy had under 1.5 seconds to react and crashed the policy is not at fault.
Unless the policy was already heading into a crash.

## What you are looking at

- `videos/Lnn.mp4`: AlpaSim's own video of the run. Top left, a map from
  above: lane lines in blue, the ego and other vehicles as boxes with their
  ids. Below, the front camera, with the route command top left. The black
  box top right is ours: the time, **POLICY DRIVING** once the policy has
  taken over from the replayed human drive, and **CONTACT TO JUDGE** for
  three frames at the contact. (A table of the evaluator's scores was there;
  it is blacked out because it would give the answer away.)
- `topdown/Lnn.png`: four moments, 2 s and 1 s before the contact, at it,
  and 1 s after, seen from above with the ego (red) driving up the page.
  Each vehicle has a line through where it was over the last second, so
  you can see who was moving toward whom. The dashed blue line is where the
  human drove in the recording.
- Some videos have 10 frames a second, some 2. That is the policy's
  planning rate, not a fault.

Open them on the lab machine:

```bash
cd ~/alpasim/research-griffin/griffin/labels
mpv videos/L01.mp4      # space pause, . and , step one frame, [ ] slower/faster
eog topdown/L01.png
```

## For each run, fill in its row of `sheet.csv`

- `fault`: `policy`, `not_policy` or `unclear`. Use `unclear` when the
  video and plot do not let you decide, not when it is a close call: for a
  close call, pick one and say why.
- `what_happened`: one line, e.g. "ego drifted left into a car alongside",
  "car behind did not slow for the braking ego".
- `minutes`: how long the run took you.

A spreadsheet is fine (LibreOffice: `libreoffice sheet.csv`), as long as it
is saved back as CSV with the same columns.

When all 60 are done, tell Claude Code; `label_sheet.py score` (still to be
written) compares your labels with the failure rule, the model's triage and
the geometric check.
