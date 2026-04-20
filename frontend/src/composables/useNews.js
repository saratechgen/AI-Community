import { ref } from 'vue'

export function useNews() {
  const news = ref({
    claude:       [],
    aiAgents:     [],
    aiAtWork:     [],
    advancements: [],
    quickTips:    [],
  })
  const loading = ref(false)
  const error   = ref(null)
  const brief   = ref('')

  async function fetchNews() {
    loading.value = true
    error.value   = null
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL ?? 'http://localhost:8001'}/api/news`)
      if (!res.ok) throw new Error(`Server error: ${res.status}`)
      const json = await res.json()
      if (json.error) throw new Error(json.error.message)
      news.value  = json.data
      brief.value = json.meta?.brief ?? ''
    } catch (e) {
      error.value = 'Could not load news. Please try again later.'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  return { news, loading, error, fetchNews, brief }
}
