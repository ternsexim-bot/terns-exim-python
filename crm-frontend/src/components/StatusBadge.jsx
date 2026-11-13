import { Badge } from '@/components/ui/badge'

const STATUS_CLASSES = {
  New: 'border-transparent bg-blue-100 text-blue-700 hover:bg-blue-100',
  Contacted: 'border-transparent bg-violet-100 text-violet-700 hover:bg-violet-100',
  Negotiation: 'border-transparent bg-amber-100 text-amber-800 hover:bg-amber-100',
  Won: 'border-transparent bg-emerald-100 text-emerald-800 hover:bg-emerald-100',
  Lost: 'border-transparent bg-red-100 text-red-800 hover:bg-red-100',
}

const DEFAULT_CLASSES = 'border-transparent bg-slate-100 text-slate-600 hover:bg-slate-100'

export default function StatusBadge({ status }) {
  return (
    <Badge className={`${STATUS_CLASSES[status] ?? DEFAULT_CLASSES} font-bold uppercase tracking-wide text-[11px]`}>
      {status}
    </Badge>
  )
}
