import type { RawRssItem } from './types.ts'

/**
 * Minimal feed parser — zero dependencies. Auto-detects RSS 2.0 vs Atom by
 * the root element. Handles the subset every mainstream feed uses; not a
 * general-purpose XML parser. Swap for `fast-xml-parser` if you hit a feed
 * it can't read.
 */
export function parseFeed(xml: string): RawRssItem[] {
  return isAtom(xml) ? parseAtom(xml) : parseRss20(xml)
}

function isAtom(xml: string): boolean {
  return /<feed\b[^>]*xmlns\s*=\s*["']http:\/\/www\.w3\.org\/2005\/Atom["']/i.test(xml)
}

function parseRss20(xml: string): RawRssItem[] {
  const items: RawRssItem[] = []
  for (const match of xml.matchAll(/<item\b[^>]*>([\s\S]*?)<\/item>/g)) {
    const body = match[1] ?? ''
    items.push({
      title: pickTag(body, 'title'),
      link: pickTag(body, 'link'),
      description: pickTag(body, 'description') ?? pickTag(body, 'content:encoded'),
      pubDate: pickTag(body, 'pubDate') ?? pickTag(body, 'dc:date'),
      creator: pickTag(body, 'dc:creator') ?? pickTag(body, 'author'),
      guid: pickTag(body, 'guid'),
      categories: pickAllTags(body, 'category'),
    })
  }
  return items
}

function parseAtom(xml: string): RawRssItem[] {
  const items: RawRssItem[] = []
  for (const match of xml.matchAll(/<entry\b[^>]*>([\s\S]*?)<\/entry>/g)) {
    const body = match[1] ?? ''
    items.push({
      title: pickTag(body, 'title'),
      link: pickAtomLink(body),
      description: pickTag(body, 'summary') ?? pickTag(body, 'content'),
      pubDate: pickTag(body, 'published') ?? pickTag(body, 'updated'),
      creator: pickAtomAuthor(body),
      guid: pickTag(body, 'id'),
      categories: pickAttrAll(body, 'category', 'term'),
    })
  }
  return items
}

function pickAtomLink(body: string): string | undefined {
  const links = [...body.matchAll(/<link\b([^>]*)\/?>/gi)].map((m) => parseAttrs(m[1] ?? ''))
  const alternate = links.find((a) => a.rel === 'alternate' || a.rel === undefined)
  return alternate?.href
}

function pickAtomAuthor(body: string): string | undefined {
  const block = body.match(/<author\b[^>]*>([\s\S]*?)<\/author>/i)?.[1]
  if (!block) return undefined
  return pickTag(block, 'name')
}

function pickTag(body: string, tag: string): string | undefined {
  const re = new RegExp(`<${escapeTag(tag)}\\b[^>]*>([\\s\\S]*?)<\\/${escapeTag(tag)}>`, 'i')
  const m = body.match(re)
  if (!m) return undefined
  return cleanValue(m[1] ?? '')
}

function pickAllTags(body: string, tag: string): string[] {
  const re = new RegExp(`<${escapeTag(tag)}\\b[^>]*>([\\s\\S]*?)<\\/${escapeTag(tag)}>`, 'gi')
  const out: string[] = []
  for (const m of body.matchAll(re)) {
    const value = cleanValue(m[1] ?? '')
    if (value) out.push(value)
  }
  return out
}

function pickAttrAll(body: string, tag: string, attr: string): string[] {
  const re = new RegExp(`<${escapeTag(tag)}\\b([^>]*)\\/?>`, 'gi')
  const out: string[] = []
  for (const m of body.matchAll(re)) {
    const value = parseAttrs(m[1] ?? '')[attr]
    if (value) out.push(value)
  }
  return out
}

function parseAttrs(s: string): Record<string, string> {
  const attrs: Record<string, string> = {}
  for (const m of s.matchAll(/(\w[\w:-]*)\s*=\s*"([^"]*)"/g)) {
    if (m[1]) attrs[m[1]] = m[2] ?? ''
  }
  return attrs
}

function escapeTag(tag: string): string {
  return tag.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function cleanValue(raw: string): string {
  const cdata = raw.match(/^<!\[CDATA\[([\s\S]*?)\]\]>$/)
  const value = (cdata ? cdata[1] : raw) ?? ''
  return decodeEntities(value).trim()
}

function decodeEntities(s: string): string {
  return s
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)))
    .replace(/&amp;/g, '&')
}
