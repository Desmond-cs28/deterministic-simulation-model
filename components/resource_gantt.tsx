"use client"

import { ACTIVITY_SEQUENCE } from "@/lib/activities"
import {
  ActivityColor,
  DISPLAY_INDEX_OFFSET,
  EMPTY_COUNT,
  FIRST_INDEX,
  GANTT_AXIS_HEIGHT,
  GANTT_LABEL_WIDTH,
  GANTT_PADDING_RIGHT,
  GANTT_PIXELS_PER_MINUTE,
  GANTT_ROW_HEIGHT,
  INDEX_STEP,
  ResourceKind,
  RUST,
  ZERO_MINUTES,
} from "@/lib/constants"
import { format_clock, student_label } from "@/lib/format"
import type { ActivityId } from "@/lib/constants"
import type { SimulationResult } from "@/lib/types"

const TICK_FINE_MINUTES = 30
const TICK_COARSE_MINUTES = 60
const TICK_COARSE_AFTER = 180
const LANE_FILL = "#efe6d6"
const OVERTIME_FILL = "rgba(180, 73, 42, 0.12)"

export function ResourceGantt({ result }: { result: SimulationResult }) {
  const session = result.config.working_period_minutes
  const axis_end = Math.max(result.makespan_minutes, session)
  if (result.students.length === EMPTY_COUNT || axis_end === ZERO_MINUTES) {
    return null
  }

  const resources = resource_lanes(result)
  const chart_width = GANTT_LABEL_WIDTH + axis_end * GANTT_PIXELS_PER_MINUTE + GANTT_PADDING_RIGHT
  const chart_height = GANTT_AXIS_HEIGHT + resources.length * GANTT_ROW_HEIGHT + INDEX_STEP * 8
  const tick_step = axis_end > TICK_COARSE_AFTER ? TICK_COARSE_MINUTES : TICK_FINE_MINUTES
  const ticks: number[] = []
  let tick = ZERO_MINUTES
  while (tick <= axis_end) {
    ticks.push(tick)
    tick += tick_step
  }

  return (
    <div className="rounded-xl bg-card p-4 ring-1 ring-foreground/10">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h3 className="font-heading text-2xl">Resource timeline</h3>
          <p className="mt-1 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            Each bar is one student on one unit. A gap on a lane is idle time. The tint after the
            session line is overtime.
          </p>
        </div>
        <ul className="flex flex-wrap gap-3">
          {ACTIVITY_SEQUENCE.map((activity) => (
            <li key={activity.activity_id} className="flex items-center gap-1.5 text-xs">
              <span
                className="inline-block size-2.5 rounded-sm"
                style={{ backgroundColor: ActivityColor[activity.activity_id] }}
              />
              {activity.short_label}
            </li>
          ))}
        </ul>
      </div>
      <div className="mt-4 overflow-x-auto">
        <svg
          width={chart_width}
          height={chart_height}
          role="img"
          aria-label="Gantt chart of officers and computers across the session"
        >
          <line
            x1={GANTT_LABEL_WIDTH}
            x2={GANTT_LABEL_WIDTH + axis_end * GANTT_PIXELS_PER_MINUTE}
            y1={GANTT_AXIS_HEIGHT - 6}
            y2={GANTT_AXIS_HEIGHT - 6}
            stroke="#d9d0c1"
          />
          {ticks.map((minute) => {
            const x = GANTT_LABEL_WIDTH + minute * GANTT_PIXELS_PER_MINUTE
            return (
              <g key={minute}>
                <line x1={x} x2={x} y1={GANTT_AXIS_HEIGHT - 10} y2={chart_height - 4} stroke="#e4dccf" />
                <text x={x} y={14} textAnchor="middle" fontSize="11" fill="#5e574c" fontFamily="IBM Plex Mono, monospace">
                  {format_clock(minute)}
                </text>
              </g>
            )
          })}
          {session < axis_end ? (
            <rect
              x={GANTT_LABEL_WIDTH + session * GANTT_PIXELS_PER_MINUTE}
              y={GANTT_AXIS_HEIGHT}
              width={(axis_end - session) * GANTT_PIXELS_PER_MINUTE}
              height={resources.length * GANTT_ROW_HEIGHT}
              fill={OVERTIME_FILL}
            />
          ) : null}
          {resources.map((lane, row_index) => {
            const y = GANTT_AXIS_HEIGHT + row_index * GANTT_ROW_HEIGHT
            return (
              <g key={lane.key}>
                <text x={0} y={y + 20} fontSize="12" fill="#1c1915">
                  {lane.label}
                </text>
                <rect
                  x={GANTT_LABEL_WIDTH}
                  y={y + 6}
                  width={axis_end * GANTT_PIXELS_PER_MINUTE}
                  height={GANTT_ROW_HEIGHT - 12}
                  fill={LANE_FILL}
                  rx={4}
                />
                {lane.bars.map((bar) => (
                  <g key={bar.key}>
                    <title>{bar.title}</title>
                    <rect
                      x={GANTT_LABEL_WIDTH + bar.start_minutes * GANTT_PIXELS_PER_MINUTE}
                      y={y + 6}
                      width={Math.max(bar.processing_minutes * GANTT_PIXELS_PER_MINUTE, INDEX_STEP)}
                      height={GANTT_ROW_HEIGHT - 12}
                      fill={ActivityColor[bar.activity_id]}
                      rx={3}
                    />
                  </g>
                ))}
              </g>
            )
          })}
          <line
            x1={GANTT_LABEL_WIDTH + session * GANTT_PIXELS_PER_MINUTE}
            x2={GANTT_LABEL_WIDTH + session * GANTT_PIXELS_PER_MINUTE}
            y1={GANTT_AXIS_HEIGHT - 12}
            y2={chart_height - 4}
            stroke={RUST}
            strokeDasharray="4 3"
          />
        </svg>
      </div>
    </div>
  )
}

type Lane = {
  key: string
  label: string
  bars: Array<{
    key: string
    activity_id: ActivityId
    start_minutes: number
    processing_minutes: number
    title: string
  }>
}

function resource_lanes(result: SimulationResult): Lane[] {
  const lanes: Lane[] = []
  const specs = [
    { kind: ResourceKind.OFFICER, count: result.config.officer_count, title: "Officer" },
    { kind: ResourceKind.COMPUTER, count: result.config.computer_count, title: "Computer" },
  ]
  for (const spec of specs) {
    let unit_index = FIRST_INDEX
    while (unit_index < spec.count) {
      const bars = result.assignments
        .filter((assignment) => assignment.resource_kind === spec.kind && assignment.resource_index === unit_index)
        .map((assignment) => {
          const activity = ACTIVITY_SEQUENCE.find((item) => item.activity_id === assignment.activity_id)
          const label = activity ? activity.short_label : assignment.activity_id
          return {
            key: `${assignment.student_index}-${assignment.activity_id}`,
            activity_id: assignment.activity_id,
            start_minutes: assignment.start_minutes,
            processing_minutes: assignment.processing_minutes,
            title: `${student_label(assignment.student_index)} · ${label} · ${format_clock(assignment.start_minutes)}–${format_clock(assignment.end_minutes)}`,
          }
        })
      lanes.push({
        key: `${spec.kind}-${unit_index}`,
        label: `${spec.title} ${unit_index + DISPLAY_INDEX_OFFSET}`,
        bars,
      })
      unit_index += INDEX_STEP
    }
  }
  return lanes
}
