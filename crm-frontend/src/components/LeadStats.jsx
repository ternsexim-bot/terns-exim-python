const CARDS = [
  { key: 'total',       label: 'Total Leads', cls: '' },
  { key: 'new',         label: 'New',         cls: 'new' },
  { key: 'contacted',   label: 'Contacted',   cls: 'contacted' },
  { key: 'negotiation', label: 'Negotiation', cls: 'negotiation' },
  { key: 'won',         label: 'Won',         cls: 'won' },
  { key: 'lost',        label: 'Lost',        cls: 'lost' },
]

export default function LeadStats({ stats }) {
  return (
    <div className="stats-grid">
      {CARDS.map(({ key, label, cls }) => (
        <div key={key} className={`stat-card ${cls}`}>
          <div className="stat-number">{stats[key] ?? 0}</div>
          <div className="stat-label">{label}</div>
        </div>
      ))}
    </div>
  )
}
