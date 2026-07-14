export default function QuickActions() {
  const actions = [
    { id: 1, label: "Create Event", icon: "✨", primary: true },
    { id: 2, label: "Sync Calendar", icon: "🔄" },
    { id: 3, label: "Ask AI", icon: "🤖" },
    { id: 4, label: "Import/Export", icon: "📥" },
    { id: 5, label: "Connect Platform", icon: "🔗" }
  ];

  return (
    <div className="glass-panel" style={{ padding: '16px 24px' }}>
      <div className="flex-between" style={{ gap: '16px', overflowX: 'auto', whiteSpace: 'nowrap' }}>
        {actions.map(action => (
          <button 
            key={action.id} 
            className={`btn ${action.primary ? 'btn-primary' : ''}`}
            style={!action.primary ? { background: 'rgba(255,255,255,0.8)', border: '1px solid var(--border-color)', color: 'var(--text-primary)' } : {}}
          >
            <span style={{ marginRight: '8px' }}>{action.icon}</span>
            {action.label}
          </button>
        ))}
      </div>
    </div>
  );
}
