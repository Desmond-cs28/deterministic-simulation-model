# North Hall registration simulator

Deterministic discrete-event simulation of a university registration centre, for a computer-simulation course. Arrivals, processing times, and resource counts are fixed. The same inputs always produce the same schedule.

The Python program is the simulation. The web lab runs the same model and draws the tables and graphs.

## The hall

Ashworth University opens North Hall at 08:00 for a 240-minute session. A cohort of 36 students arrives every 3 minutes. Each student passes four activities:

| Activity | Resource | Minutes |
| --- | --- | --- |
| Document verification | Registration officer | 6 |
| Course enrolment | Computer | 10 |
| Fee assessment | Registration officer | 5 |
| Card and timetable | Computer | 4 |

That is 11 officer-minutes and 14 computer-minutes per student. Officers are one shared pool. Computers are one shared pool. A student who finishes an activity joins the next queue immediately, so an officer can call the next student while an earlier student is still at a computer. The lowest-numbered free unit is used. The longest-waiting student is seated first.

Forms, chairs, and the network are treated as unlimited. Work still open at the end of the session continues, and the extra time is overtime.

## Measures

- **Makespan** — minutes from opening until the last student finishes.
- **Students processed** — students who complete all four activities.
- **Finished in session** — completions at or before the session length.
- **Utilisation** — busy minutes ÷ (units × makespan).
- **Idle time** — resource-minutes with no student, up to the makespan.
- **Service efficiency** — processing ÷ (processing + waiting).
- **Schedule efficiency** — a resource lower bound ÷ makespan.
- **Efficiency score** — (students finished in session ÷ cohort) × overall utilisation.

The ranking clears as many students as possible before the session closes, then keeps the highest overall utilisation. A larger pool is chosen only when those extra desks still earn their time.

## Default study

Cohort 36, arrival every 3 minutes, session 240 minutes.

| Scenario | Officers | Computers | Makespan | In session | Overtime | Officer util. | Computer util. | Score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline hall | 2 | 2 | 261 | 25 / 36 | 21 | 75.9% | 96.6% | 0.599 |
| Extra officers | 4 | 2 | 261 | 25 / 36 | 21 | 37.9% | 96.6% | 0.399 |
| Lean computer step | 2 | 3 | 205 | 36 / 36 | 0 | 96.6% | 82.0% | 0.878 |
| Extra computers | 2 | 4 | 205 | 36 / 36 | 0 | 96.6% | 61.5% | 0.732 |
| Work-balanced mix | 3 | 4 | 147 | 36 / 36 | 0 | 89.8% | 85.7% | 0.875 |
| Both pools doubled | 4 | 4 | 143 | 36 / 36 | 0 | 69.2% | 88.1% | 0.787 |

Computers are the scarce pool in the baseline hall. Adding officers, and holding computers at two, leaves the makespan at 261 minutes. Adding one computer, to three, shortens the makespan by 56 minutes and clears the whole cohort inside the session. A fourth computer leaves the makespan at 205 minutes, because the two officers are then the limit.

**Most efficient allocation in the study: 2 officers and 3 computers** (score 0.878). It clears 36 of 36 students with the least combined officer-time and computer-time.

The work-balanced mix (3 officers, 4 computers) is close on the score (0.875) and is the one to staff when queues matter: average waiting falls from 55.4 minutes to 14.9 minutes, and the hall finishes at 147 minutes.

Figures for this study are in `output/figures/`.

## Run the Python program

```bash
python3 -m registration_sim
python3 -m registration_sim --students 40 --officers 3 --computers 4 --session 240
python3 -m registration_sim --charts output/figures
python3 -m pytest
```

Dependencies are listed in `requirements.txt` (`matplotlib` for the figures, `pytest` for the tests).

## Run the web lab

```bash
npm install
npm run dev
```

The lab listens on port 3847. Use it to change the cohort, open each allocation, and read the timeline, comparison table, and sensitivity grid. `npm run parity` checks the TypeScript engine against `tests/fixtures/parity.json`, which is written by:

```bash
python3 -m registration_sim --export-parity tests/fixtures/parity.json
```

## Where the project tasks live

| Task | Where |
| --- | --- |
| a. Deterministic model | `registration_sim/engine.py`, model section of the lab |
| b. Resources and processing times | `registration_sim/activities.py` |
| c. Python program | `python3 -m registration_sim` |
| d. Total time under different allocations | Experiment table, makespan column |
| e. Effect of more officers and computers | Sensitivity grid and line chart |
| f. Utilisation, students processed, idle time, efficiency | Metrics in `registration_sim/metrics.py` and the glossary |
| g. At least three experiments | Six named scenarios |
| h. Most efficient strategy | Ranking in `registration_sim/experiments.py`, reading section |
| i. Tables and graphs | Lab charts, and `output/figures/*.png` |
