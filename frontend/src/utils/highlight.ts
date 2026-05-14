function escapeHtml(value: string) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function escapeRegExp(value: string) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

export function highlightKeyword(value: string | null | undefined, keyword: string | null | undefined) {
  const text = value ?? ''
  const term = keyword?.trim()

  if (!term) {
    return escapeHtml(text)
  }

  const pattern = new RegExp(`(${escapeRegExp(term)})`, 'gi')
  return escapeHtml(text).replace(pattern, '<mark class="keyword-highlight">$1</mark>')
}
