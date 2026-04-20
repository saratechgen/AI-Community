import { ref, onMounted } from 'vue'

/**
 * Generic static JSON fetcher.
 * Swap `url` for an API endpoint later — component stays unchanged.
 *
 * @param {string} url  Path under /public (e.g. '/data/hero.json')
 */
export function useStaticJson(url) {
  const data    = ref(null)
  const loading = ref(true)
  const error   = ref(null)

  onMounted(async () => {
    try {
      const res = await fetch(url)
      if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`)
      data.value = await res.json()
    } catch (e) {
      error.value = e.message
      console.error(e)
    } finally {
      loading.value = false
    }
  })

  return { data, loading, error }
}
