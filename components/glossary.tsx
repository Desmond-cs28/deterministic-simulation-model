const TERMS = [
  {
    term: "Students processed",
    meaning: "Every student who completes all four activities. In this model the hall stays open until the cohort is done, so this equals the cohort size.",
  },
  {
    term: "Finished in session",
    meaning: "Students whose card is issued at or before the session length. The rest are still in the hall when the working period ends.",
  },
  {
    term: "Makespan",
    meaning: "Minutes from opening until the last student finishes. This is the total time required to complete registration.",
  },
  {
    term: "Overtime",
    meaning: "Makespan minus the session length, when the makespan is longer. Zero means the cohort is clear before the close.",
  },
  {
    term: "Utilisation",
    meaning: "Busy minutes divided by units × makespan. Officer busy time is fixed for a cohort (every student needs the same officer minutes); utilisation falls when you add units or when the day grows.",
  },
  {
    term: "Idle time",
    meaning: "Resource-minutes when a unit is not serving a student, from opening until the makespan. Gaps on the timeline are idle time.",
  },
  {
    term: "Service efficiency",
    meaning: "Total processing minutes divided by processing plus student waiting. It is the share of a student's time in the hall that is spent being served.",
  },
  {
    term: "Schedule efficiency",
    meaning: "A lower bound on the makespan divided by the makespan actually achieved. It shows how close the dispatch rule comes to the best time that resource limits allow.",
  },
  {
    term: "Efficiency score",
    meaning: "The fraction of the cohort finished inside the session, multiplied by overall utilisation. The study ranks allocations by students finished, then by this utilisation, so the winner clears the morning without spare desks sitting idle.",
  },
] as const

export function Glossary() {
  return (
    <section aria-labelledby="glossary-title" className="rounded-xl bg-card p-5 ring-1 ring-foreground/10">
      <h2 id="glossary-title" className="font-heading text-2xl tracking-tight">
        How the measures are defined
      </h2>
      <dl className="mt-4 grid gap-4 sm:grid-cols-2">
        {TERMS.map((item) => (
          <div key={item.term}>
            <dt className="font-medium">{item.term}</dt>
            <dd className="mt-1 text-sm leading-relaxed text-muted-foreground">{item.meaning}</dd>
          </div>
        ))}
      </dl>
    </section>
  )
}
