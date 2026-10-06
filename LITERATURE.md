# Literature review: agent-driven accelerated AV testing (IEEE IV 2027)

Compiled 6 Oct 2026. Every entry was opened at the URL given unless marked. **[meta]** means the bibliographic data came from OpenAlex or an index page because the publisher page was blocked. Keys marked * already exist in `paper/refs.bib`.

## 1. Accelerated and adaptive stress testing

- **NADE**: Feng, Yan, Sun, Feng, Liu, *Nat. Commun.* 12:748 (2021). RL background vehicles make sparse adversarial moves on highways (cut-in, lane change, braking), and importance sampling keeps the estimate unbiased. Reaching relative half-width (RHW) 0.3 took about 500x and 6,000x fewer tests than the naturalistic environment (NDE). https://pmc.ncbi.nlm.nih.gov/articles/PMC7854639/ `feng2021nade`
- **D2RL**: Feng et al., *Nature* 615:620–627 (2023). Dense RL trains only on safety-critical states. Tested on highway, urban and roundabout simulation and augmented-reality track tests. Reaches RHW 0.3 10^3–10^5x faster than the NDE (156 tests against 2.5×10^7 at ACM). Author manuscript: https://par.nsf.gov/servlets/purl/10460886 `feng2023d2rl`
- **Importance sampling for cut-ins**: Zhao et al., *IEEE T-ITS* 18(3), 2017. Cut-ins sampled from skewed naturalistic statistics (cutting-in vehicle speed, range, TTC). Speed-up 2,000–20,000x. https://arxiv.org/abs/1605.04965 `zhao2017accelerated`
- **Scenario library generation**: Feng, Feng, Yu, Zhang, Liu, *IEEE T-ITS* 2020. Defines criticality as maneuver challenge × exposure frequency, a formal version of "most challenging". https://arxiv.org/abs/1905.03419 `feng2020tslg`
- **Rare-event simulation**: O'Kelly et al., NeurIPS 2018. Adaptive importance sampling on a full deep-learning AV stack, 2–20x faster than naive Monte Carlo. https://proceedings.neurips.cc/paper/2018/hash/653c579e3f9ba5c03f2f2f8cf4512b39-Abstract.html `okelly2018rare`
- **Adaptive Stress Testing (AST)**: Lee et al. (incl. Kochenderfer), *JAIR* 69 (2020). Finds the most likely failure by solving an MDP with MCTS. Also adds differential AST for regression testing. https://jair.org/index.php/jair/article/view/12190 `lee2020ast`
- **AST for AVs**: Koren, Alsaif, Lee, Kochenderfer, IEEE IV 2018 [venue: meta]. Pedestrian at a crosswalk. Deep RL finds more likely collisions than MCTS with fewer simulator calls. https://arxiv.org/abs/1902.01909 `koren2018ast`
- **Black-box safety validation survey**: Corso et al., *JAIR* 72 (2021). Covers falsification, most-likely failure and failure-probability estimation. https://jair.org/index.php/jair/article/view/12716 `corso2021survey`
- **Falsification tools**:
  - S-TaLiRo: Annapureddy et al., TACAS 2011. https://plv.colorado.edu/papers/staliro-tool-paper.html `annapureddy2011staliro`
  - Breach: Donzé, CAV 2010 [meta]. https://www-verimag.imag.fr/PEOPLE/donzeal/software/breach/ `donze2010breach`
  - Both minimise temporal-logic robustness.
  - VerifAI: Dreossi et al., CAV 2019. Falsification and fuzzing over Scenic programs. https://arxiv.org/abs/1902.04245 `dreossi2019verifai`
  - Scenic: Fremont et al., PLDI 2019. https://pldi19.sigplan.org/details/pldi-2019-papers/55/Scenic-A-Language-for-Scenario-Specification-and-Scene-Generation `fremont2019scenic`
