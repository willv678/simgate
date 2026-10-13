# Figure survey: scenario-based AV testing papers (IV / ITSC / T-IV), for IV 2027 planning

**Method.** I read each paper's own figure and table captions in its arXiv HTML. Figures marked **[viewed]** I also opened and looked at as images (about 30 figures). Nothing below comes from an abstract alone. The arXiv comment field confirms the venue for every paper except #13.

## Papers and their figures

1. **ARISE: Adaptive Refinement and Iterative Scenario Engineering.** Poddubnyy et al., **IV 2026**. [arXiv 2601.14743](https://arxiv.org/abs/2601.14743)
   - F1: LLM-generated scenario rendered in CARLA (camera view).
   - F2 **[viewed]**: pipeline diagram (extraction → snippet retrieval → script assembly → test-and-repair loop). Real prompt and code text sits inside the boxes.
   - F3 **[viewed]**: 3-frame strip of chase-camera CARLA renders, with ego and adversary marked by boxes.
   - T1–T4: execution and repair success rate vs. temperature (against the ChatScene baseline); semantic-conformity scores per LLM; SafeBench collision rate and red-light / stop-sign violations.
2. **Chat2Scenario.** Zhao et al., **IV 2024**. [2404.16147](https://arxiv.org/abs/2404.16147)
   - Web-app screenshot; framework schematic; scenario-classification tree.
   - Trajectory plots with matching CarMaker 3D renders **[viewed]**.
   - LLM prompt box; criticality-window illustration; OpenSCENARIO and CarMaker file excerpts.
   - 4 tables: dataset fields, criticality metrics, extracted examples, accuracy.
3. **Determining the Tactical Challenge of Scenarios to Efficiently Test ADS.** Vater et al., **IV 2024** (6 pages, 3 figures, 2 tables). [2404.02599](https://arxiv.org/abs/2404.02599)
   - Process diagram; reachability graph.
   - **[viewed]** stacked lane-vs-position (s-coordinate) strips with decision-time windows.
   - Parameter table; results table.
4. **Augmenting Safety-Critical Driving Scenarios…** Mirkhani et al., **IV 2024**. [2404.13347](https://arxiv.org/abs/2404.13347)
   - Trajectory-synthesis schematic; autoencoder architecture; t-SNE clusters.
   - Bar charts of cluster share before and after augmentation.
   - **[viewed]** closed-loop top-down frame strips with fail/pass icons.
   - 2 tables of closed-loop metrics.
5. **(Re)²H2O.** Niu et al., **IV 2023**. [2302.13726](https://arxiv.org/abs/2302.13726)
   - **[viewed]** top-down highway snapshots with ego in red and background vehicles in yellow.
   - Collision-distance histogram; training curves (reward, speed); illustrative risk-escalation example.
   - Baseline-comparison table.
6. **Behavior-Centric Scenario Extraction and Clustering (CVQ-VAE).** Roßberg et al., **IV 2026**. [2603.16964](https://arxiv.org/abs/2603.16964)
   - 2 method diagrams; augmented-scenario BEV.
   - 2 tables: detection metrics, cluster purity.
7. **From Words to Collisions.** Gao, Piccinini, Moller, Alanwar, Betz, **ITSC 2025**. An earlier version was labelled IV 2025; the final version says ITSC. [2502.02145](https://arxiv.org/abs/2502.02145)
   - Concept figure; **[viewed]** framework block diagram with an evaluation band and a generation band.
   - **[viewed]** planner sampling fan (green feasible / red infeasible).
   - Prompt parser outputs shown as colored text.
   - Confusion matrices: LLM collision and safety judgments vs. ground truth.
   - Risk score of the attacker trajectory, original vs. generated.
   - **[viewed]** 2×3 BEV grid: safe original (top row) vs. generated collision (bottom row), same timesteps, dashed zoom box.
   - 4 ablation and LLM-comparison tables.
8. **Seeking to Collide** (online LLM + retrieval scenario generation). Mei, Nie, Sun, Tian, **ITSC 2025**. [2505.00972](https://arxiv.org/abs/2505.00972)
   - Challenge illustration; **[viewed]** method diagram with the actual prompt skeleton.
   - Confusion matrix of the LLM behavior classifier.
   - **[viewed]** "current state → LLM output → raw vs. safety-critical" BEV panels.
   - **[viewed]** speed and acceleration histograms, raw vs. generated.
   - Example of a newly discovered behavior.
   - 1 method-comparison table.
9. **Adversarial Safety-Critical Scenario Generation using Naturalistic Human Driving Priors.** Hao et al., **T-IV 2023**. [2408.03200](https://arxiv.org/abs/2408.03200)
   - This is a journal paper, so it has 17 figures.
   - CARLA collision-type images; framework and network diagrams.
   - Road reconstructions from the datasets; calibration and loss curves.
   - Statistical comparison plots; examples of generated scenarios; collision-direction plot; clustering plot.
   - 4 tables.
10. **SOTIF-Compliant Scenario Generation (semi-concrete scenarios + parameter sampling).** Birkemeyer et al., **ITSC 2023** (6 pages).
    - Feature-model diagrams.
    - **[viewed]** box plots of test effectiveness (mutation score) for each sampling strategy, "pure random" vs. "with feedback". 0 tables.
11. **Clustering-based Criticality Analysis.** Schütt, Otten, Sax, **ITSC 2023**. [2306.12738](https://arxiv.org/abs/2306.12738)
    - Abstraction-level diagram, activity diagram, class diagram, scenario sketches.
    - **[viewed]** 3D kernel-space projections.
    - 2D parameter scatters (ego_x × delay) colored by cluster and by worst-case time-to-collision (WTTC).
12. **ANTI-CARLA.** Ramakrishna et al., **ITSC 2022**. [2208.06309](https://arxiv.org/abs/2208.06309)
    - Overview and framework diagrams; meta-model; spec-file excerpt; glue-code illustration; track map.
    - **[viewed]** camera screenshots of failing test cases, each captioned with its parameter values.
    - Infraction bar charts per town and per controller.
    - **[viewed]** side-by-side 3D scatter of the parameter space (time-of-day × precipitation × cloud), failed in red vs. passed in blue, random search vs. guided search.
    - 1 table of sampler statistics.
13. **Bayesian Optimization for Accelerated Virtual Validation.** Awasthi et al., arXiv 2025, venue not stated (12 pages). [2507.22769](https://arxiv.org/abs/2507.22769)
    - Loop diagram; scene sketches.
    - **[viewed]** 3D parameter grid (v_ego × v_lead × gap) colored by maximum lateral displacement; the same axes with seed points vs. BO-acquired points.
    - DBSCAN clusters.
    - **[viewed]** box plots of the number of simulations needed to first find each critical cluster, per acquisition-function × metric pairing.
14. **High-Dimensional Fault Tolerance Testing (low-rank models).** Mei et al., **ITSC 2024**. [2407.21069](https://arxiv.org/abs/2407.21069)
    - Problem illustration.
    - **[viewed]** heatmap grids (fault time × magnitude) of the safety indicator: ground truth vs. 6 surrogate models.
    - Metric-vs-sparsity curves; sensitivity plots.
    - 3 tables.

Context (not IV, but closest to our neural-reconstruction setting): **NeuroNCAP**, ECCV 2024, [2404.07762](https://arxiv.org/abs/2404.07762).
- **[viewed]** grid of real-scene camera frames (original vs. injected stationary, frontal and side actors; time runs downward).
- **[viewed]** top-down scenario schematics.
- Planner output overlaid on the camera image.
- 3 tables.

## What recurs (14 papers above)

| Figure type | Papers |
|---|---|
| Framework / pipeline block diagram | 14 (a feature-model or concept diagram in a few) |
| Method × metrics comparison table | ~10 |
| BEV / top-down scenario snapshots, often as time strips | ~10 |
| Rendered or camera-view scenario frames | 6 |
| LLM prompt or output text inside a figure, or spec / OpenSCENARIO excerpts | 6 |
| Parameter-space scatter or heatmap of failure regions | 4 (ANTI-CARLA, BO, Clustering, Fault-testing) |
| Histograms of kinematics or other distributions | 4 |
| Search-efficiency plots (runs-to-first-failure or effectiveness per strategy, as box plots) | 2 (BO, SOTIF) |
| Confusion matrix of LLM judgments vs. ground truth | 2 (both LLM papers) |
| t-SNE / embedding cluster plots | 3 |
| Per-category bar charts | 2 |

**Typical figure budget.** Across the 11 conference papers the median is about **6 figures and 2 tables**, ranging from 3 to 10 figures and 0 to 4 tables. The verified 6-page ones are small: 3 figures + 2 tables (Tactical) and 3 figures + 0 tables (SOTIF). Most figures have several panels.

**What reviewers clearly expect:**
- a framework diagram as Fig. 1 or Fig. 2;
- at least one qualitative scenario figure (BEV and/or camera frames) showing the found failure;
- a methods × metrics table.
- LLM papers also add a figure showing what the LLM actually received or produced, and validate the LLM's judgments with a confusion matrix.

**Gap.** None of the papers I opened has a cumulative "failures found vs. number of simulations" curve. The closest are BO's box plots of simulations-to-first-critical-case and SOTIF's per-strategy box plots. A clean sample-efficiency curve would set our paper apart.

**What the best papers do visually:**
- Words2Collisions pairs the safe original row against the generated collision row at the same timesteps.
- ANTI-CARLA plots random and guided search on identical axes with a pass/fail color code.
- BO separates seed points from acquired points with different marker edges inside the parameter space.
- NeuroNCAP shows the real scene next to the injected actor across time.
- The fault-testing paper puts small-multiple heatmaps on a single shared colorbar.

## Recommended figures for our paper (5 figures + 2 tables)

1. **Fig. 1, agent loop diagram.** Written question → study plan → strategy (rules / LLM / hybrid / random / Optuna) → AlpaSim run → validity checks (physics, config landed) → self-heal skill menu → crash explanation. Mark which steps are the LLM and which are deterministic, and annotate the arrows with run counts.
2. **Fig. 2, hardest confirmed crash vs. nominal.** Top row: camera frames from the neural reconstruction. Bottom row: BEV with ego and actor trajectories, the collision marked, and the knob values in the caption. Use the same timesteps as the nominal run.
3. **Fig. 3, search efficiency (the headline result).** Cumulative confirmed crashes, or best severity / minimum TTC so far, against the number of runs for each strategy. Show the median with an interquartile band across seeds, plus an inset box plot of runs to the first confirmed crash.
4. **Fig. 4, parameter-space map.** 2D scatter of actor timing × ego speed with pass / confirmed-crash / invalid as color and strategy as marker shape. This shows where each search spends its runs.
5. **Fig. 5, the left-drift failure mode.** Lateral offset over time for drift cases vs. nominal, with lane boundaries drawn in, and a small BEV overlay of the drifting trajectories.
6. **Table I, strategies × metrics.** Runs, valid-run rate, confirmed crashes, distinct failure clusters, severity of the hardest case, LLM tokens/cost, wall-clock time.
7. **Table II, operational issues and self-healing.** Issue class → count → recovery skill → success rate, plus how many runs the validity checks rejected (the "false crashes" they caught). If we have human labels, a small confusion matrix of the agent's crash explanations against them would match what the LLM-testing papers show.
