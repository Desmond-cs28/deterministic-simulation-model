const NAV_ITEMS = [
  { href: "#model", label: "Model" },
  { href: "#lab", label: "Run" },
  { href: "#experiments", label: "Experiments" },
  { href: "#sensitivity", label: "Sensitivity" },
  { href: "#reading", label: "Reading" },
] as const

export function Masthead() {
  return (
    <header className="bg-secondary text-secondary-foreground">
      <div className="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-8 sm:px-6 sm:py-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <p className="font-mono text-[0.72rem] tracking-[0.18em] text-[#f0d3a2] uppercase">
            Ashworth University · North Hall
          </p>
          <p className="font-mono text-[0.72rem] tracking-[0.14em] text-secondary-foreground/70 uppercase">
            Computer simulation · Project 2
          </p>
        </div>
        <div className="grid gap-6 lg:grid-cols-[1.4fr_0.8fr] lg:items-end">
          <div>
            <h1 className="font-heading max-w-xl text-4xl leading-[1.05] tracking-tight sm:text-5xl">
              Registration centre simulator
            </h1>
            <p className="mt-4 max-w-xl text-base leading-relaxed text-secondary-foreground/80 sm:text-lg">
              A deterministic model of one morning session. Arrivals, processing times, and the pools of
              officers and computers are known before the doors open. The schedule that follows is the
              same every time you run it.
            </p>
          </div>
          <dl className="grid grid-cols-3 gap-3 border border-white/15 p-4 sm:gap-4">
            <Stat kicker="Opens" value="08:00" />
            <Stat kicker="Cohort" value="36" />
            <Stat kicker="Session" value="4 h" />
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
      <dt className="font-mono text-[0.68rem] tracking-[0.14em] text-[#f0d3a2] uppercase">{kicker}</dt>
      <dd className="font-heading mt-1 text-2xl">{value}</dd>
    </div>
  )
}
