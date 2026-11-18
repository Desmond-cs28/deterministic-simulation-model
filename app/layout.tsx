import type { Metadata } from "next"
import { Fraunces, IBM_Plex_Mono, Outfit } from "next/font/google"

import "./globals.css"

const body_font = Outfit({
  subsets: ["latin"],
  variable: "--font-body",
})

const display_font = Fraunces({
  subsets: ["latin"],
  variable: "--font-display",
})

const mono_font = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono-lab",
})

export const metadata: Metadata = {
  title: "Palm University College registration desk",
  description:
    "A deterministic simulation of one morning of course registration at Palm University College, Manya Jorpanya.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${body_font.variable} ${display_font.variable} ${mono_font.variable}`}>
      <body className="antialiased">{children}</body>
    </html>
  )
}
