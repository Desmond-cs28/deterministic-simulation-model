import { EMPTY_COUNT } from "@/lib/constants"
import { format_clock, format_count, format_one_decimal, format_percent } from "@/lib/format"
import type { SimulationMetrics } from "@/lib/types"

export function KpiGrid({ metrics }: { metrics: SimulationMetrics }) {
  const finish_clock = format_clock(metrics.makespan_minutes)
  const overtime_note =
    metrics.overtime_minutes === EMPTY_COUNT
      ? "Inside the session"
      : `${metrics.overtime_minutes} min overtime`

  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      <Kpi label="Makespan" value={finish_clock} note={`${metrics.makespan_minutes} min · ${overtime_note}`} />
      <Kpi
        label="Finished in session"
        value={format_count(metrics.students_finished_within_period, metrics.students_processed)}
        note={`${metrics.students_unfinished_within_period} still in the hall at close`}
      />
      <Kpi label="Officer utilisation" value={format_percent(metrics.officer_utilisation)} note={`${metrics.officer_idle_minutes} idle min`} />
      <Kpi label="Computer utilisation" value={format_percent(metrics.computer_utilisation)} note={`${metrics.computer_idle_minutes} idle min`} />
      <Kpi label="Idle resource-minutes" value={String(metrics.overall_idle_minutes)} note={`${format_percent(metrics.overall_utilisation)} overall utilisation`} />
      <Kpi label="Average wait" value={`${format_one_decimal(metrics.average_waiting_minutes)} min`} note={`Peak in hall: ${metrics.peak_students_in_system}`} />
      <Kpi label="Service efficiency" value={format_percent(metrics.service_efficiency)} note="Processing ÷ (processing + waiting)" />
      <Kpi label="Schedule efficiency" value={format_percent(metrics.schedule_efficiency)} note={`Lower bound ${metrics.lower_bound_minutes} min`} />
    </div>
  )
}

function Kpi({ label, value, note }: { label: string; value: string; note: string }) {
  return (
    <div className="rounded-xl bg-card px-3 py-3 ring-1 ring-foreground/10 sm:px-4">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="font-heading mt-1 text-2xl tracking-tight tabular-nums">{value}</p>
      <p className="mt-1 text-xs leading-relaxed text-muted-foreground">{note}</p>
    </div>
  )
}
