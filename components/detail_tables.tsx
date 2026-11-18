import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { NO_LABEL, YES_LABEL } from "@/lib/constants"
import { format_clock, format_one_decimal, format_percent, student_label } from "@/lib/format"
import type { SimulationMetrics, SimulationResult } from "@/lib/types"

export function DetailTables({ result, metrics }: { result: SimulationResult; metrics: SimulationMetrics }) {
  const session = result.config.working_period_minutes
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <div className="rounded-xl bg-card p-4 ring-1 ring-foreground/10">
        <h3 className="font-heading text-xl">Resource utilisation</h3>
        <Table className="mt-3">
          <TableHeader>
            <TableRow>
              <TableHead>Resource</TableHead>
              <TableHead>Busy</TableHead>
              <TableHead>Idle</TableHead>
              <TableHead>Utilisation</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {metrics.resources.map((row) => (
              <TableRow key={row.resource_label}>
                <TableCell>{row.resource_label}</TableCell>
                <TableCell className="tabular-nums">{row.busy_minutes} min</TableCell>
                <TableCell className="tabular-nums">{row.idle_minutes} min</TableCell>
                <TableCell className="tabular-nums">{format_percent(row.utilisation)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <div className="rounded-xl bg-card p-4 ring-1 ring-foreground/10">
        <h3 className="font-heading text-xl">Waiting by activity</h3>
        <Table className="mt-3">
          <TableHeader>
            <TableRow>
              <TableHead>Activity</TableHead>
              <TableHead>Avg wait</TableHead>
              <TableHead>Max wait</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {metrics.stages.map((stage) => (
              <TableRow key={stage.activity_id}>
                <TableCell>{stage.label}</TableCell>
                <TableCell className="tabular-nums">{format_one_decimal(stage.average_wait_minutes)} min</TableCell>
                <TableCell className="tabular-nums">{stage.max_wait_minutes} min</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <div className="rounded-xl bg-card p-4 ring-1 ring-foreground/10 lg:col-span-2">
        <h3 className="font-heading text-xl">Students</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          {metrics.students_processed} processed. A student counts as finished in the session when the card is issued at or before the close.
        </p>
        <div className="mt-3 max-h-96 overflow-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Student</TableHead>
                <TableHead>Arrives</TableHead>
                <TableHead>Starts</TableHead>
                <TableHead>Finishes</TableHead>
                <TableHead>Wait</TableHead>
                <TableHead>Flow</TableHead>
                <TableHead>In session</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {result.students.map((student) => {
                const started = student.stages[0]?.start_minutes ?? student.arrival_minutes
                const in_session = student.completion_minutes <= session
                return (
                  <TableRow key={student.student_index}>
                    <TableCell>{student_label(student.student_index)}</TableCell>
                    <TableCell className="tabular-nums">{format_clock(student.arrival_minutes)}</TableCell>
                    <TableCell className="tabular-nums">{format_clock(started)}</TableCell>
                    <TableCell className="tabular-nums">{format_clock(student.completion_minutes)}</TableCell>
                    <TableCell className="tabular-nums">{student.waiting_minutes} min</TableCell>
                    <TableCell className="tabular-nums">{student.flow_minutes} min</TableCell>
                    <TableCell>{in_session ? YES_LABEL : NO_LABEL}</TableCell>
                  </TableRow>
                )
              })}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  )
}
