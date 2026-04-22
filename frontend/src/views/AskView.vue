<template>
  <div class="ask-view">

    <header class="ask-header">
      <h1 class="ask-title">Ask AI Adoption</h1>
      <p class="ask-subtitle">Have a question about AI tools, training, or initiatives? The AI Adoption team is here to help.</p>
    </header>

    <div class="ask-body">

      <!-- ── Left: form or confirmation ───────────────────── -->
      <div class="ask-main">

        <!-- Confirmation card -->
        <div v-if="submitted" class="confirm-card">
          <div class="confirm-check">✓</div>
          <h2 class="confirm-title">Query Submitted!</h2>
          <p class="confirm-text">Your query has been received. We'll follow up on your registered email address within 2–3 business days.</p>

          <div class="ack-box">
            <span class="ack-label">Your Acknowledgment Number</span>
            <span class="ack-number">{{ ackNumber }}</span>
            <span class="ack-hint">Save this number when following up with the team.</span>
          </div>

          <button class="btn-reset" @click="handleReset">Submit another query</button>
        </div>

        <!-- Form card -->
        <div v-else class="form-card">
          <div class="form-card-title">
            <MessageSquare :size="15" class="form-card-icon" />
            Submit your query
          </div>

          <form @submit.prevent="handleSubmit" novalidate>

            <!-- Row 1: Name + Email -->
            <div class="form-row">
              <div class="form-field" :class="{ 'field--error': errors.name }">
                <label class="field-label">Name <span class="field-req">*</span></label>
                <input v-model="form.name" type="text" class="field-input"
                  placeholder="Your full name" @input="errors.name = ''" />
                <span v-if="errors.name" class="field-msg">{{ errors.name }}</span>
              </div>
              <div class="form-field" :class="{ 'field--error': errors.email }">
                <label class="field-label">Email <span class="field-req">*</span></label>
                <input v-model="form.email" type="email" class="field-input"
                  placeholder="you@dewa.gov.ae" @input="errors.email = ''" />
                <span v-if="errors.email" class="field-msg">{{ errors.email }}</span>
              </div>
            </div>

            <!-- Row 2: Division + Department -->
            <div class="form-row">
              <div class="form-field" :class="{ 'field--error': errors.division }">
                <label class="field-label">Division <span class="field-req">*</span></label>
                <input v-model="form.division" type="text" class="field-input"
                  placeholder="e.g. Generation" @input="errors.division = ''" />
                <span v-if="errors.division" class="field-msg">{{ errors.division }}</span>
              </div>
              <div class="form-field" :class="{ 'field--error': errors.department }">
                <label class="field-label">Department / Section <span class="field-req">*</span></label>
                <input v-model="form.department" type="text" class="field-input"
                  placeholder="e.g. AI & Data Analytics" @input="errors.department = ''" />
                <span v-if="errors.department" class="field-msg">{{ errors.department }}</span>
              </div>
            </div>

            <!-- Query Type -->
            <div class="form-field" :class="{ 'field--error': errors.query_type }">
              <label class="field-label">Query Type <span class="field-req">*</span></label>
              <select v-model="form.query_type" class="field-input field-select"
                @change="errors.query_type = ''">
                <option value="" disabled>Select a category…</option>
                <option value="Tools">Tools</option>
                <option value="Trainings">Trainings</option>
                <option value="Team Related">Team Related</option>
                <option value="Others">Others</option>
              </select>
              <span v-if="errors.query_type" class="field-msg">{{ errors.query_type }}</span>
            </div>

            <!-- Message -->
            <div class="form-field" :class="{ 'field--error': errors.message }">
              <label class="field-label">Your Message <span class="field-req">*</span></label>
              <textarea v-model="form.message" class="field-input field-textarea" rows="4"
                placeholder="Describe your question or concern in detail…"
                @input="errors.message = ''"></textarea>
              <span v-if="errors.message" class="field-msg">{{ errors.message }}</span>
            </div>

            <!-- API error -->
            <div v-if="errorMsg" class="api-error">{{ errorMsg }}</div>

            <!-- Submit -->
            <button type="submit" class="btn-submit" :disabled="submitting">
              <Loader2 v-if="submitting" :size="14" class="btn-spin" />
              {{ submitting ? 'Submitting…' : 'Submit Query' }}
            </button>

          </form>
        </div>
      </div>

      <!-- ── Right: static info sidebar ───────────────────── -->
      <aside class="ask-sidebar">

        <div class="info-card">
          <div class="info-card-title">What happens next?</div>
          <ol class="info-steps">
            <li class="info-step">
              <span class="step-num">1</span>
              <div class="step-body">
                <strong>Acknowledged</strong>
                <span>You receive a unique reference number instantly.</span>
              </div>
            </li>
            <li class="info-step">
              <span class="step-num">2</span>
              <div class="step-body">
                <strong>Team review</strong>
                <span>The AI Adoption team reviews and routes your query.</span>
              </div>
            </li>
            <li class="info-step">
              <span class="step-num">3</span>
              <div class="step-body">
                <strong>Response</strong>
                <span>We follow up directly on your registered email.</span>
              </div>
            </li>
          </ol>
        </div>

        <div class="info-card info-meta">
          <div class="info-meta-row">
            <Clock :size="13" class="info-meta-icon" />
            <span><strong>Response time:</strong> 2–3 business days</span>
          </div>
          <div class="info-meta-row">
            <MapPin :size="13" class="info-meta-icon" />
            <span>AI Adoption Dept · 8th Al Shera'a Building, Dubai</span>
          </div>
        </div>

      </aside>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { MessageSquare, Loader2, Clock, MapPin } from 'lucide-vue-next'
