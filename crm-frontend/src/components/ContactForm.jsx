import { useState } from 'react'
import { createLead } from '../api/leads'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '@/components/ui/select'
import { cn } from '@/lib/utils'

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

const PRODUCTS = [
  'Hex Bolts', 'Anchor Bolts', 'Foundation Bolts',
  'Nuts', 'Washers', 'Threaded Rods', 'General Enquiry',
]

function validate({ name, email, phone }) {
  const errors = {}

  const trimmedName = name.trim()
  if (!trimmedName) {
    errors.name = 'Name is required'
  } else if (trimmedName.length < 2) {
    errors.name = 'Name must be at least 2 characters'
  }

  const trimmedEmail = email.trim()
  if (!trimmedEmail) {
    errors.email = 'Email is required'
  } else if (!EMAIL_RE.test(trimmedEmail)) {
    errors.email = 'Enter a valid email'
  }

  const trimmedPhone = phone.trim()
  if (!trimmedPhone) {
    errors.phone = 'Phone is required'
  } else if (/[^\d\s+\-()]/.test(trimmedPhone)) {
    errors.phone = 'Enter a valid phone number'
  } else {
    const digits = trimmedPhone.replace(/\D/g, '')
    if (digits.length < 7 || digits.length > 15) {
      errors.phone = 'Enter a valid phone number'
    }
  }

  return errors
}

const BLANK = { name: '', email: '', phone: '', product_interest: '', message: '' }

export default function ContactForm() {
  const [form, setForm]             = useState(BLANK)
  const [errors, setErrors]         = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [status, setStatus]         = useState(null) // 'success' | 'error'

  const set = (k) => (e) => setForm(prev => ({ ...prev, [k]: e.target.value }))
  const setField = (k) => (v) => setForm(prev => ({ ...prev, [k]: v }))

  const handleSubmit = async (e) => {
    e.preventDefault()

    const errs = validate(form)
    setErrors(errs)
    if (Object.keys(errs).length > 0) return

    setSubmitting(true)
    setStatus(null)
    try {
      // POST JSON to https://terns-exim-api.onrender.com/leads
      await createLead({
        name:             form.name.trim(),
        email:            form.email.trim(),
        phone:            form.phone.trim(),
        product_interest: form.product_interest,
        message:          form.message,
        source:           'CRM Form',
        status:           'New',
      })
      setStatus('success')
      setForm(BLANK)
      setErrors({})
    } catch {
      setStatus('error')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="mx-auto max-w-xl p-6">
      <div className="rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-navy">Product Enquiry</h1>
        <p className="mt-1.5 text-sm text-slate-500">
          Fill in the form and our team will get back to you shortly.
        </p>

        {status === 'success' && (
          <div className="mt-4 rounded-md border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
            Enquiry submitted successfully. We will contact you shortly.
          </div>
        )}
        {status === 'error' && (
          <div className="mt-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
            Something went wrong. Please try again.
          </div>
        )}

        <form onSubmit={handleSubmit} noValidate className="mt-6 flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <Label>Name *</Label>
            <Input
              value={form.name}
              onChange={set('name')}
              placeholder="Your full name"
              className={cn(errors.name && 'border-red-400 focus-visible:ring-red-400')}
            />
            {errors.name && <span className="text-xs text-red-600">{errors.name}</span>}
          </div>

          <div className="flex flex-col gap-1.5">
            <Label>Email *</Label>
            <Input
              type="email"
              value={form.email}
              onChange={set('email')}
              placeholder="email@example.com"
              className={cn(errors.email && 'border-red-400 focus-visible:ring-red-400')}
            />
            {errors.email && <span className="text-xs text-red-600">{errors.email}</span>}
          </div>

          <div className="flex flex-col gap-1.5">
            <Label>Phone *</Label>
            <Input
              value={form.phone}
              onChange={set('phone')}
              placeholder="+91 99999 99999"
              className={cn(errors.phone && 'border-red-400 focus-visible:ring-red-400')}
            />
            {errors.phone && <span className="text-xs text-red-600">{errors.phone}</span>}
          </div>

          <div className="flex flex-col gap-1.5">
            <Label>Product</Label>
            <Select value={form.product_interest} onValueChange={setField('product_interest')}>
              <SelectTrigger><SelectValue placeholder="Select product (optional)" /></SelectTrigger>
              <SelectContent>
                {PRODUCTS.map(p => <SelectItem key={p} value={p}>{p}</SelectItem>)}
              </SelectContent>
            </Select>
          </div>

          <div className="flex flex-col gap-1.5">
            <Label>Message</Label>
            <Textarea
              value={form.message}
              onChange={set('message')}
              placeholder="Tell us about your requirements..."
              rows={4}
            />
          </div>

          <Button type="submit" disabled={submitting} className="mt-2 bg-gold text-navy hover:bg-gold-dark hover:text-white">
            {submitting ? 'Submitting...' : 'Send Enquiry'}
          </Button>
        </form>
      </div>
    </div>
  )
}
