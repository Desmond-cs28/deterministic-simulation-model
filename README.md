# Palm University College registration desk

A deterministic simulation of one morning of undergraduate course registration at Palm University College, Manya Jorpanya. Arrivals, processing times, and the number of officers and computers are fixed, so the same inputs always produce the same schedule.

The Python program is the simulation. The web page runs the same model and draws the timeline, the comparison table, and the graphs.

## The morning

The college calendar sets undergraduate course registration for a short week (31 August to 4 September 2026 for the first cohort). The college has a little over 100 undergraduates, so one morning at the Registry is a group of 20. They are booked every 8 minutes from 08:00. The desk is meant to close at 12:00, which is 240 minutes.

Each student takes three steps:

| Step | Resource | Minutes |
| --- | --- | --- |
| Registry check | Registry officer | 6 |
| Student Portal course registration | Computer | 12 |
| Timetable issue | Registry officer | 4 |

That is 10 minutes with an officer and 12 minutes on a computer. The officer handles both the check and the timetable. The computer is only for the Student Portal. A student moves to the next queue as soon as a step ends, so the officer can call the next student while an earlier student is still on the computer.

## Three experiments

| Allocation | Officers | Computers | Makespan | Finished by 12:00 | Overtime | Officer use | Computer use | System efficiency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Current desk | 1 | 1 | 250 min (12:10) | 19 / 20 | 10 min | 80.0% | 96.0% | 33.6% |
| Second officer | 2 | 1 | 250 min (12:10) | 19 / 20 | 10 min | 40.0% | 96.0% | 36.7% |
| Second computer | 1 | 2 | 204 min (11:24) | 20 / 20 | 0 | 98.0% | 58.8% | 45.3% |

The portal computer is the limit on the current desk. A second officer does not change the finish time, and officer utilisation falls from 80% to 40%. A second computer brings the last student forward by 46 minutes and clears all 20 before noon. Average waiting falls from 43.4 minutes to 26.6 minutes.

The most efficient allocation in this study is one officer and two computers. It is the only one that finishes the whole group before the desk closes.

## Run the Python program

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m registration_sim
python3 -m registration_sim --charts output/figures
python3 -m pytest
```

## Run the page

```bash
npm install
npm run dev
```

The page listens on port 3847. `npm run parity` checks the page's engine against `tests/fixtures/parity.json`.

## What the project asks for

- The model is deterministic: arrivals, times, and resources are fixed.
- Resources and times are the table above.
- `python3 -m registration_sim --students 20` registers a chosen group.
- The three experiments give the total time under different allocations.
- Adding an officer and adding a computer are reported separately.
- The report includes students processed, utilisation, idle time, and system efficiency.
- The comparison names the most efficient allocation and is shown as a table and as graphs.
