# Outline

IEEE IV 2027. Six pages, including figures, tables, and references. Deadline
15 Nov 2026. Rewritten 29 Sep 2026 for the system as it now stands. Every
sentence below cites a file; a claim with no file is in the left-out list.
Numbers marked (n=1) are single samples until the campaign and
`auditor_repeats.json` replace them.

## Claim

An LLM can operate an unattended simulation batch without being trusted.
Deterministic checks decide which runs enter the dataset; the model only
proposes: recoveries from a finite menu, quarantine flags on a finished batch,
and new checks. A proposal takes effect only after a verified gate or the data
admits it. Because the menu is finite, the gate is checked exhaustively
against every answer a policy could give. What the model learns becomes code,
so the batch gets safer and cheaper to run.

Working title: *Runtime assurance for LLM-operated simulation: the model
proposes, the gate decides.*

## Figure 1: architecture (`research/harness/`)

Simplex layout. Left, the trusted path: preflight (`preflight.py`, machine check
`environment.py`), launch (`run_experiment.py`), postflight (`postflight.py`,
landed check and promoted rules in `read_state.py`), the state machine
(`loop.py`). Right, the untrusted proposers: tier 1 diagnosis on FAILED
(`diagnose.py --policy agent`, read-only tools), tier 2 batch audit
(`audit.py`), rule proposals. Between them, the gates: `validate_diagnosis.py`
for recoveries, `promote.py` for rules, a person for enacting rules.

## Pages

**1. Introduction.** Unattended batches fail silently. Our own earlier data had
four such failures (`RESULTS.md`): `context_length` 1 made VaVAM crash in 8 of
10 runs; a latency plot used a delay the simulator never applied (162 of 212
rows); 22% of runs wrote no metrics; the MPC reported `solved` whenever it did
not throw. None of them raised an error. Contributions: the gate and its
exhaustive check, a diagnosis agent on a fenced menu, a batch auditor, and
rule mining that turns what the auditor finds into checks.

**2. The gate (Loop 1).** States READY, RUNNING, COMPLETE, FAILED, DONE
(`read_state.py`). A run is kept only after preflight, the machine check, exit
0, postflight, the landed check, and every promoted rule. The menu: CONFIGURE
(how a run executes: `context_length`, `scene_file`, `trafficsim_device`),
RE-RUN, RESTART_CLEANUP, CLEANUP_ENV, HALT. `validate_diagnosis.py` rejects
anything else. Recovery may never change what a run measures.

**3. Verification (`verify_supervisor.py`, FACTS.md).** An adversarial policy
tries 26 answers at every FAILED state against a world that fails every launch.
The first run found a hole: CONFIGURE of the delay let a recovery keep a run
measuring 0 ms under a 100 ms experiment, lie 2 reintroduced. After removing
the delay from CONFIGURE: 0 violations over 3,822 transitions; at most 3
launches per run; no cycles. This is the section a controls reader will check.

**4. Unattended operation (B2, `b2_trace.jsonl`).** 150 runs, 537 min, 150 kept,
0 halted. The only failures were a Docker network leak from 29 earlier runs; a
per-run cleanup could not fix it, a person did. The leak led to the machine
check and CLEANUP_ENV, which fix it with no person (replayed with
`faults.fill_network_pool`). The auditor later found the same leak in the old
autolab batch. Multi-scene: S1, 101 scenes (`s1_trace.jsonl`, running).

**5. Diagnosis: script, tier 0, tier 1 (`comparison_opus.txt`, C0, campaign).**
On three real failures both model tiers choose the fix a person applied where
the script re-runs; the larger menu made that difference, not the tools. In
the pilot campaign (C0) tier 1 halted a persistent failure after one launch
where the script would spend three, and halted a transient hang it should have
retried. Table: per fault kind, detected / recovered / launches / halted, for
script, tier 0, tier 1, and the no-gate arm (`score_campaign.py`). The pilot
has n=1 per fault; the campaign fills this table.

**6. The auditor and what it teaches the gate (`auditor_eval.txt`,
`mining_eval.txt`).** Table 2: batches A–F. It caught every planted lie with no
false flags in A–D and F, and none in E, the batch that is wrong the same way
throughout, as lie 1 really was. One reference run restores detection (F).
Table 3: rules it proposed and `promote.py` admitted, applied with no model
call to held-out batches: `context_length` catches E 10/10, the delay rule
20/20, the controller rule catches kinematic but not rails. Zero false flags
on 30 clean runs.

**7. Related work and limits.** Simplex and runtime assurance (Sha 2001;
Black-Box Simplex; shielding): we move the idea from physical safety to
experimental validity. Closest: ADMITBench and the Mercangöz group's
fault-tolerant control agent (a gate around LLM advice, physical plants);
agentic self-healing pipelines (no rule baseline, no validity guarantee);
AgentSpec and ShieldAgent (free-form actions); TrainCheck and RADAR (silent
failures, not simulation configs). IDs in `FACTS.md`. Limits: one simulator,
one driver, silent faults the auditor misses (rails), a study-specific rule.

## Numbers still to produce

- Campaign: 10 per fault kind × script, tier 0, tier 1 (`enqueue_campaign.py`,
  `score_campaign.py`). Replaces every n=1 in section 5.
- `auditor_repeats.json`: three samples per auditor batch (running).
- S1: which of 101 scenes run, and the failures the loop met on real scenes.
- An S1 audit with one reference run.

## Left out

The files do not support these; they are not in the six pages.

- The model beating the script in general. It chose better on three real
  failures and one persistent fault, and worse on one transient fault.
- "First runtime assurance for LLM agents." It is in print (FACTS.md).
- The auditor catching uniform lies without a reference run (E is 0/10).
- Rails caught by a mined rule. Held out 1/2.
- A rate for any model behaviour from one sample.
- Loop 2 as a search over scenes, delays, or gains.
- Switching stability, dwell time, MPC tuning.
- The 12 GB out-of-memory event as the paper's failure mode.
