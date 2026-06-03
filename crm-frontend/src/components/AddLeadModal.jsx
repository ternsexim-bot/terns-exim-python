import { useState } from 'react'

const PRODUCTS = [
  'Hex Bolts', 'Anchor Bolts', 'Foundation Bolts',
  'Nuts', 'Washers', 'Threaded Rods', 'General Enquiry',
]

const SOURCES = ['Website', 'Email', 'Phone', 'WhatsApp', 'Trade Fair', 'Referral', 'Other']

const BLANK = {
  name: '', email: '', phone: '', company: '',
  country: '', product_interest: '', message: '',
  source: 'Website', status: 'New',
}

export default function AddLeadModal({ onClose, onAdd }) {
  const [form, setForm] = useState(BLANK)
  const [submitting, setSubmitting] = useState(false)

  const set = (k) => (e) => setForm(prev => ({ ...prev, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    await onAdd(form)
    setSubmitting(false)
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Add New Lead</h2>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>

        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-row">
            <div className="form-group">
              <label>Name *</label>
              <input
                required
                value={form.name}
                onChange={set('name')}
                placeholder="Full name"
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={form.email}
                onChange={set('email')}
                placeholder="email@example.com"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Phone</label>
              <input value={form.phone} onChange={set('phone')} placeholder="+91 99999 99999" />
            </div>
            <div className="form-group">
              <label>Company</label>
              <input value={form.company} onChange={set('company')} placeholder="Company name" />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Country</label>
              <input value={form.country} onChange={set('country')} placeholder="USA, UAE, UK..." />
            </div>
            <div className="form-group">
              <label>Product Interest</label>
              <select value={form.product_interest} onChange={set('product_interest')}>
                <option value="">Select product</option>
                {PRODUCTS.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Source</label>
              <select value={form.source} onChange={set('source')}>
                {SOURCES.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Status</label>
              <select value={form.status} onChange={set('status')}>
                {['New', 'Contacted', 'Negotiation', 'Won', 'Lost'].map(s => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Message / Notes</label>
            <textarea
              value={form.message}
              onChange={set('message')}
              placeholder="Customer's inquiry or internal notes..."
              rows={3}
            />
          </div>

          <div className="modal-actions">
            <button type="button" className="btn-cancel" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn-submit" disabled={submitting}>
              {submitting ? 'Saving...' : 'Add Lead'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
