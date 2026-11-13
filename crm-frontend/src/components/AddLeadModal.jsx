import { useState } from 'react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
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

const PRODUCTS = [
  'Hex Bolts', 'Anchor Bolts', 'Foundation Bolts',
  'Nuts', 'Washers', 'Threaded Rods', 'General Enquiry',
]

const SOURCES = ['Website', 'Email', 'Phone', 'WhatsApp', 'Trade Fair', 'Referral', 'Other']
const STATUSES = ['New', 'Contacted', 'Negotiation', 'Won', 'Lost']

const BLANK = {
  name: '', email: '', phone: '', company: '',
  country: '', product_interest: '', message: '',
  source: 'Website', status: 'New',
}

export default function AddLeadModal({ onClose, onAdd }) {
  const [form, setForm] = useState(BLANK)
  const [submitting, setSubmitting] = useState(false)

  const set = (k) => (e) => setForm(prev => ({ ...prev, [k]: e.target.value }))
  const setField = (k) => (v) => setForm(prev => ({ ...prev, [k]: v }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    await onAdd(form)
    setSubmitting(false)
  }

  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Add New Lead</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label>Name *</Label>
              <Input required value={form.name} onChange={set('name')} placeholder="Full name" />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label>Email</Label>
              <Input type="email" value={form.email} onChange={set('email')} placeholder="email@example.com" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label>Phone</Label>
              <Input value={form.phone} onChange={set('phone')} placeholder="+91 99999 99999" />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label>Company</Label>
              <Input value={form.company} onChange={set('company')} placeholder="Company name" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label>Country</Label>
              <Input value={form.country} onChange={set('country')} placeholder="USA, UAE, UK..." />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label>Product Interest</Label>
              <Select value={form.product_interest} onValueChange={setField('product_interest')}>
                <SelectTrigger><SelectValue placeholder="Select product" /></SelectTrigger>
                <SelectContent>
                  {PRODUCTS.map(p => <SelectItem key={p} value={p}>{p}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label>Source</Label>
              <Select value={form.source} onValueChange={setField('source')}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  {SOURCES.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div className="flex flex-col gap-1.5">
              <Label>Status</Label>
              <Select value={form.status} onValueChange={setField('status')}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  {STATUSES.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <Label>Message / Notes</Label>
            <Textarea
              value={form.message}
              onChange={set('message')}
              placeholder="Customer's inquiry or internal notes..."
              rows={3}
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={submitting} className="bg-gold text-navy hover:bg-gold-dark hover:text-white">
              {submitting ? 'Saving...' : 'Add Lead'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
