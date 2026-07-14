export default function RecentNotifications() {
  const notifications = [
    { id: 1, platform: "Telegram", sender: "@crypto_king", time: "10:45 AM", decision: "Ignored (Spam)", event: false, confidence: 99 },
    { id: 2, platform: "Gmail", sender: "boss@company.com", time: "09:30 AM", decision: "Created Event", event: true, confidence: 95 },
    { id: 3, platform: "Discord", sender: "Design Team", time: "Yesterday", decision: "Created Event", event: true, confidence: 88 },
    { id: 4, platform: "WhatsApp", sender: "Mom", time: "Yesterday", decision: "Ignored (Chatter)", event: false, confidence: 92 },
  ];

  return (
    <div className="glass-panel">
      <h2 style={{ fontSize: '1.2rem', marginBottom: '16px' }}>📩 Recent Notifications</h2>
      <div style={{ overflowX: 'auto' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Platform & Sender</th>
              <th>Time</th>
              <th>AI Decision</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {notifications.map(n => (
              <tr key={n.id}>
                <td>
                  <div style={{ fontWeight: '600' }}>{n.platform}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{n.sender}</div>
                </td>
                <td style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{n.time}</td>
                <td>
                  <span className={`badge ${n.event ? 'badge-auto-sync' : 'badge-ignore'}`}>
                    {n.decision}
                  </span>
                </td>
                <td style={{ fontWeight: '600', color: n.confidence > 90 ? 'var(--accent-green)' : 'var(--accent-orange)' }}>
                  {n.confidence}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
