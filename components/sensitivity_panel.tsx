"use client"

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"

import { Button } from "@/components/ui/button"
import {
  FIRST_INDEX,
  GRID,
  INDEX_STEP,
  INK,
  LINE_COLORS,
  MUTED,
  PAPER,
  RUST,
  SENSITIVITY_MAX_UNITS,
  SENSITIVITY_MIN_UNITS,
} from "@/lib/constants"
import type { SensitivityCell } from "@/lib/types"

import { SectionBlock } from "./section_block"

const LOW_RED = 215
const LOW_GREEN = 239
const LOW_BLUE = 233
const HIGH_RED = 224
const HIGH_GREEN = 122
const HIGH_BLUE = 92

export function SensitivityPanel({
  cells,
  session_minutes,
  applied_officers,
  applied_computers,
  best_officers,
  best_computers,
  on_select,
}: {
  cells: SensitivityCell[]
  session_minutes: number
  applied_officers: number
  applied_computers: number
  best_officers: number
  best_computers: number
  on_select: (officer_count: number, computer_count: number) => void
}) {
  const makespans = cells.map((cell) => cell.makespan_minutes)
  const low = Math.min(...makespans)
  const high = Math.max(...makespans)
  const chart_rows = chart_rows_from(cells)
  const computer_counts = counts_between(SENSITIVITY_MIN_UNITS, SENSITIVITY_MAX_UNITS)
  const officer_counts = computer_counts

  return (
    <SectionBlock
      id="sensitivity"
      kicker="Sensitivity"
      title="What changes when you add one more desk"
      lede="Each cell is a full run of the same cohort. Reading across a row adds officers. Reading down a column adds computers. A flat stretch means the extra unit is idle capacity: the other pool is still the bottleneck."
    >
      <div className="overflow-x-auto rounded-xl bg-card p-4 ring-1 ring-foreground/10">
        <div className="min-w-[36rem]">
          <div
            className="grid gap-1 text-center text-xs"
            style={{ gridTemplateColumns: `6.5rem repeat(${officer_counts.length}, minmax(4.5rem, 1fr))` }}
          >
            <div />
            {officer_counts.map((officer_count) => (
              <div key={officer_count} className="py-1 font-medium">
                {officer_count} {officer_count === SENSITIVITY_MIN_UNITS ? "officer" : "officers"}
              </div>
            ))}
            {computer_counts.map((computer_count) => (
              <div key={computer_count} className="contents">
                <div className="flex items-center justify-end pr-2 text-left font-medium">
                  {computer_count} {computer_count === SENSITIVITY_MIN_UNITS ? "computer" : "computers"}
                </div>
                {officer_counts.map((officer_count) => {
                  const cell = cells.find(
                    (item) => item.officer_count === officer_count && item.computer_count === computer_count,
                  )
                  if (!cell) {
                    return <div key={`${officer_count}-${computer_count}`} />
                  }
                  const best = officer_count === best_officers && computer_count === best_computers
                  const applied = officer_count === applied_officers && computer_count === applied_computers
                  return (
                    <Button
                      key={`${officer_count}-${computer_count}`}
                      type="button"
                      variant="outline"
                      className="h-auto cursor-pointer flex-col gap-0 rounded-md px-1 py-2"
                      style={{
                        backgroundColor: heat_color(cell.makespan_minutes, low, high),
                        outline: best || applied ? "2px solid #1c1915" : undefined,
                      }}
                      onClick={() => on_select(officer_count, computer_count)}
                    >
                      <span className="font-mono text-sm tabular-nums text-foreground">{cell.makespan_minutes}</span>
                      <span className="text-[0.65rem] text-foreground/70">
                        {cell.students_finished_within_period}/{cell.student_count}
                        {best ? " · best" : ""}
                      </span>
                    </Button>
                  )
                })}
              </div>
            ))}
          </div>
          <p className="mt-3 text-xs text-muted-foreground">
            Cell numbers are the makespan in minutes, then how many students finish inside the session. Pale cells finish sooner. The outlined cell marked “best” wins the efficiency score. Click a cell to open that staffing in the timeline.
          </p>
        </div>
      </div>
      <div className="mt-4 rounded-xl bg-card p-4 ring-1 ring-foreground/10">
        <h3 className="font-heading text-xl">Makespan as each pool grows</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          One line per computer pool. The dashed line is the session close ({session_minutes} min).
        </p>
        <div className="mt-3 h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chart_rows} margin={{ top: 8, right: 8, left: 0, bottom: 8 }}>
              <CartesianGrid stroke={GRID} />
              <XAxis dataKey="officer_count" tick={{ fill: MUTED, fontSize: 11 }} label={{ value: "Officers", position: "insideBottom", offset: -2, fill: MUTED, fontSize: 12 }} />
              <YAxis tick={{ fill: MUTED, fontSize: 11 }} width={48} />
              <Tooltip contentStyle={{ background: PAPER, border: `1px solid ${GRID}`, borderRadius: 8, fontSize: 12, color: INK }} />
              <Legend />
              <ReferenceLine y={session_minutes} stroke={RUST} strokeDasharray="4 4" />
              {computer_counts.map((computer_count, index) => (
                <Line
                  key={computer_count}
                  type="monotone"
                  dataKey={`computers_${computer_count}`}
                  name={
                    computer_count === SENSITIVITY_MIN_UNITS
                      ? `${computer_count} computer`
                      : `${computer_count} computers`
                  }
                  stroke={LINE_COLORS[index % LINE_COLORS.length]}
                  strokeWidth={2}
                  dot={{ r: 3 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </SectionBlock>
  )
}

function counts_between(low: number, high: number): number[] {
  const values: number[] = []
  let cursor = low
  while (cursor <= high) {
    values.push(cursor)
    cursor += INDEX_STEP
  }
  return values
}

function chart_rows_from(cells: SensitivityCell[]): Array<Record<string, number>> {
  const grouped = new Map<number, Record<string, number>>()
  for (const cell of cells) {
    const row = grouped.get(cell.officer_count) ?? { officer_count: cell.officer_count }
    row[`computers_${cell.computer_count}`] = cell.makespan_minutes
    grouped.set(cell.officer_count, row)
  }
  return [...grouped.values()].sort((left, right) => left.officer_count - right.officer_count)
}

function heat_color(makespan: number, low: number, high: number): string {
  const blend = high === low ? FIRST_INDEX : (makespan - low) / (high - low)
  const red = Math.round(LOW_RED + (HIGH_RED - LOW_RED) * blend)
  const green = Math.round(LOW_GREEN + (HIGH_GREEN - LOW_GREEN) * blend)
  const blue = Math.round(LOW_BLUE + (HIGH_BLUE - LOW_BLUE) * blend)
  return `rgb(${red}, ${green}, ${blue})`
}
