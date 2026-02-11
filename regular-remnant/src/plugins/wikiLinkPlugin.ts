import fs from 'node:fs'
import path from 'node:path'
import matter from 'gray-matter'
import wikiLinkPlugin from 'remark-wiki-link'

const postsDir = path.resolve('content/posts')

// Build lookup maps from post files (case-insensitive)
const titleToId = new Map<string, string>()
const slugToId = new Map<string, string>()
const fullIdSet = new Map<string, string>()

const files = fs.readdirSync(postsDir).filter((f) => f.endsWith('.md') || f.endsWith('.mdx'))

for (const file of files) {
  if (file.startsWith('_')) continue
  const id = file.replace(/\.mdx?$/, '')
  const slug = id.replace(/^\d{4}-\d{2}-\d{2}-/, '')

  fullIdSet.set(id.toLowerCase(), id)
  slugToId.set(slug.toLowerCase(), id)

  try {
    const raw = fs.readFileSync(path.join(postsDir, file), 'utf-8')
    const { data } = matter(raw)
    if (data.title) {
      titleToId.set(String(data.title).toLowerCase(), id)
    }
  } catch {
    // skip files that can't be parsed
  }
}

const allPermalinks = [...new Set([...titleToId.values(), ...slugToId.values(), ...fullIdSet.values()])]

function pageResolver(name: string): string[] {
  const lower = name.toLowerCase()
  const byTitle = titleToId.get(lower)
  if (byTitle) return [byTitle]
  const bySlug = slugToId.get(lower)
  if (bySlug) return [bySlug]
  const byFullId = fullIdSet.get(lower)
  if (byFullId) return [byFullId]
  return [name]
}

function hrefTemplate(permalink: string): string {
  return `/posts/${permalink}/`
}

export default function remarkWikiLinks() {
  return [
    wikiLinkPlugin,
    {
      permalinks: allPermalinks,
      pageResolver,
      hrefTemplate,
      aliasDivider: '|',
      wikiLinkClassName: 'internal',
      newClassName: 'new'
    }
  ] as const
}
