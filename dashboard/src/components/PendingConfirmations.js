export default function PendingConfirmations() {
  const pending = [
    {
      id: 1,
      sender: "Alice Johnson",
      platform: "Discord",
      original: "Let's do a sync tomorrow at 10am for 30 mins.",
      title: "Sync with Alice",
      time: "Tomorrow, 10:00 AM",
      confidence: 94
    },
    {
      id: 2,
      sender: "marketing@startup.com",
      platform: "Gmail",
      original: "Webinar: The future of AI is starting on Nov 15 at 2pm PST.",
      title: "Webinar: Future of AI",
      time: "Nov 15, 2:00 PM PST",
      confidence: 82
    }
  ];

  return (
    <div className="glass-panel">
      <h2 style={{ fontSize: '1.2rem', marginBottom: '16px' }}>⚠️ Pending Confirmations</h2>
      <div className="scrollable-list" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {pending.map(item => (
          <div key={item.id} style={{ 
            background: 'rgba(255,255,255,0.6)', 
            padding: '16px', 
            borderRadius: '12px',
            border: '1px solid rgba(239, 68, 68, 0.2)' 
          }}>
            <div className="flex-between" style={{ marginBottom: '8px' }}>
              <span className="badge badge-ask" style={{ fontSize: '0.7rem' }}>Action Required</span>
              <span style={{ fontSize: '0.8rem', color: 'var(--accent-green)', fontWeight: 'bold' }}>{item.confidence}% Confidence</span>
            </div>
            
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontStyle: 'italic', marginBottom: '8px' }}>
              "{item.original}"
            </p>
            
            <div style={{ background: 'rgba(255,255,255,0.8)', padding: '12px', borderRadius: '8px', marginBottom: '12px' }}>
              <p style={{ fontWeight: '600' }}>{item.title}</p>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{item.time} via {item.platform}</p>
            </div>
            
            <div style={{ display: 'flex', gap: '8px' }}>
              <button className="btn btn-success" style={{ flex: 1 }}>Accept</button>
              <button className="btn" style={{ flex: 1, background: '#e2e8f0' }}>Edit</button>
              <button className="btn btn-danger" style={{ flex: 1 }}>Reject</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
