import { readFileSync } from "node:fs"
import { join } from "node:path"

import { NextResponse } from "next/server"

export const dynamic = "force-static"

const HTML_TYPE = "text/html; charset=utf-8"

export function GET() {
  const page_path = join(process.cwd(), "index.html")
  const page_html = readFileSync(page_path, "utf8")
  return new NextResponse(page_html, {
    headers: { "content-type": HTML_TYPE },
  })
}
