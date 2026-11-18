"use client"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { format_one_decimal, format_percent, format_score } from "@/lib/format"
import type { ScenarioRun } from "@/lib/types"

import { ExperimentCharts } from "./experiment_charts"
import { SectionBlock } from "./section_block"

export function ExperimentPanel({
  runs,
  recommended_id,
  session_minutes,
  on_open,
}: {
  runs: ScenarioRun[]
  recommended_id: string
  session_minutes: number
  on_open: (run: ScenarioRun) => void
}) {
  return (
    <SectionBlock
      id="experiments"
      kicker="Experiments"
      title="Three ways to staff the same morning"
      lede="The students, the arrival interval, and the session stay fixed. The first row is the desk as it stands. The next adds an officer. The last adds a portal computer. Open a row to see that morning on the timeline."
    >
      <div className="overflow-x-auto rounded-xl bg-card ring-1 ring-foreground/10">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Scenario</TableHead>
              <TableHead>Officers</TableHead>
              <TableHead>Computers</TableHead>
              <TableHead>Makespan</TableHead>
              <TableHead>In session</TableHead>
              <TableHead>Overtime</TableHead>
              <TableHead>Officer util.</TableHead>
              <TableHead>Computer util.</TableHead>
              <TableHead>Idle min.</TableHead>
              <TableHead>Avg wait</TableHead>
              <TableHead>System eff.</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {runs.map((run) => {
              const recommended = run.scenario.scenario_id === recommended_id
              return (
                <TableRow key={run.scenario.scenario_id} className={recommended ? "bg-accent/60" : undefined}>
                  <TableCell>
                    <Button
                      type="button"
                      variant="link"
                      className="h-auto cursor-pointer px-0 text-left"
                      onClick={() => on_open(run)}
                    >
                      {run.scenario.name}
                    </Button>
                    {recommended ? (
                      <Badge className="ml-2" variant="default">
                        Most efficient
                      </Badge>
                    ) : null}
                    <p className="text-xs text-muted-foreground">{run.scenario.summary}</p>
                  </TableCell>
                  <TableCell className="tabular-nums">{run.scenario.officer_count}</TableCell>
                  <TableCell className="tabular-nums">{run.scenario.computer_count}</TableCell>
                  <TableCell className="tabular-nums">{run.metrics.makespan_minutes}</TableCell>
                  <TableCell className="tabular-nums">
                    {run.metrics.students_finished_within_period}/{run.metrics.students_processed}
                  </TableCell>
                  <TableCell className="tabular-nums">{run.metrics.overtime_minutes}</TableCell>
                  <TableCell className="tabular-nums">{format_percent(run.metrics.officer_utilisation)}</TableCell>
                  <TableCell className="tabular-nums">{format_percent(run.metrics.computer_utilisation)}</TableCell>
                  <TableCell className="tabular-nums">{run.metrics.overall_idle_minutes}</TableCell>
                  <TableCell className="tabular-nums">{format_one_decimal(run.metrics.average_waiting_minutes)}</TableCell>
                  <TableCell className="tabular-nums">{format_percent(run.metrics.service_efficiency)}</TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </div>
      <div className="mt-3">
        <Button type="button" variant="outline" className="cursor-pointer" onClick={() => download_csv(runs)}>
          Download comparison (.csv)
        </Button>
      </div>
      <div className="mt-4">
        <ExperimentCharts runs={runs} session_minutes={session_minutes} />
      </div>
    </SectionBlock>
  )
}

function download_csv(runs: ScenarioRun[]): void {
  const headers = [
    "Scenario",
    "Officers",
    "Computers",
    "Makespan",
    "In session",
    "Processed",
    "Overtime",
    "Officer util.",
    "Computer util.",
    "Overall util.",
    "Idle min.",
    "Avg wait",
    "Service eff.",
    "Schedule eff.",
    "Score",
  ]
  const lines = [headers.join(",")]
  for (const run of runs) {
    const cells = [
      run.scenario.name,
      String(run.scenario.officer_count),
      String(run.scenario.computer_count),
      String(run.metrics.makespan_minutes),
      String(run.metrics.students_finished_within_period),
      String(run.metrics.students_processed),
      String(run.metrics.overtime_minutes),
      format_percent(run.metrics.officer_utilisation),
      format_percent(run.metrics.computer_utilisation),
      format_percent(run.metrics.overall_utilisation),
      String(run.metrics.overall_idle_minutes),
      format_one_decimal(run.metrics.average_waiting_minutes),
      format_percent(run.metrics.service_efficiency),
      format_percent(run.metrics.schedule_efficiency),
      format_score(run.metrics.efficiency_score),
    ]
    lines.push(cells.map(csv_cell).join(","))
  }
  const blob = new Blob([lines.join("\n")], { type: "text/csv" })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement("a")
  anchor.href = url
  anchor.download = "scenario_comparison.csv"
  anchor.click()
  URL.revokeObjectURL(url)
}

function csv_cell(value: string): string {
  if (value.includes(",") || value.includes("\"")) {
    return `"${value.replaceAll("\"", "\"\"")}"`
  }
  return value
}
