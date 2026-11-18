"""Build the 15-slide class presentation for the registration simulation."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / "output" / "figures"
LOGO = Path(__file__).resolve().parent / "puc-logo.png"
OUTPUT = Path(__file__).resolve().parent / "Palm_University_College_Registration_Simulation.pptx"

DEEP = RGBColor(0x01, 0x33, 0x26)
GREEN = RGBColor(0x02, 0x55, 0x3C)
PAPER = RGBColor(0xF3, 0xF6, 0xF2)
INK = RGBColor(0x14, 0x24, 0x1C)
MUTED = RGBColor(0x3D, 0x53, 0x48)
GOLD = RGBColor(0xC4, 0xA3, 0x5A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
MINT = RGBColor(0xD7, 0xEB, 0xE3)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xC9, 0xDD, 0xD3)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
FONT = "Calibri"
SLIDE_COUNT = 15


def _set_run(run, text, size, color, bold=False):
    run.text = text
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color


def add_text(slide, left, top, width, height, text, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    shape = slide.shapes.add_textbox(left, top, width, height)
    frame = shape.text_frame
    frame.word_wrap = True
    frame.auto_size = None
    frame.margin_left = Emu(0)
    frame.margin_right = Emu(0)
    frame.margin_top = Emu(0)
    frame.margin_bottom = Emu(0)
    try:
        frame._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor])
    except Exception:
        pass
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    _set_run(paragraph.add_run(), text, size, color, bold)
    return shape


def add_lines(slide, left, top, width, height, lines, size=18, color=INK, spacing=8):
    shape = slide.shapes.add_textbox(left, top, width, height)
    frame = shape.text_frame
    frame.word_wrap = True
    frame.margin_left = Emu(0)
    frame.margin_right = Emu(0)
    for index, line in enumerate(lines):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.alignment = PP_ALIGN.LEFT
        paragraph.space_after = Pt(spacing)
        content = line[1:] if line.startswith("• ") else line
        prefix = "•  " if line.startswith("• ") else ""
        _set_run(paragraph.add_run(), prefix + content, size, color, False)
    return shape


def rect(slide, left, top, width, height, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def round_rect(slide, left, top, width, height, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = LINE
    shape.shadow.inherit = False
    shape.adjustments[0] = 0.08
    return shape


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def content_slide(prs, number, kicker, title):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, 0, 0, SLIDE_W, SLIDE_H, PAPER)
    rect(slide, 0, 0, SLIDE_W, Inches(0.12), DEEP)
    add_text(slide, Inches(0.5), Inches(0.28), Inches(10), Inches(0.28), kicker, 12, GREEN, True)
    add_text(slide, Inches(0.5), Inches(0.52), Inches(12.3), Inches(0.55), title, 28, INK, True)
    rect(slide, 0, Inches(7.22), SLIDE_W, Inches(0.28), DEEP)
    add_text(slide, Inches(0.45), Inches(7.24), Inches(9), Inches(0.24), "Palm University College  ·  Computer Simulation Project 2", 11, WHITE)
    add_text(slide, Inches(11.4), Inches(7.24), Inches(1.5), Inches(0.24), f"{number}  /  {SLIDE_COUNT}", 11, WHITE, align=PP_ALIGN.RIGHT)
    return slide


def style_cell(cell, text, size, color, fill, bold=False, align=PP_ALIGN.LEFT):
    cell.text = ""
    cell.fill.solid()
    cell.fill.fore_color.rgb = fill
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = Inches(0.08)
    cell.margin_right = Inches(0.06)
    paragraph = cell.text_frame.paragraphs[0]
    paragraph.alignment = align
    _set_run(paragraph.add_run(), text, size, color, bold)
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    for edge in ("lnL", "lnR", "lnT", "lnB"):
        line = tc_pr.find(qn(f"a:{edge}"))
        if line is not None:
            tc_pr.remove(line)
        element = tc_pr.makeelement(qn(f"a:{edge}"), {"w": "6350", "cap": "flat", "cmpd": "sng", "algn": "ctr"})
        fill = element.makeelement(qn("a:solidFill"), {})
        colour = fill.makeelement(qn("a:srgbClr"), {"val": "C9DDD3"})
        fill.append(colour)
        element.append(fill)
        tc_pr.append(element)


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    prs.core_properties.title = "Deterministic simulation of course registration at Palm University College"
    prs.core_properties.author = "Desmond"
    prs.core_properties.subject = "Computer Simulation Project 2"
    _title(prs)
    _problem(prs)
    _approach(prs)
    _setting(prs)
    _activities(prs)
    _rules(prs)
    _measures(prs)
    _program(prs)
    _experiments(prs)
    _results(prs)
    _officers(prs)
    _computers(prs)
    _graphs(prs)
    _recommendation(prs)
    _close(prs)
    prs.save(OUTPUT)
    return OUTPUT


def _title(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, 0, 0, SLIDE_W, SLIDE_H, DEEP)
    rect(slide, 0, 0, Inches(0.18), SLIDE_H, GOLD)
    if LOGO.exists():
        slide.shapes.add_picture(str(LOGO), Inches(0.7), Inches(0.45), Inches(1.15), Inches(1.15))
    add_text(slide, Inches(2.05), Inches(0.62), Inches(10), Inches(0.3), "PALM UNIVERSITY COLLEGE  ·  MANYA JORPANYA", 14, GOLD, True)
    add_text(slide, Inches(0.7), Inches(2.05), Inches(11.5), Inches(1.5), "Course registration,\nsimulated one morning at a time", 40, WHITE, True)
    add_text(slide, Inches(0.7), Inches(4.35), Inches(10.5), Inches(0.9), "A deterministic simulation of the Registry desk: fixed arrivals, fixed processing times, and a choice of how many officers and computers to staff.", 18, MINT)
    add_text(slide, Inches(0.7), Inches(6.35), Inches(7), Inches(0.35), "Computer Simulation  ·  Project 2", 16, WHITE, True)
    add_text(slide, Inches(0.7), Inches(6.75), Inches(7), Inches(0.3), "Desmond", 16, GOLD)
    notes(slide, "Introduce yourself and the college. Say the project asks how a registration desk with limited officers and computers can finish a known group of students inside a fixed morning. Tell the class the method is deterministic simulation: nothing is random.")


def _problem(prs):
    slide = content_slide(prs, 2, "The brief", "What management wants to know")
    add_lines(slide, Inches(0.55), Inches(1.4), Inches(7.4), Inches(5.2), [
        "• The Registry has a limited number of officers and computers.",
        "• Every registration step takes a known number of minutes.",
        "• Students are expected during a fixed working period, 08:00 to 12:00.",
        "• Management needs the total time, the idle time, and the allocation that finishes the morning most efficiently.",
    ], 20, INK, 14)
    round_rect(slide, Inches(8.3), Inches(1.55), Inches(4.5), Inches(4.7), DEEP)
    add_text(slide, Inches(8.55), Inches(1.85), Inches(4.05), Inches(0.4), "Given, not guessed", 16, GOLD, True)
    add_lines(slide, Inches(8.55), Inches(2.45), Inches(4.0), Inches(3.3), [
        "• How many students arrive",
        "• The gap between arrivals",
        "• Minutes for each step",
        "• Officers on duty",
        "• Portal computers",
        "• When the desk closes",
    ], 16, WHITE, 8)
    notes(slide, "Read the problem in plain words. Stress that this is not a guess about a random queue. For the first model, arrivals, times, and resources are fixed before the doors open.")


def _approach(prs):
    slide = content_slide(prs, 3, "The method", "Deterministic simulation")
    cards = [
        ("Same inputs", "Run the morning twice with the same numbers and the schedule is identical."),
        ("One student at a time", "Each student walks the steps in order. A step uses one officer or one computer until it ends."),
        ("Then compare", "Keep the students fixed. Change only the officers, then only the computers, and read the new finish time."),
    ]
    for index, (heading, body) in enumerate(cards):
        top = Inches(1.45 + index * 1.75)
        round_rect(slide, Inches(0.55), top, Inches(12.2), Inches(1.55), CARD)
        rect(slide, Inches(0.55), top, Inches(0.12), Inches(1.55), GREEN)
        add_text(slide, Inches(1.0), top + Inches(0.22), Inches(11.3), Inches(0.4), heading, 22, GREEN, True)
        add_text(slide, Inches(1.0), top + Inches(0.7), Inches(11.3), Inches(0.65), body, 18, INK)
    notes(slide, "Define deterministic for the class: there is no probability distribution. If a classmate runs your program with the same inputs, they get your exact times. That is what makes the comparison fair.")


def _setting(prs):
    slide = content_slide(prs, 4, "The college", "One morning at the Registry")
    facts = [
        ("20", "students booked\nfor the morning"),
        ("8 min", "between arrivals,\nfirst student at 08:00"),
        ("12:00", "the desk is meant\nto close"),
        ("240 min", "the length of\nthe working period"),
    ]
    for index, (value, label) in enumerate(facts):
        left = Inches(0.5 + index * 3.2)
        round_rect(slide, left, Inches(1.5), Inches(3.0), Inches(2.35), CARD)
        add_text(slide, left + Inches(0.2), Inches(1.7), Inches(2.6), Inches(0.7), value, 32, GREEN, True, PP_ALIGN.CENTER)
        add_text(slide, left + Inches(0.2), Inches(2.5), Inches(2.6), Inches(1.0), label, 16, MUTED, align=PP_ALIGN.CENTER)
    add_text(slide, Inches(0.55), Inches(4.2), Inches(12.2), Inches(2.4), "Palm has a little over 100 undergraduates, and course registration is a short week, not a single rush hour for the whole college. This model is one morning of that week. The officer checks the student ID and the programme: Computer Science, Business Information Technology, or Business Administration. Course registration itself is done on the Student Portal.", 18, INK)
    notes(slide, "Tie the numbers to the real college. You are not inventing a huge university hall. Twenty students is a plausible share of one registration morning. Mention the Student Portal, because that is the computer step.")


def _activities(prs):
    slide = content_slide(prs, 5, "Resources and times", "Three steps, two scarce resources")
    steps = [
        ("1", "Registry check", "Officer", "6 min", "Confirm the ID and the programme."),
        ("2", "Student Portal", "Computer", "12 min", "Register the semester courses."),
        ("3", "Timetable", "Officer", "4 min", "Confirm the list and issue the timetable."),
    ]
    for index, (number, name, resource, minutes, detail) in enumerate(steps):
        left = Inches(0.45 + index * 4.25)
        round_rect(slide, left, Inches(1.45), Inches(4.0), Inches(3.15), CARD)
        add_text(slide, left + Inches(0.25), Inches(1.65), Inches(3.5), Inches(0.35), f"STEP  {number}", 13, GREEN, True)
        add_text(slide, left + Inches(0.25), Inches(2.05), Inches(3.5), Inches(0.7), name, 26, INK, True)
        add_text(slide, left + Inches(0.25), Inches(2.85), Inches(3.5), Inches(0.4), f"{resource}   ·   {minutes}", 18, GREEN, True)
        add_text(slide, left + Inches(0.25), Inches(3.4), Inches(3.5), Inches(0.8), detail, 16, MUTED)
    add_text(slide, Inches(0.55), Inches(4.9), Inches(12.2), Inches(1.9), "Each student needs 10 minutes with an officer and 12 minutes on a computer, 22 minutes of work in all. The officer pool covers both the check and the timetable. The computer pool is only the Student Portal. Forms, chairs, and the network are treated as available whenever an officer or a computer is free.", 18, INK)
    notes(slide, "This slide answers the part of the brief that asks you to name the resources and the processing time of each activity. Point at the 12 minutes: the computer step is the longest single task.")


def _rules(prs):
    slide = content_slide(prs, 6, "The model", "How a student moves through the desk")
    rules = [
        ("Arrive", "Student i arrives at i × 8 minutes. Student 1 is at the door at 08:00."),
        ("Seize", "The step takes the lowest-numbered free officer or computer and keeps it until the minutes are done."),
        ("Wait", "If that resource is busy, the student who has waited longest is called next."),
        ("Move on", "Finishing a step joins the next queue at once, so the officer can call someone else while a student is still on the computer."),
    ]
    for index, (heading, body) in enumerate(rules):
        column = index % 2
        row = index // 2
        left = Inches(0.5 + column * 6.4)
        top = Inches(1.45 + row * 2.55)
        round_rect(slide, left, top, Inches(6.1), Inches(2.35), CARD)
        add_text(slide, left + Inches(0.3), top + Inches(0.25), Inches(5.5), Inches(0.45), heading, 22, GREEN, True)
        add_text(slide, left + Inches(0.3), top + Inches(0.85), Inches(5.5), Inches(1.2), body, 16, INK)
    notes(slide, "Walk through one student, then a second student who arrives while the first is on the computer. The important idea is that the officer is shared and becomes free as soon as a step ends. Work is not interrupted.")


def _measures(prs):
    slide = content_slide(prs, 7, "The measures", "What each run reports")
    items = [
        ("Total time", "Minutes from 08:00 until the last student leaves."),
        ("Students processed", "Students who finish all three steps. In this model, that is the whole group."),
        ("Finished by close", "Students who have a timetable at or before 12:00."),
        ("Idle time", "Minutes an officer or a computer is free while the desk is still open."),
        ("Utilisation", "Busy minutes divided by units × total time. Adding a spare person or machine lowers this."),
        ("System efficiency", "Time being served, divided by time being served plus time waiting."),
    ]
    for index, (heading, body) in enumerate(items):
        column = index % 3
        row = index // 3
        left = Inches(0.45 + column * 4.25)
        top = Inches(1.45 + row * 2.7)
        round_rect(slide, left, top, Inches(4.05), Inches(2.45), CARD)
        add_text(slide, left + Inches(0.25), top + Inches(0.25), Inches(3.55), Inches(0.7), heading, 20, GREEN, True)
        add_text(slide, left + Inches(0.25), top + Inches(1.05), Inches(3.55), Inches(1.15), body, 15, INK)
    notes(slide, "Define system efficiency in one sentence: of the time a student spends at the desk, what share is actual service rather than waiting. A low percentage means the queue, not the work, is using up the morning.")


def _program(prs):
    slide = content_slide(prs, 8, "The program", "Python runs the morning")
    round_rect(slide, Inches(0.5), Inches(1.45), Inches(6.3), Inches(5.3), DEEP)
    add_text(slide, Inches(0.8), Inches(1.7), Inches(5.7), Inches(0.4), "Run it", 14, GOLD, True)
    commands = "python3 -m venv .venv\nsource .venv/bin/activate\npip install -r requirements.txt\npython registration.py"
    add_text(slide, Inches(0.8), Inches(2.25), Inches(5.7), Inches(2.2), commands, 18, WHITE)
    add_text(slide, Inches(0.8), Inches(4.7), Inches(5.7), Inches(1.6), "Change the group with --students, and the desk with --officers and --computers. The same inputs always print the same times.", 16, MINT)
    add_lines(slide, Inches(7.15), Inches(1.55), Inches(5.6), Inches(5.0), [
        "• Python is the simulation.",
        "• Matplotlib draws the three graphs.",
        "• The program writes index.html and the comparison table.",
        "• A hand-worked case is checked with pytest, so the clock times are not only a printout.",
        "• A short Next.js file serves that same page on the live site. It does not recalculate the queue.",
    ], 16, INK, 10)
    notes(slide, "If the lecturer asks to see the program, this is the command. Be clear that Python does the simulation. The website only displays the page the program already produced.")


def _experiments(prs):
    slide = content_slide(prs, 9, "The experiments", "Three ways to staff the same morning")
    add_text(slide, Inches(0.55), Inches(1.35), Inches(12.2), Inches(0.7), "The 20 students, the 8-minute arrivals, and the 12:00 close stay fixed. Only the desk changes.", 18, INK)
    experiments = [
        ("1", "Current desk", "1 officer\n1 computer", "The Registry as it stands this morning."),
        ("2", "Second officer", "2 officers\n1 computer", "One more officer. The portal computer stays as it is."),
        ("3", "Second computer", "1 officer\n2 computers", "One more Student Portal computer. The officer stays as they are."),
    ]
    for index, (number, name, counts, detail) in enumerate(experiments):
        left = Inches(0.45 + index * 4.25)
        round_rect(slide, left, Inches(2.25), Inches(4.05), Inches(4.4), CARD)
        add_text(slide, left + Inches(0.25), Inches(2.45), Inches(3.5), Inches(0.35), f"EXPERIMENT  {number}", 13, GREEN, True)
        add_text(slide, left + Inches(0.25), Inches(2.9), Inches(3.5), Inches(0.7), name, 26, INK, True)
        add_text(slide, left + Inches(0.25), Inches(3.7), Inches(3.5), Inches(1.1), counts, 20, GREEN, True)
        add_text(slide, left + Inches(0.25), Inches(5.05), Inches(3.5), Inches(1.2), detail, 16, MUTED)
    notes(slide, "Say why there are three, not one. The brief asks for the effect of more officers and the effect of more computers separately. Experiment 2 changes only officers. Experiment 3 changes only computers.")


def _results(prs):
    slide = content_slide(prs, 10, "The comparison", "Total time under each allocation")
    headers = ["Allocation", "Officers", "Computers", "Total time", "By 12:00", "Officer use", "Computer use", "Efficiency"]
    rows = [
        ["Current desk", "1", "1", "12:10  ·  250 min", "19 / 20", "80.0%", "96.0%", "33.6%"],
        ["Second officer", "2", "1", "12:10  ·  250 min", "19 / 20", "40.0%", "96.0%", "36.7%"],
        ["Second computer", "1", "2", "11:24  ·  204 min", "20 / 20", "98.0%", "58.8%", "45.3%"],
    ]
    table_shape = slide.shapes.add_table(4, 8, Inches(0.35), Inches(1.5), Inches(12.6), Inches(2.6))
    table = table_shape.table
    widths = [1.85, 1.15, 1.3, 2.15, 1.25, 1.55, 1.7, 1.65]
    for index, width in enumerate(widths):
        table.columns[index].width = Inches(width)
    for column, header in enumerate(headers):
        style_cell(table.cell(0, column), header, 12, WHITE, DEEP, True, PP_ALIGN.CENTER)
    for row_index, row in enumerate(rows):
        fill = MINT if row_index == 2 else CARD
        for column, value in enumerate(row):
            align = PP_ALIGN.LEFT if column == 0 else PP_ALIGN.CENTER
            style_cell(table.cell(row_index + 1, column), value, 13, INK, fill, row_index == 2, align)
    add_lines(slide, Inches(0.5), Inches(4.45), Inches(12.3), Inches(2.5), [
        "• All 20 students are processed in every experiment. The desk stays open until the last timetable is issued.",
        "• On the current desk the last student leaves at 12:10, ten minutes after the close. One student is still there at noon.",
        "• The highlighted row is the only allocation that finishes the whole group before 12:00.",
    ], 16, INK, 8)
    notes(slide, "Read the total-time column first: 250, 250, then 204. Then read the By 12:00 column: 19, 19, then 20. Those two columns are the result the brief asks for. The green row is the one you will recommend.")


def _officers(prs):
    slide = content_slide(prs, 11, "More officers", "A second officer does not shorten the morning")
    stats = [
        ("12:10", "Finish time, unchanged"),
        ("19 / 20", "Still finished by noon"),
        ("80% → 40%", "Officer utilisation"),
        ("60 → 310", "Idle resource-minutes"),
    ]
    for index, (value, label) in enumerate(stats):
        left = Inches(0.45 + index * 3.2)
        round_rect(slide, left, Inches(1.5), Inches(3.05), Inches(2.15), CARD)
        add_text(slide, left + Inches(0.12), Inches(1.68), Inches(2.8), Inches(0.75), value, 26, GREEN, True, PP_ALIGN.CENTER)
        add_text(slide, left + Inches(0.15), Inches(2.55), Inches(2.75), Inches(0.8), label, 15, MUTED, align=PP_ALIGN.CENTER)
    add_text(slide, Inches(0.55), Inches(4.05), Inches(12.2), Inches(2.6), "The portal computer is busy 96 percent of the morning either way. The officer is often waiting for a student to finish on that computer. A second officer splits the same 200 minutes of officer work across two people, so each is busy only 40 percent of the time. Average waiting falls only from 43.4 minutes to 38.0 minutes. The extra officer is present, and mostly idle.", 20, INK)
    notes(slide, "This is the officer half of the resource question. Do not say officers never matter. Say that on this morning the computer is the limit, so another officer cannot move the finish time. The evidence is the unchanged 250 minutes and the idle time jumping to 310.")


def _computers(prs):
    slide = content_slide(prs, 12, "More computers", "A second computer clears the morning")
    stats = [
        ("46 min", "Earlier finish, 12:10 to 11:24"),
        ("20 / 20", "Finished before the close"),
        ("43.4 → 26.6", "Average wait, in minutes"),
        ("45.3%", "System efficiency, up from 33.6%"),
    ]
    for index, (value, label) in enumerate(stats):
        left = Inches(0.45 + index * 3.2)
        round_rect(slide, left, Inches(1.5), Inches(3.05), Inches(2.15), CARD)
        add_text(slide, left + Inches(0.1), Inches(1.68), Inches(2.85), Inches(0.75), value, 24, GREEN, True, PP_ALIGN.CENTER)
        add_text(slide, left + Inches(0.15), Inches(2.55), Inches(2.75), Inches(0.85), label, 15, MUTED, align=PP_ALIGN.CENTER)
    add_text(slide, Inches(0.55), Inches(4.05), Inches(12.2), Inches(2.6), "The longest step is the 12 minutes on the Student Portal, and on the current desk the longest wait is for that computer, up to 62 minutes. A second computer lets the next student start registering while the first is still being served. The single officer then becomes the busy resource, at 98 percent. The two computers share the work, so each computer's utilisation falls to 58.8 percent. The morning still ends inside the session.", 20, INK)
    notes(slide, "This is the computer half of the question. Quote the 46 minutes and the move from 19 finished to 20 finished. Mention the 62-minute maximum wait so the class can see where students were actually standing.")


def _graphs(prs):
    slide = content_slide(prs, 13, "The graphs", "The same three results, drawn")
    images = [
        (FIGURES / "makespan_by_scenario.png", "Total time. The line is 12:00."),
        (FIGURES / "utilisation_by_scenario.png", "Who is busy under each desk."),
        (FIGURES / "students_within_period.png", "Who finishes before the close."),
    ]
    for index, (path, caption) in enumerate(images):
        left = Inches(0.4 + index * 4.3)
        round_rect(slide, left, Inches(1.45), Inches(4.15), Inches(4.15), CARD)
        slide.shapes.add_picture(str(path), left + Inches(0.15), Inches(1.6), Inches(3.85))
        add_text(slide, left + Inches(0.25), Inches(4.55), Inches(3.7), Inches(0.8), caption, 16, INK)
    notes(slide, "Do not read every bar. On the first chart, show that the officer bar stays at the same height and the computer bar drops below the 12:00 line. On the second, show the computer bar staying tall until the third experiment. On the third, show the third bar reaching the full group of 20.")


def _recommendation(prs):
    slide = content_slide(prs, 14, "The decision", "Staff one officer and two computers")
    round_rect(slide, Inches(0.5), Inches(1.45), Inches(12.3), Inches(1.7), DEEP)
    add_text(slide, Inches(0.8), Inches(1.65), Inches(11.7), Inches(0.35), "MOST EFFICIENT ALLOCATION", 13, GOLD, True)
    add_text(slide, Inches(0.8), Inches(2.05), Inches(11.7), Inches(0.8), "1 registry officer   ·   2 Student Portal computers", 28, WHITE, True)
    points = [
        ("Finishes the group", "20 of 20 students have a timetable before noon. The other two desks leave one student after 12:00."),
        ("Uses the scarce resource", "The computer was the limit. Adding the officer left the finish time at 250 minutes."),
        ("Why not the busiest desk?", "The current desk has higher overall utilisation, 88 percent against 72 percent, but it misses the close. Finishing the students comes first."),
    ]
    for index, (heading, body) in enumerate(points):
        left = Inches(0.5 + index * 4.2)
        add_text(slide, left, Inches(3.45), Inches(4.0), Inches(0.7), heading, 18, GREEN, True)
        add_text(slide, left, Inches(4.15), Inches(4.0), Inches(2.5), body, 15, INK)
    notes(slide, "State the recommendation in one sentence, then the reason. If someone asks why the current desk is not more efficient because it is busier, answer that a busy computer which still misses noon is not the efficient allocation. The rule finishes the students first, then prefers the desk that stays useful.")


def _close(prs):
    slide = content_slide(prs, 15, "To take away", "What the morning shows")
    add_lines(slide, Inches(0.55), Inches(1.4), Inches(7.6), Inches(5.2), [
        "• The model is deterministic: 20 students, every 8 minutes, three fixed steps.",
        "• One officer and one computer finish at 12:10. One student misses the close.",
        "• A second officer does not move that time.",
        "• A second computer finishes everyone at 11:24.",
        "• That desk is the efficient allocation for this morning.",
    ], 20, INK, 12)
    round_rect(slide, Inches(8.4), Inches(1.5), Inches(4.4), Inches(5.1), DEEP)
    add_text(slide, Inches(8.65), Inches(1.75), Inches(4.0), Inches(0.4), "See the run", 16, GOLD, True)
    add_text(slide, Inches(8.65), Inches(2.3), Inches(4.0), Inches(1.5), "python registration.py", 18, WHITE, True)
    add_text(slide, Inches(8.65), Inches(4.0), Inches(4.0), Inches(1.8), "The same results are on the live page and in the GitHub repository.", 16, MINT)
    notes(slide, "Close on the five lines, then invite questions. You can offer to open the live page or to run the program with a different number of students if someone wants to see the model move.")


if __name__ == "__main__":
    path = build()
    print(path)
