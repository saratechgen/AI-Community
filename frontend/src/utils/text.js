/**
 * Text sanitisation utilities.
 * Rule: ALL user-facing text from external feeds must pass through
 * decodeHtml() before rendering. This is a mandatory convention —
 * see CONVENTIONS.md § Content Sanitisation.
 */

/**
 * Decode HTML entities and strip residual tags from feed text.
 * Uses DOMParser so every named and numeric entity is handled
 * without maintaining a manual replacement list.
 *
 * @param {string} str - Raw text from RSS/API feed
 * @returns {string} Clean, display-safe string
 */
export function decodeHtml(str) {
  if (!str) return ''
  // DOMParser decodes ALL HTML entities (named + numeric)
  const doc = new DOMParser().parseFromString(str, 'text/html')
  const decoded = doc.documentElement.textContent || ''
  // Collapse multiple whitespace and trim
  return decoded.replace(/\s+/g, ' ').trim()
}