- **Bayesian optimisation and surrogate search**:
  - Abeysirigoonawardena, Shkurti, Dudek, ICRA 2019 [meta]. BO raises collision risk with pedestrians and vehicles. https://api.openalex.org/works/doi:10.1109%2FICRA.2019.8793740 `abeysirigoonawardena2019adversarial`
  - Gangopadhyay et al., ITSC 2019. BO over hazard-derived parameters; abstract page only. https://wrap.warwick.ac.uk/139533/ `gangopadhyay2019bo`
  - Ben Abdessalem et al., ICSE 2018. NSGA-II plus decision trees on pedestrian AEB in PreScan. Finds 78% more distinct critical scenarios than the baseline. https://orbilu.uni.lu/bitstream/10993/33706/1/ICSE-Main-24.pdf `benabdessalem2018learnable`
  - SAMOTA: Haq, Shin, Briand, ICSE 2022. Surrogate-assisted many-objective search on CARLA. Beats NSGA-style and random search. https://conf.researchr.org/details/icse-2022/icse-2022-papers/150/Efficient-Online-Testing-for-DNN-Enabled-Systems-using-Surrogate-Assisted-and-Many-Ob `haq2022samota`
- **Surveys**:
  - Riedmaier et al., *IEEE Access* 8:87456–87477 (2020) [meta; publisher pages blocked]. https://doi.org/10.1109/ACCESS.2020.2993730 `riedmaier2020survey`
  - Zhang, Tao, Tan, Törngren et al. Covers 86 papers on critical-scenario identification. ArXiv version opened; published in *IEEE TSE* 2022 [meta]. https://arxiv.org/abs/2110.08664 `zhang2022critical`
  - Ding et al., *IEEE T-ITS* 2023. Splits methods into data-driven, adversarial and knowledge-based. Names five challenges: fidelity, efficiency, diversity, transferability, controllability. https://arxiv.org/abs/2202.02215 `ding2023survey`

## 2. Scenario categories and parameterisation

- **NHTSA pre-crash typology**: Najm, Smith, Yanagisawa, DOT HS 810 767 (2007). 37 scenarios cover 99.4% of light-vehicle crashes. Lead vehicle stopped is most frequent. Also includes LTAP/OD, straight crossing paths (SCP), lane change and pedestrian crossing. https://rosap.ntl.bts.gov/view/dot/6281 `najm2007precrash`
- **Euro NCAP AEB/LSS VRU v4.5** (Dec 2023; Wayback copy, since current links return 404). Pedestrian speed 5 km/h near side, 8 km/h far side, with VUT 10–60 km/h. CPLA: VUT 20–60 km/h. CPTA turning: VUT 10/15/20 km/h. Impact points 25/50/75%. https://cdn.euroncap.com/media/79884/euro-ncap-aeb-lss-vru-test-protocol-v45.pdf `euroncap2023vru`
- **Euro NCAP AEB Car-to-Car v4.3** (Dec 2023; Wayback).
  - CCRs/m/b rear-end: 5 km/h speed steps × 25% overlap. CCRb: 12/40 m headway, −2/−6 m/s².
  - CCFtap: VUT 10/15/20 × oncoming 30/45/60 km/h.
  - CCCscp: VUT 20–60 km/h or from a stop, crossing vehicle 20–60 km/h.
  - https://cdn.euroncap.com/media/79864/euro-ncap-aeb-c2c-test-protocol-v43.pdf `euroncap2023c2c`
- **Functional, logical and concrete scenarios**: Menzel, Bagschik, Maurer, IEEE IV 2018. A logical scenario is a set of parameter ranges. https://arxiv.org/abs/1801.08598 `menzel2018scenarios`
- **ASAM OpenSCENARIO XML 1.4.0** (May 2026). Scenarios can be parameterised for automated variation. https://www.asam.net/standards/detail/openscenario-xml/ `asam2026openscenario`

## 3. How acceleration is measured

