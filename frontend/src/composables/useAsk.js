import { ref } from 'vue'

const BASE = import.meta.env.VITE_API_URL ?? ''

export function useAsk() {
  const submitting = ref(false)
  const submitted  = ref(false)
  const ackNumber  = ref('')
  const errorMsg   = ref('')

  async function submitQuery(payload) {
    if (submitting.value) return   // duplicate-click guard
    submitting.value = true
    errorMsg.value   = ''
    try {
      const res  = await fetch(`${BASE}/api/ask`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify(payload),
      })
      const json = await res.json()
      if (json.error) throw new Error(json.error.message)
      ackNumber.value = json.data.ack_number
      submitted.value = true
    } catch (e) {
      errorMsg.value = e.message || 'Submission failed. Please try again.'
    } finally {
      submitting.value = false
    }
  }

  function reset() {
    submitted.value  = false
    ackNumber.value  = ''
    errorMsg.value   = ''
  }

  return { submitting, submitted, ackNumber, errorMsg, submitQuery, reset }
}
