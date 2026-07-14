export default function InsightsWidget() {
  const insights = [
    { icon: "📅", title: "Busiest Day", value: "Thursday (8 meetings)" },
    { icon: "🕒", title: "Free Time Today", value: "4.5 hours remaining" },
    { icon: "⏰", title: "Upcoming Deadlines", value: "3 due this week" },
    { icon: "🤖", title: "AI Events Added", value: "12 this week" }
  ];

  return (
    <div className="glass-panel">
      <h2 style={{ fontSize: '1.2rem', marginBottom: '16px' }}>🧠 AI Insights</h2>
      <div className="grid-cols-2">
        {insights.map((insight, i) => (
          <div key={i} style={{ 
            background: 'rgba(255,255,255,0.5)', 
            padding: '12px 16px', 
            borderRadius: '12px',
            border: '1px solid rgba(255,255,255,0.8)'
          }}>
            <div className="flex-between">
              <span style={{ fontSize: '1.5rem' }}>{insight.icon}</span>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: '600', textTransform: 'uppercase' }}>
                {insight.title}
              </span>
            </div>
            <p style={{ marginTop: '8px', fontWeight: '600', fontSize: '1.1rem' }}>{insight.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