import { useAsk } from '../composables/useAsk.js'

const { submitting, submitted, ackNumber, errorMsg, submitQuery, reset } = useAsk()

const form = reactive({ name: '', email: '', division: '', department: '', query_type: '', message: '' })
const errors = reactive({ name: '', email: '', division: '', department: '', query_type: '', message: '' })

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/

function validate() {
  let ok = true
  const req = (k, msg) => { if (!form[k].trim()) { errors[k] = msg; ok = false } }
  req('name',       'Name is required.')
  req('division',   'Division is required.')
  req('department', 'Department / Section is required.')
  req('message',    'Please describe your query.')
  if (!form.email.trim())                          { errors.email      = 'Email is required.';            ok = false }
  else if (!EMAIL_RE.test(form.email.trim()))      { errors.email      = 'Enter a valid email address.'; ok = false }
  if (!form.query_type)                            { errors.query_type = 'Please select a query type.';  ok = false }
  return ok
}

async function handleSubmit() {
  if (!validate()) return
  await submitQuery({
    name:       form.name.trim(),
    email:      form.email.trim(),
    division:   form.division.trim(),
    department: form.department.trim(),
    query_type: form.query_type,
    message:    form.message.trim(),
  })
}

function handleReset() {
  reset()
  Object.keys(form).forEach(k => (form[k] = ''))
  Object.keys(errors).forEach(k => (errors[k] = ''))
}
</script>

