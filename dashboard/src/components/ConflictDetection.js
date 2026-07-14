export default function ConflictDetection() {
  const conflicts = [
    {
      id: 1,
      event1: "Weekly Standup",
      event2: "Sync with Alice",
      overlap: "30 mins",
      time: "Tomorrow, 10:00 AM"
    }
  ];

  return (
    <div className="glass-panel" style={{ border: '1px solid rgba(245, 158, 11, 0.4)' }}>
      <h2 style={{ fontSize: '1.2rem', marginBottom: '16px', color: 'var(--accent-orange)' }}>
        ⚡ Schedule Conflicts
      </h2>
      <div className="scrollable-list" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {conflicts.map(conflict => (
          <div key={conflict.id} style={{ 
            background: 'rgba(254, 243, 199, 0.5)', 
            padding: '16px', 
            borderRadius: '12px',
          }}>
            <p style={{ fontWeight: '600', marginBottom: '8px' }}>Overlap Detected: {conflict.overlap}</p>
            <p style={{ fontSize: '0.9rem', marginBottom: '4px' }}>🔴 {conflict.event1}</p>
            <p style={{ fontSize: '0.9rem', marginBottom: '12px' }}>🔴 {conflict.event2}</p>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '12px' }}>
              Time: {conflict.time}
            </p>
            
            <div style={{ display: 'flex', gap: '8px', flexDirection: 'column' }}>
              <button className="btn" style={{ background: 'white', border: '1px solid #d1d5db', color: '#111827' }}>
                Reschedule {conflict.event2}
              </button>
              <button className="btn" style={{ background: 'white', border: '1px solid #d1d5db', color: '#111827' }}>
                Keep Both
              </button>
            </div>
          </div>
        ))}
        {conflicts.length === 0 && (
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>No conflicts detected.</p>
        )}
      </div>
    </div>
  );
}
