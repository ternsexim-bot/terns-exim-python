import { useState, useEffect, useCallback } from 'react'
import { getLeads, getStats, updateLead, deleteLead, createLead } from '../api/leads'
import LeadStats from './LeadStats'
import LeadsTable from './LeadsTable'
import AddLeadModal from './AddLeadModal'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '@/components/ui/select'

const STATUSES = ['New', 'Contacted', 'Negotiation', 'Won', 'Lost']
const ALL_STATUS = '__all__'

const EMPTY_STATS = { total: 0, new: 0, contacted: 0, negotiation: 0, won: 0, lost: 0 }

export default function Dashboard() {
  const [leads, setLeads]           = useState([])
  const [stats, setStats]           = useState(EMPTY_STATS)
  const [loading, setLoading]       = useState(false)
  const [error, setError]           = useState(null)
  const [statusFilter, setFilter]   = useState('')
  const [showModal, setShowModal]   = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [leadsData, statsData] = await Promise.all([
        getLeads(statusFilter),
        getStats(),
      ])
      setLeads(leadsData)
      setStats(statsData)
    } catch {
      setError('Cannot reach CRM API. Check that terns-exim-api.onrender.com is running.')
    } finally {
      setLoading(false)
    }
  }, [statusFilter])

  useEffect(() => { load() }, [load])

  const refreshStats = async () => {
    const statsData = await getStats()
    setStats(statsData)
  }

  const handleStatusChange = async (id, status) => {
    try {
      const updated = await updateLead(id, { status })
      setLeads(prev => prev.map(l => (l.id === id ? updated : l)))
      await refreshStats()
    } catch {
      setError('Failed to update lead status.')
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this lead? This cannot be undone.')) return
    try {
      await deleteLead(id)
      setLeads(prev => prev.filter(l => l.id !== id))
      await refreshStats()
    } catch {
      setError('Failed to delete lead.')
    }
  }

  const handleAdd = async (data) => {
    try {
      const lead = await createLead(data)
      if (!statusFilter || statusFilter === lead.status) {
        setLeads(prev => [lead, ...prev])
      }
      await refreshStats()
      setShowModal(false)
    } catch {
      setError('Failed to create lead.')
    }
  }

  return (
    <div className="flex min-h-screen flex-col">
      <div className="sticky top-0 z-[100] flex h-14 items-center justify-between bg-navy px-7 text-white shadow-md">
        <div className="text-[17px] font-bold tracking-wide">
          TERNS EXIM <span className="text-gold">CRM</span>
        </div>
        <div className="text-xs text-white/50">Lead Management Dashboard</div>
      </div>

      <div className="mx-auto w-full max-w-[1600px] flex-1 p-7">
        {error && (
          <div className="mb-5 rounded-lg border border-red-200 bg-red-50 px-4 py-2.5 text-[13px] text-red-800">
            {error}
          </div>
        )}

        <LeadStats stats={stats} />

        <div>
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div className="text-base font-semibold text-slate-900">
              All Leads ({leads.length})
            </div>
            <div className="flex items-center gap-2">
              <Select
                value={statusFilter || ALL_STATUS}
                onValueChange={(v) => setFilter(v === ALL_STATUS ? '' : v)}
              >
                <SelectTrigger className="h-9 w-[160px]"><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value={ALL_STATUS}>All Status</SelectItem>
                  {STATUSES.map(s => (
                    <SelectItem key={s} value={s}>{s}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button variant="outline" size="sm" onClick={load}>
                ↻ Refresh
              </Button>
              <Button
                size="sm"
                className="bg-gold text-navy hover:bg-gold-dark hover:text-white"
                onClick={() => setShowModal(true)}
              >
                + Add Lead
              </Button>
            </div>
          </div>

          <LeadsTable
            leads={leads}
            loading={loading}
            onStatusChange={handleStatusChange}
            onDelete={handleDelete}
          />
        </div>
      </div>

      {showModal && (
        <AddLeadModal onClose={() => setShowModal(false)} onAdd={handleAdd} />
      )}
    </div>
  )
}
