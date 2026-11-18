import {
  ActivityId,
  CARD_ISSUE_MINUTES,
  COURSE_ENROLMENT_MINUTES,
  DOCUMENT_VERIFICATION_MINUTES,
  FEE_ASSESSMENT_MINUTES,
  ResourceKind,
  ZERO_MINUTES,
} from "./constants"
import type { ActivitySpec } from "./types"

export const ACTIVITY_SEQUENCE: readonly ActivitySpec[] = [
  {
    activity_id: ActivityId.DOCUMENT_VERIFICATION,
    label: "Document verification",
    short_label: "Documents",
    resource_kind: ResourceKind.OFFICER,
    processing_minutes: DOCUMENT_VERIFICATION_MINUTES,
    description:
      "An officer checks the admission letter, identity document, and prerequisite record.",
  },
  {
    activity_id: ActivityId.COURSE_ENROLMENT,
    label: "Course enrolment",
    short_label: "Enrolment",
    resource_kind: ResourceKind.COMPUTER,
    processing_minutes: COURSE_ENROLMENT_MINUTES,
    description:
      "The student enters course selections on a registration computer and writes them to the student information system.",
  },
  {
    activity_id: ActivityId.FEE_ASSESSMENT,
    label: "Fee assessment",
    short_label: "Fees",
    resource_kind: ResourceKind.OFFICER,
    processing_minutes: FEE_ASSESSMENT_MINUTES,
    description:
      "An officer calculates tuition, applies a recorded waiver or scholarship, and confirms the payment entry.",
  },
  {
    activity_id: ActivityId.CARD_ISSUE,
    label: "Card and timetable",
    short_label: "Card",
    resource_kind: ResourceKind.COMPUTER,
    processing_minutes: CARD_ISSUE_MINUTES,
    description:
      "A registration computer prints the timetable and encodes the student card.",
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
