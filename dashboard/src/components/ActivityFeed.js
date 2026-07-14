'use client';
import { useState } from 'react';

export default function ActivityFeed() {
  const [activities, setActivities] = useState([
    { id: 1, action: "Created event 'Project Alpha Review'", time: "Just now", icon: "📅", undoable: true },
    { id: 2, action: "Ignored promotional email from Canva", time: "5 mins ago", icon: "🗑️", undoable: true },
    { id: 3, action: "Synced calendar with Google", time: "12 mins ago", icon: "🔄", undoable: false },
    { id: 4, action: "Deleted duplicate 'Lunch with Bob'", time: "1 hour ago", icon: "✂️", undoable: true },
    { id: 5, action: "Added reminder for 'Dentist'", time: "2 hours ago", icon: "⏰", undoable: false },
  ]);

  const handleUndo = (id) => {
    setActivities(activities.filter(a => a.id !== id));
    // Toast notification would go here in a real app
    alert("Action reversed successfully.");
  };

  return (
    <div className="glass-panel">
      <h2 style={{ fontSize: '1.2rem', marginBottom: '16px' }}>📡 AI Activity Feed</h2>
      <div className="scrollable-list" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {activities.map(activity => (
          <div key={activity.id} className="flex-between" style={{ 
            padding: '12px', 
            background: 'rgba(255,255,255,0.6)', 
            borderRadius: '8px' 
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{ fontSize: '1.2rem', background: 'white', padding: '6px', borderRadius: '50%', boxShadow: 'var(--shadow-sm)' }}>
                {activity.icon}
              </span>
              <div>
                <p style={{ fontSize: '0.9rem', fontWeight: '500' }}>{activity.action}</p>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{activity.time}</p>
              </div>
            </div>
            {activity.undoable && (
              <button 
                onClick={() => handleUndo(activity.id)}
                style={{ 
                  background: 'none', 
                  border: 'none', 
                  color: 'var(--accent-blue)', 
                  fontSize: '0.8rem', 
                  fontWeight: '600',
                  cursor: 'pointer',
                  textDecoration: 'underline'
                }}
              >
                Undo
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
