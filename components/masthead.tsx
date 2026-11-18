import { DEFAULT_STUDENT_COUNT } from "@/lib/constants"

const NAV_ITEMS = [
  { href: "#model", label: "Model" },
  { href: "#lab", label: "Run" },
  { href: "#experiments", label: "Experiments" },
  { href: "#reading", label: "Reading" },
] as const

const COHORT_LABEL = String(DEFAULT_STUDENT_COUNT)

export function Masthead() {
  return (
    <header className="bg-secondary text-secondary-foreground">
      <div className="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-8 sm:px-6 sm:py-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <p className="font-mono text-[0.72rem] tracking-[0.18em] text-[#d7ebe3] uppercase">
            Palm University College · Manya Jorpanya
          </p>
          <p className="font-mono text-[0.72rem] tracking-[0.14em] text-secondary-foreground/70 uppercase">
            Computer simulation · Project 2
          </p>
        </div>
        <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr] lg:items-end">
          <div className="flex gap-4">
            <img
              src="/palm-logo.png"
              alt="Palm University College"
              width={72}
              height={72}
              className="h-[72px] w-[72px] shrink-0 rounded-full bg-white"
            />
            <div>
              <h1 className="font-heading max-w-xl text-4xl leading-[1.05] tracking-tight sm:text-5xl">
                Course registration desk
              </h1>
              <p className="mt-4 max-w-xl text-base leading-relaxed text-secondary-foreground/80 sm:text-lg">
                One morning of undergraduate course registration at the Registry. Students arrive on a
                fixed timetable, an officer checks each ID, and a Student Portal computer records the
                courses. The same morning produces the same schedule every time.
              </p>
            </div>
          </div>
          <dl className="grid grid-cols-3 gap-3 border border-white/15 p-4 sm:gap-4">
            <Stat kicker="Opens" value="08:00" />
            <Stat kicker="Students" value={COHORT_LABEL} />
            <Stat kicker="Closes" value="12:00" />
          </dl>
        </div>
        <nav className="flex flex-wrap gap-2" aria-label="Page sections">
          {NAV_ITEMS.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="rounded-full border border-white/20 px-3 py-1.5 text-sm text-secondary-foreground/90 hover:bg-white/10"
            >
              {item.label}
            </a>
          ))}
        </nav>
      </div>
    </header>
  )
}

function Stat({ kicker, value }: { kicker: string; value: string }) {
  return (
    <div>
      <dt className="font-mono text-[0.68rem] tracking-[0.14em] text-[#d7ebe3] uppercase">{kicker}</dt>
      <dd className="font-heading mt-1 text-2xl">{value}</dd>
    </div>
  )
}
