"use client"

import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"

import { AMBER, GRID, INK, MUTED, NAVY, PAPER, PERCENT_SCALE, RUST, TEAL } from "@/lib/constants"
import type { ScenarioRun } from "@/lib/types"

const tooltip_style = {
  background: PAPER,
  border: `1px solid ${GRID}`,
  borderRadius: 8,
  fontSize: 12,
  color: INK,
}

export function ExperimentCharts({ runs, session_minutes }: { runs: ScenarioRun[]; session_minutes: number }) {
  const rows = runs.map((run) => ({
    label: run.scenario.short_label,
    makespan_minutes: run.metrics.makespan_minutes,
    officer_utilisation: Math.round(run.metrics.officer_utilisation * PERCENT_SCALE),
    computer_utilisation: Math.round(run.metrics.computer_utilisation * PERCENT_SCALE),
    finished: run.metrics.students_finished_within_period,
  }))
  const cohort = runs[0]?.metrics.students_processed ?? 0

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <ChartCard title="Makespan against the session close" note="The dashed line is the end of the working period.">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={rows} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
            <CartesianGrid vertical={false} stroke={GRID} />
            <XAxis dataKey="label" tick={{ fill: MUTED, fontSize: 11 }} interval={0} height={48} />
            <YAxis tick={{ fill: MUTED, fontSize: 11 }} unit="m" width={48} />
            <Tooltip contentStyle={tooltip_style} />
            <ReferenceLine y={session_minutes} stroke={RUST} strokeDasharray="4 4" />
            <Bar dataKey="makespan_minutes" name="Makespan (min)" fill={TEAL} radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>
      <ChartCard title="Utilisation of each pool" note="A tall computer bar beside a short officer bar means the terminals are the scarce resource.">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={rows} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
            <CartesianGrid vertical={false} stroke={GRID} />
            <XAxis dataKey="label" tick={{ fill: MUTED, fontSize: 11 }} interval={0} height={48} />
            <YAxis tick={{ fill: MUTED, fontSize: 11 }} unit="%" width={48} domain={[0, 100]} />
            <Tooltip contentStyle={tooltip_style} />
            <Legend />
            <Bar dataKey="officer_utilisation" name="Officers" fill={NAVY} radius={[4, 4, 0, 0]} />
            <Bar dataKey="computer_utilisation" name="Computers" fill={TEAL} radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>
      <ChartCard title="Students finished before close" note="The dashed line is the full cohort.">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={rows} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
            <CartesianGrid vertical={false} stroke={GRID} />
            <XAxis dataKey="label" tick={{ fill: MUTED, fontSize: 11 }} interval={0} height={48} />
            <YAxis tick={{ fill: MUTED, fontSize: 11 }} width={36} allowDecimals={false} />
            <Tooltip contentStyle={tooltip_style} />
            <ReferenceLine y={cohort} stroke={NAVY} strokeDasharray="4 4" />
            <Bar dataKey="finished" name="Finished in session" fill={AMBER} radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>
    </div>
  )
}

function ChartCard({ title, note, children }: { title: string; note: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl bg-card p-4 ring-1 ring-foreground/10">
      <h3 className="font-heading text-xl">{title}</h3>
      <p className="mt-1 text-sm text-muted-foreground">{note}</p>
      <div className="mt-3 h-72">{children}</div>
    </div>
  )
}
