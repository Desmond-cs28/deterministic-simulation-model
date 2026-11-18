export function SectionBlock({
  id,
  kicker,
  title,
  lede,
  children,
}: {
  id: string
  kicker: string
  title: string
  lede?: string
  children: React.ReactNode
}) {
  return (
    <section id={id} className="scroll-mt-8">
      <p className="font-mono text-[0.72rem] tracking-[0.16em] text-primary uppercase">{kicker}</p>
      <h2 className="font-heading mt-1 text-3xl tracking-tight text-foreground sm:text-4xl">{title}</h2>
      {lede ? <p className="mt-3 max-w-3xl text-base leading-relaxed text-muted-foreground">{lede}</p> : null}
      <div className="mt-6">{children}</div>
    </section>
  )
}