- **Tests to a precision target**: tests needed to reach RHW 0.3 compared with NDE or naive Monte Carlo (NADE, D2RL, Zhao, O'Kelly).
- **Failures per budget**: distinct failure types found, and simulations until the first failure (LeGEND: simulation 11 on average). AV-Fuzzer (Li et al., ISSRE 2020, https://research.nvidia.com/publication/2020-10_av-fuzzer-finding-safety-violations-autonomous-driving-systems, `li2020avfuzzer`) finds 5 violation types where earlier tools find at most 2.
- **Diversity**: distinct critical regions; type exposure rate (LeGEND: 11.5% against 3.1% for random); Pareto hypervolume (EvoDrive).
- **Criticality**: TTC, PET and related measures are reviewed by Westhofen et al., *Arch. Comput. Methods Eng.* 2022. https://arxiv.org/abs/2108.02403 `westhofen2022criticality`. NeuroNCAP uses collision rate and impact speed.
- **Coverage**: listed as an open issue by Zhang et al.

## 4. LLMs in AV scenario generation and testing

- **ChatScene**: Zhang, Xu, Li, CVPR 2024. Text → retrieval → Scenic code in CARLA. Collision rate 15% higher than baselines against RL ego policies. https://arxiv.org/abs/2405.14062 `zhang2024chatscene`
- **LeGEND**: Tang et al., ASE 2024. GPT-4 turns accident reports into logical scenarios, followed by a multi-objective GA on Apollo/LGSVL. Finds 11 critical types against 2 for random search and 4 for AV-Fuzzer. https://arxiv.org/html/2409.10066v1 `tang2024legend`
- **TARGET**: Deng et al., *IEEE TSE* 51 (2025). Builds scenarios from traffic rules through a validated DSL. Exposed 610 issues across 7 ADSs. https://arxiv.org/abs/2305.06018v4 `deng2025target`
- **OmniTester**: Lu et al. (incl. Shuo Feng). Multimodal LLM with RAG and self-improvement in SUMO. Opened as arXiv; published in *Automotive Innovation* 2025 [meta]. https://arxiv.org/abs/2409.06450 `lu2025omnitester`
- **SoVAR**: Guo et al., ASE 2024. Accident reports → LLM extraction → constraint solving → Apollo. https://arxiv.org/abs/2409.08081 `guo2024sovar`
- **LEADE**: Tian et al., arXiv 2024. LMM seeds from traffic videos plus a GA, with the LLM used to escape local optima. https://arxiv.org/abs/2406.10857 `tian2024leade`
- **LLM-attacker**: Mei, Nie, Sun, Tian, *IEEE T-ITS* 2025. Multiple LLM agents pick adversarial vehicles. Training on its scenarios halves the collision rate. https://arxiv.org/abs/2501.15850 `mei2025llmattacker`
- **EvoDrive**: Nie et al., arXiv June 2026. Self-improving LLM actor-critic with a Pareto archive, in MetaDrive and CARLA. https://arxiv.org/abs/2606.03678 `nie2026evodrive`
- **PlannerForge**: Gao et al. (incl. Betz), EMNLP 2026. End-to-end LLM-agent testing pipeline, tested with 10 LLMs. Its scenarios cause 20.0% collisions against 6.1% for Scenario Factory 2.0. https://arxiv.org/abs/2609.08965 `gao2026plannerforge`*
- **AutoSimTest**: Duvvuru et al., ICSE 2025. Multi-agent LLM simulation testing of small drones on PX4/ArduPilot. https://arxiv.org/abs/2501.11864 `duvvuru2025autosimtest`*
- **LLM testing survey**: Zhao et al., *IEEE T-ITS* 2025. https://arxiv.org/abs/2505.16587 `zhao2025llmsurvey`
- **Neural-reconstruction simulators**:
  - NeuroNCAP: Ljungbergh et al., ECCV 2024. NeRF closed loop with Euro NCAP-style stationary, frontal and side scenarios, jittered, 100 runs each. UniAD and VAD collide 98–99% of the time in frontal scenarios without post-processing. https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/4335_ECCV_2024_paper.php `ljungbergh2024neuroncap`
  - HUGSIM: Zhou et al., arXiv 2024. 3DGS, 400+ scenarios. https://arxiv.org/abs/2412.01718 `zhou2024hugsim`
  - Abeysirigoonawardena et al., CoRL 2023. Adversarial scenarios found in a neural-rendering surrogate transfer to the real world. https://proceedings.mlr.press/v229/abeysirigoonawardena23a.html `abeysirigoonawardena2023transferable`
  - CARLA-GS: Huang, Ma, Ke, arXiv 2026. 3DGS plus LLM trajectory agents plus CARLA physics. https://arxiv.org/abs/2607.07601 `huang2026carlags`
  - AlpaSim: about 900 reconstructed 20-second scenes (NuRec/3DGUT). https://perspectives.nvidia.com/nvidia-alpamayo/task/faq/simulation-tools-autonomous-driving-stress-testing/ `alpasim`*

## 5. Gaps this paper can fill

1. **Validity of loop outputs.** TARGET validates its DSL and PlannerForge counts executable scenarios (193/200). Neither checks whether a finished run was physically plausible before counting its failure. Simulators are also nondeterministic:
   - 31.3% of CARLA benchmark scenarios are potentially flaky (Osikowicz, McMinn, Shin, FTW@ICSE 2025, https://conf.researchr.org/details/icse-2025/ftw-2025-papers/1/Empirically-Evaluating-Flaky-Tests-for-Autonomous-Driving-Systems-in-Simulated-Enviro, `osikowicz2025flaky`).
   - Flakiness skews randomised testing (Amini, Naseri, Nejati, *EMSE* 2023, https://arxiv.org/abs/2311.18768, `amini2023flaky`).
   - Game engines are seldom deterministic (Chance et al., *IEEE T-ITS* 2022, https://arxiv.org/abs/2104.06262, `chance2022determinism`).
   Our preflight, postflight and physics gates answer this.
2. **Reliability of the agent.** Variance across seeds and LLMs, rates of invalid proposals, and cost are rarely reported (PlannerForge is a partial exception).
3. **Search on an equal budget.** No paper compares rule-based, LLM-only and hybrid choice of the next test on the same simulation budget under the same validity filter.
4. **Real-scene simulators.** LLM testing work runs on CARLA, LGSVL, SUMO or MetaDrive. NeuroNCAP and the CoRL 2023 work use neural rendering but no LLM search. CARLA-GS uses an LLM but not a closed-loop end-to-end policy.
5. **Standard categories.** We can report results per NHTSA/Euro NCAP category with the parameters below.

## Scenario categories and parameters we could adopt

| Category | Typical parameters | Source |
|---|---|---|
| Urban car-following / lead vehicle stopped or braking | ego 10–80 km/h; lead speed; headway 12/40 m; lead decel −2 to −6 m/s²; overlap | Euro NCAP C2C v4.3 (CCRs/m/b); Najm 2007 |
| Unprotected left turn (LTAP/OD) | ego turn 10/15/20 km/h; oncoming 30/45/60 km/h; gap timing | Euro NCAP CCFtap; Najm |
| Merging / cut-in | cutting-in vehicle speed, range, TTC at lane change | Zhao 2017; NADE 2021 |
| Intersection crossing (SCP) | ego 20–60 km/h or from stop; crossing vehicle 20–60 km/h; arrival offset | Euro NCAP CCCscp; Najm |
| Pedestrian crossing | ego 10–60 km/h; pedestrian 5/8 km/h; impact point 25/50/75%; occlusion; pedestrian x, y, heading | Euro NCAP VRU v4.5; Ben Abdessalem 2018 |

## What reviewers will expect as baselines and metrics

- **Baselines on the same simulation budget (for example 50 runs per category):**
  - Random or Latin-hypercube sampling.
  - A Euro NCAP-style grid.
  - Gaussian-process Bayesian optimisation.
  - A GA or NSGA-II (AV-Fuzzer/LeGEND-style).
  - Rule-only and LLM-only versions of our loop, against the hybrid.
- **Efficiency:** valid failures against simulations run (any-time curve), simulations to the first failure, and quality of the top 5 (minimum TTC or distance, impact speed). Also report wall-clock time and LLM tokens or cost.
- **Diversity and coverage:** distinct failure clusters, and how much of the parameter space was covered.
- **Validity and reliability:** share of runs rejected by the gates, whether found failures reproduce on rerun, and results over several seeds and LLMs with confidence intervals and significance tests.
- **Acceleration claims:** quote an acceleration factor only against an explicit reference (random or naturalistic sampling). Otherwise call it relative efficiency.
