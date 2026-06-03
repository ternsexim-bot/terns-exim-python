const STATUSES = ['New', 'Contacted', 'Negotiation', 'Won', 'Lost']

function fmt(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric',
  })
}

export default function LeadsTable({ leads, loading, onStatusChange, onDelete }) {
  if (loading) {
    return <div className="loading">Loading leads...</div>
  }

  if (!leads.length) {
    return (
      <div className="empty-state">
        <div className="empty-icon">📋</div>
        <p>No leads found. Add your first lead!</p>
      </div>
    )
  }

  return (
    <div className="table-wrapper">
      <table className="leads-table">
        <thead>
          <tr>
            <th>Name / Email</th>
            <th>Phone</th>
            <th>Company</th>
            <th>Country</th>
            <th>Product Interest</th>
            <th>Status</th>
            <th>Source</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {leads.map(lead => (
            <tr key={lead.id}>
              <td>
                <div className="lead-name">{lead.name}</div>
                {lead.email && <div className="lead-email">{lead.email}</div>}
              </td>
              <td>{lead.phone || '—'}</td>
              <td>{lead.company || '—'}</td>
              <td>{lead.country || '—'}</td>
              <td>{lead.product_interest || '—'}</td>
              <td>
                <select
                  className="status-select"
                  value={lead.status}
                  onChange={e => onStatusChange(lead.id, e.target.value)}
                >
                  {STATUSES.map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </td>
              <td>{lead.source || '—'}</td>
              <td>{fmt(lead.created_at)}</td>
              <td>
                <button
                  className="btn-delete"
                  onClick={() => onDelete(lead.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
