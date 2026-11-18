# Palm University College registration simulation

A deterministic simulation of one morning of undergraduate course registration at Palm University College, Manya Jorpanya. Student arrivals, processing times, and the number of officers and computers are fixed, so the same inputs always produce the same schedule.

The results page is live at https://deterministic-simulation-model.apps.grok.bot.

## Languages

| Part | Language | What it does |
| --- | --- | --- |
| `registration.py` and `registration_sim/` | Python | The simulation, the experiments, the tables, and the graphs |
| `index.html` and `output/figures/` | HTML and PNG, written by Python | The results page and its three graphs |
| `app/route.js`, `next.config.mjs`, `package.json` | JavaScript (Next.js) | Serves that results page so the live site can be published |

Matplotlib draws the graphs. Pytest checks the schedule against a hand-worked case. The Next.js files do not recalculate the simulation. They return the page Python already wrote.

## What the model represents

The college calendar sets course registration for a short week. About 100 undergraduates share that week, so one morning at the Registry is 20 students. They arrive every 8 minutes from 08:00. The desk is open for 240 minutes, until 12:00.

Each student takes the same three steps:

| Activity | Resource | Minutes |
| --- | --- | --- |
| Registry check | Registration officer | 6 |
| Student Portal course registration | Computer | 12 |
| Timetable issue | Registration officer | 4 |

An officer does the check and the timetable. A computer is used only for the Student Portal. A student moves to the next queue as soon as a step ends. If the needed officer or computer is busy, the student who has waited longest goes next.

## Run the simulation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python registration.py
```

Change the morning with `--students`, `--interarrival`, `--officers`, `--computers`, and `--session`. The three experiments keep that same group of students and only change the officers and the computers.

```bash
python registration.py --students 20 --officers 1 --computers 2
python -m pytest
```

The program prints the activity table, the single-run results, and the comparison of the three allocations. It writes:

- `output/figures/makespan_by_scenario.png`
- `output/figures/utilisation_by_scenario.png`
- `output/figures/students_within_period.png`
- `output/figures/scenario_comparison.csv`
- `index.html`, which you can open in a browser

## The three experiments

| Allocation | Officers | Computers | Total time | Finished by 12:00 | Overtime | Officer use | Computer use | Idle min. | System efficiency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Current desk | 1 | 1 | 250 min (12:10) | 19 / 20 | 10 min | 80.0% | 96.0% | 60 | 33.6% |
| Second officer | 2 | 1 | 250 min (12:10) | 19 / 20 | 10 min | 40.0% | 96.0% | 310 | 36.7% |
| Second computer | 1 | 2 | 204 min (11:24) | 20 / 20 | 0 | 98.0% | 58.8% | 172 | 45.3% |

All 20 students are processed in every experiment. The portal computer is the limit on the current desk. A second officer does not shorten the morning. A second computer finishes every student before noon and cuts the average wait from 43.4 minutes to 26.6 minutes.

The most efficient allocation is one officer and two computers, because it is the only one that finishes the whole group inside the working period.

## Class presentation

`presentation/Palm_University_College_Registration_Simulation.pptx` is a 15-slide deck of this project for the class. Each slide has speaker notes.

## How this meets the brief

- **a.** The model is a deterministic simulation. Arrivals, processing times, and resources are fixed.
- **b.** The resources are registry officers and Student Portal computers. The times are in the table above.
- **c.** `python registration.py --students 20` registers a chosen number of students.
- **d.** The comparison table gives the total time for each allocation.
- **e.** The second experiment adds an officer. The third adds a computer. The graphs show the effect on total time.
- **f.** Each run reports utilisation, students processed, idle time, and system efficiency. System efficiency is time being served divided by time being served plus time waiting.
- **g.** The program runs three allocations: the current desk, a second officer, and a second computer.
- **h.** The program names the most efficient allocation: one officer and two computers.
- **i.** The printed tables, the CSV file, the three graphs, and https://deterministic-simulation-model.apps.grok.bot present and interpret the results.
