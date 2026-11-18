/**
 * Compare the TypeScript engine with a fixture written by the Python program.
 * Usage: python -m registration_sim --export-parity tests/fixtures/parity.json && npx tsx scripts/parity.ts
 */

import { readFileSync } from "node:fs"

import { EMPTY_COUNT, FIRST_INDEX, INDEX_STEP, PARITY_ROUND_DIGITS, ScenarioId } from "../lib/constants"
import { simulate } from "../lib/engine"
import { default_config, recommend, run_study } from "../lib/experiments"
import { measure } from "../lib/metrics"
import type { SimulationConfig } from "../lib/types"

type FixtureCase = {
  scenario_id: string
  officer_count: number
  computer_count: number
  student_count: number
  interarrival_minutes: number
  working_period_minutes: number
  metrics: Record<string, number>
  assignments?: Array<Record<string, number | string>>
}

const FLOAT_KEYS = new Set([
  "average_waiting_minutes",
  "average_flow_minutes",
  "officer_utilisation",
  "computer_utilisation",
  "overall_utilisation",
  "service_efficiency",
  "schedule_efficiency",
  "completion_ratio",
  "efficiency_score",
  "productivity_per_resource_hour",
  "average_students_waiting",
])

function nearly_equal(left: number, right: number): boolean {
  const tolerance = 10 ** -PARITY_ROUND_DIGITS
  return Math.abs(left - right) <= tolerance
}

function main(): void {
  const path = process.argv[2] ?? "tests/fixtures/parity.json"
  const cases = JSON.parse(readFileSync(path, "utf8")) as FixtureCase[]
  let failures = 0
  for (const fixture of cases) {
    const config: SimulationConfig = {
      student_count: fixture.student_count,
      interarrival_minutes: fixture.interarrival_minutes,
      officer_count: fixture.officer_count,
      computer_count: fixture.computer_count,
      working_period_minutes: fixture.working_period_minutes,
    }
    const metrics = measure(simulate(config))
    for (const [key, expected] of Object.entries(fixture.metrics)) {
      const actual = metrics[key as keyof typeof metrics]
      if (typeof actual !== "number") {
        continue
      }
      const matches = FLOAT_KEYS.has(key) ? nearly_equal(actual, expected) : actual === expected
      if (!matches) {
        failures += 1
        console.error(
          `Mismatch ${fixture.student_count} students, ${fixture.officer_count}+${fixture.computer_count}, ${key}: ts=${actual} py=${expected}`,
        )
      }
    }
    if (fixture.assignments) {
      const actual_rows = simulate(config).assignments
      if (actual_rows.length !== fixture.assignments.length) {
        failures += 1
        console.error(`Assignment count ${actual_rows.length} != ${fixture.assignments.length}`)
      }
      for (let index = FIRST_INDEX; index < actual_rows.length; index += INDEX_STEP) {
        const actual = actual_rows[index]
        const expected = fixture.assignments[index]
        const fields = [
          "student_index",
          "activity_id",
          "resource_kind",
          "resource_index",
          "ready_minutes",
          "start_minutes",
          "end_minutes",
        ] as const
        for (const field of fields) {
          if (actual[field] !== expected[field]) {
            failures += 1
            console.error(`Assignment ${index} ${field}: ts=${actual[field]} py=${expected[field]}`)
          }
        }
      }
    }
  }

  const chosen = recommend(run_study(default_config()))
  if (chosen.scenario.scenario_id !== ScenarioId.LEAN) {
    failures += INDEX_STEP
    console.error(`Recommendation ${chosen.scenario.scenario_id}`)
  }

  if (failures > EMPTY_COUNT) {
    console.error(`${failures} mismatches`)
    process.exit(1)
  }
  console.log(`Parity ok across ${cases.length} cases`)
}

main()
