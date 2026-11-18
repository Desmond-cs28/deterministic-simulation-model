import {
  ActivityId,
  PORTAL_REGISTRATION_MINUTES,
  REGISTRY_CHECK_MINUTES,
  ResourceKind,
  TIMETABLE_ISSUE_MINUTES,
  ZERO_MINUTES,
} from "./constants"
import type { ActivitySpec } from "./types"

export const ACTIVITY_SEQUENCE: readonly ActivitySpec[] = [
  {
    activity_id: ActivityId.REGISTRY_CHECK,
    label: "Registry check",
    short_label: "Registry",
    resource_kind: ResourceKind.OFFICER,
    processing_minutes: REGISTRY_CHECK_MINUTES,
    description:
      "A registry officer checks the student ID and confirms the programme: Computer Science, Business Information Technology, or Business Administration.",
  },
  {
    activity_id: ActivityId.PORTAL_REGISTRATION,
    label: "Student Portal registration",
    short_label: "Portal",
    resource_kind: ResourceKind.COMPUTER,
    processing_minutes: PORTAL_REGISTRATION_MINUTES,
    description:
      "The student registers semester courses on a Student Portal computer at the registry desk.",
  },
  {
    activity_id: ActivityId.TIMETABLE_ISSUE,
    label: "Timetable issue",
    short_label: "Timetable",
    resource_kind: ResourceKind.OFFICER,
    processing_minutes: TIMETABLE_ISSUE_MINUTES,
    description: "The officer confirms the course list and issues the printed timetable.",
  },
]

export function processing_minutes_for(resource_kind: ResourceKind): number {
  let total = ZERO_MINUTES
  for (const activity of ACTIVITY_SEQUENCE) {
    if (activity.resource_kind === resource_kind) {
      total += activity.processing_minutes
    }
  }
  return total
}

export function total_processing_minutes(): number {
  let total = ZERO_MINUTES
  for (const activity of ACTIVITY_SEQUENCE) {
    total += activity.processing_minutes
  }
  return total
}
