const COLOR = {
  New:         'background:#dbeafe;color:#1d4ed8',
  Contacted:   'background:#ede9fe;color:#6d28d9',
  Negotiation: 'background:#fef3c7;color:#92400e',
  Won:         'background:#d1fae5;color:#065f46',
  Lost:        'background:#fee2e2;color:#991b1b',
}

export default function StatusBadge({ status }) {
  const style = COLOR[status] ?? 'background:#f1f5f9;color:#374151'
  return (
    <span style={{
      display: 'inline-block',
      padding: '3px 10px',
      borderRadius: 99,
      fontSize: 11,
      fontWeight: 700,
      letterSpacing: 0.3,
      textTransform: 'uppercase',
      ...Object.fromEntries(style.split(';').map(s => s.split(':')))
    }}>
      {status}
    </span>
  )
}
