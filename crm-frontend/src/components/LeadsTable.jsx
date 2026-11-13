import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from '@/components/ui/table'
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'

const STATUSES = ['New', 'Contacted', 'Negotiation', 'Won', 'Lost']

function fmt(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
}

export default function LeadsTable({ leads, loading, onStatusChange, onDelete }) {
  if (loading) {
    return <div className="py-16 text-center text-slate-500">Loading leads...</div>
  }

  if (!leads.length) {
    return (
      <div className="flex flex-col items-center gap-3 py-16 text-slate-500">
        <div className="text-4xl">📋</div>
        <p>No leads found. Add your first lead!</p>
      </div>
    )
  }

  return (
    <div className="rounded-lg border border-slate-200">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name / Email</TableHead>
            <TableHead>Phone</TableHead>
            <TableHead>Company</TableHead>
            <TableHead>Country</TableHead>
            <TableHead>Product Interest</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Source</TableHead>
            <TableHead>Date</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {leads.map(lead => (
            <TableRow key={lead.id}>
              <TableCell>
                <div className="font-medium text-slate-900">{lead.name}</div>
                {lead.email && <div className="text-xs text-slate-500">{lead.email}</div>}
              </TableCell>
              <TableCell>{lead.phone || '—'}</TableCell>
              <TableCell>{lead.company || '—'}</TableCell>
              <TableCell>{lead.country || '—'}</TableCell>
              <TableCell>{lead.product_interest || '—'}</TableCell>
              <TableCell>
                <Select value={lead.status} onValueChange={(v) => onStatusChange(lead.id, v)}>
                  <SelectTrigger className="h-8 w-[140px] text-sm">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {STATUSES.map(s => (
                      <SelectItem key={s} value={s}>{s}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </TableCell>
              <TableCell>{lead.source || '—'}</TableCell>
              <TableCell>{fmt(lead.created_at)}</TableCell>
              <TableCell className="text-right">
                <Button
                  variant="outline"
                  size="sm"
                  className="border-red-200 text-red-600 hover:bg-red-50 hover:text-red-700"
                  onClick={() => onDelete(lead.id)}
                >
                  Delete
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
