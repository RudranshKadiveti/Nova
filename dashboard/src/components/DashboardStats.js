export default function DashboardStats() {
  const stats = [
    { label: "Events Created", value: "142", trend: "+12%", color: "var(--accent-blue)" },
    { label: "Notifications Processed", value: "1,402", trend: "+5%", color: "var(--text-primary)" },
    { label: "Automation Success Rate", value: "98.5%", trend: "+0.5%", color: "var(--accent-green)" },
    { label: "Duplicates Prevented", value: "24", trend: "-2%", color: "var(--accent-orange)" },
    { label: "Avg AI Confidence", value: "96%", trend: "+1%", color: "var(--text-primary)" },
    { label: "Time Saved", value: "42 hrs", trend: "+4 hrs", color: "var(--accent-blue)" },
  ];

  return (
    <div className="grid-cols-3">
      {stats.map((stat, i) => (
        <div key={i} className="glass-panel" style={{ padding: '20px' }}>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '8px', fontWeight: '500' }}>
            {stat.label}
          </p>
          <div className="flex-between">
            <h3 style={{ fontSize: '1.8rem', color: stat.color, margin: 0 }}>{stat.value}</h3>
            <span style={{ 
              fontSize: '0.8rem', 
              fontWeight: '600', 
              color: stat.trend.startsWith('+') ? 'var(--accent-green)' : 'var(--accent-red)',
              background: stat.trend.startsWith('+') ? '#d1fae5' : '#fee2e2',
              padding: '4px 8px',
              borderRadius: '999px'
            }}>
              {stat.trend}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
