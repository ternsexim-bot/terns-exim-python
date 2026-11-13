import { Card } from '@/components/ui/card'
import { cn } from '@/lib/utils'

const CARDS = [
  { key: 'total', label: 'Total Leads', borderCls: 'border-l-navy' },
  { key: 'new', label: 'New', borderCls: 'border-l-blue-500' },
  { key: 'contacted', label: 'Contacted', borderCls: 'border-l-violet-500' },
  { key: 'negotiation', label: 'Negotiation', borderCls: 'border-l-amber-500' },
  { key: 'won', label: 'Won', borderCls: 'border-l-emerald-500' },
  { key: 'lost', label: 'Lost', borderCls: 'border-l-red-500' },
]

export default function LeadStats({ stats }) {
  return (
    <div className="mb-6 grid grid-cols-[repeat(auto-fit,minmax(150px,1fr))] gap-4">
      {CARDS.map(({ key, label, borderCls }) => (
        <Card
          key={key}
          className={cn('border-l-4 px-5 py-4 shadow-sm', borderCls)}
        >
          <div className="text-[34px] font-bold leading-none text-slate-900">
            {stats[key] ?? 0}
          </div>
          <div className="mt-1.5 text-[11px] font-semibold uppercase tracking-wide text-slate-500">
            {label}
          </div>
        </Card>
      ))}
    </div>
  )
}
