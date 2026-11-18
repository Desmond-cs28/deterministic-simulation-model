const TERMS = [
  {
    term: "Students processed",
    meaning: "Students who finish the registry check, the Student Portal, and the timetable. The desk stays open until the last student is done, so this equals the morning's group.",
  },
  {
    term: "Finished in session",
    meaning: "Students who have their timetable at or before the desk closes. The rest are still waiting or being served when the session ends.",
  },
  {
    term: "Makespan",
    meaning: "Minutes from 08:00 until the last student leaves. This is the total time the morning takes.",
  },
  {
    term: "Overtime",
    meaning: "How many minutes the last student finishes after the desk was meant to close. Zero means everyone is done on time.",
  },
  {
    term: "Utilisation",
    meaning: "The share of the morning an officer or a computer is actually serving a student. Adding a person or a machine that has little to do lowers this.",
  },
  {
    term: "Idle time",
    meaning: "Minutes an officer or a computer is free while the desk is still open. Gaps on the timeline are idle time.",
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
