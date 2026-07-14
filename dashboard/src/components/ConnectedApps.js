export default function ConnectedApps() {
  const apps = [
    { name: "Google Calendar", icon: "📅", status: "Connected", health: "100%", lastSync: "2 mins ago" },
    { name: "Gmail", icon: "📧", status: "Connected", health: "98%", lastSync: "5 mins ago" },
    { name: "Discord", icon: "💬", status: "Connected", health: "100%", lastSync: "1 min ago" },
    { name: "Telegram", icon: "✈️", status: "Connected", health: "100%", lastSync: "Just now" },
    { name: "Slack", icon: "🏢", status: "Disconnected", health: "0%", lastSync: "Never" },
    { name: "WhatsApp", icon: "📞", status: "Connected", health: "92%", lastSync: "10 mins ago" }
  ];

  return (
    <div className="glass-panel">
      <div className="flex-between" style={{ marginBottom: '16px' }}>
        <h2 style={{ fontSize: '1.2rem', margin: 0 }}>🔌 Connected Apps</h2>
        <button className="btn btn-primary" style={{ padding: '4px 12px', fontSize: '0.8rem' }}>+ Add App</button>
      </div>
      
      <div className="grid-cols-2" style={{ gap: '12px' }}>
        {apps.map((app, i) => (
          <div key={i} style={{ 
            background: 'rgba(255,255,255,0.7)', 
            padding: '12px', 
            borderRadius: '12px',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }}>
            <div className="flex-between">
              <span style={{ fontSize: '1.2rem' }}>{app.icon} {app.name}</span>
              <span style={{ 
                height: '8px', 
                width: '8px', 
                borderRadius: '50%', 
                background: app.status === 'Connected' ? 'var(--accent-green)' : 'var(--accent-red)' 
              }}></span>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              <span>Health: {app.health}</span>
              <span>Sync: {app.lastSync}</span>
            </div>
            
            {app.status === 'Disconnected' && (
              <button className="btn" style={{ background: '#e2e8f0', width: '100%', marginTop: '4px', fontSize: '0.8rem', padding: '4px' }}>
                Reconnect
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