<style scoped>
.ask-view { padding: 32px 40px; max-width: 900px; --accent: #7c3aed; --accent-light: #f3e8ff; }

/* Header */
.ask-header {
  border-left: 4px solid var(--accent);
  border-bottom: 1px solid #e2e0dc;
  border-radius: 0 6px 0 0;
  background: #f8f7f5;
  padding: 14px 18px;
  margin-bottom: 24px;
}
.ask-title    { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #1a1917; margin: 0 0 4px; }
.ask-subtitle { font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; color: #3a3834; margin: 0; text-shadow: 0 1px 0 rgba(255,255,255,0.85); }

/* Two-column layout */
.ask-body { display: grid; grid-template-columns: 1fr 280px; gap: 20px; align-items: start; }
.ask-main { display: flex; flex-direction: column; gap: 0; }

/* Form card */
.form-card {
  background: #fff;
  border: 1px solid #e2e0dc;
  border-top: 3px solid var(--accent);
  border-radius: 10px;
  padding: 22px 24px;
}
.form-card-title {
  display: flex; align-items: center; gap: 7px;
  font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 700;
  color: #1a1917; margin-bottom: 20px;
}
.form-card-icon { color: var(--accent); }

/* Form grid */
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-field { display: flex; flex-direction: column; gap: 5px; margin-bottom: 14px; }
.form-field:last-of-type { margin-bottom: 0; }

.field-label { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 700; color: #3a3834; }
.field-req   { color: var(--accent); }

.field-input {
  font-family: 'DM Sans', sans-serif; font-size: 13px; color: #1a1917;
  background: #faf9f7; border: 1.5px solid #e2e0dc; border-radius: 7px;
  padding: 9px 12px; outline: none; transition: border-color 150ms, box-shadow 150ms;
  width: 100%; box-sizing: border-box;
}
.field-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(124,58,237,0.1); }
.field--error .field-input { border-color: #d93535; }
.field-select { cursor: pointer; appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2365635d' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; padding-right: 32px; }
.field-textarea { resize: vertical; min-height: 100px; }
.field-msg { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #d93535; }

.api-error { background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; padding: 10px 14px; font-family: 'DM Sans', sans-serif; font-size: 13px; color: #d93535; margin: 14px 0 0; }

/* Submit button */
.btn-submit {
  display: inline-flex; align-items: center; gap: 7px; margin-top: 18px;
  background: var(--accent); color: #fff; border: none; border-radius: 8px;
  padding: 11px 28px; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 700;
  cursor: pointer; transition: opacity 150ms;
}
.btn-submit:hover:not(:disabled) { opacity: 0.88; }
.btn-submit:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Confirmation card */
.confirm-card {
  background: #fff; border: 1px solid #e2e0dc; border-top: 3px solid #16a34a;
  border-radius: 10px; padding: 32px 28px; display: flex; flex-direction: column;
  align-items: center; text-align: center; gap: 12px;
}
.confirm-check { width: 52px; height: 52px; border-radius: 50%; background: #dcfce7; color: #16a34a; font-size: 22px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.confirm-title { font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; color: #1a1917; margin: 0; }
.confirm-text  { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #65635d; margin: 0; max-width: 340px; }

.ack-box {
  background: var(--accent-light); border: 1px solid rgba(124,58,237,0.2);
  border-radius: 10px; padding: 16px 24px; display: flex; flex-direction: column;
  align-items: center; gap: 4px; width: 100%; box-sizing: border-box;
}
.ack-label  { font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: var(--accent); }
.ack-number { font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; color: var(--accent); letter-spacing: 0.04em; }
.ack-hint   { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #85837c; }

.btn-reset { background: none; border: none; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 600; color: var(--accent); cursor: pointer; margin-top: 4px; padding: 0; text-decoration: underline; transition: opacity 150ms; }
.btn-reset:hover { opacity: 0.75; }

/* Sidebar */
.ask-sidebar { display: flex; flex-direction: column; gap: 12px; }
.info-card {
  background: #fff; border: 1px solid #e2e0dc; border-top: 3px solid var(--accent);
  border-radius: 10px; padding: 18px 20px;
}
.info-card-title { font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 700; color: #1a1917; margin-bottom: 14px; }
.info-steps { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 12px; }
.info-step  { display: flex; align-items: flex-start; gap: 10px; }
.step-num   { width: 22px; height: 22px; border-radius: 50%; background: var(--accent-light); color: var(--accent); font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; }
.step-body  { display: flex; flex-direction: column; gap: 2px; }
.step-body strong { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 700; color: #1a1917; }
.step-body span   { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #85837c; line-height: 1.4; }

.info-meta { border-top-color: #e2e0dc; display: flex; flex-direction: column; gap: 8px; }
.info-meta-row  { display: flex; align-items: flex-start; gap: 8px; font-family: 'DM Sans', sans-serif; font-size: 12px; color: #65635d; line-height: 1.4; }
.info-meta-icon { color: var(--accent); flex-shrink: 0; margin-top: 2px; }

@media (max-width: 760px) {
  .ask-view { padding: 20px; }
  .ask-body { grid-template-columns: 1fr; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
