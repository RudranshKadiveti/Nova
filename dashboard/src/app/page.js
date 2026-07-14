'use client';
import { useState, useEffect } from 'react';
import './globals.css';

export default function Dashboard() {
  const [senders, setSenders] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('ask');

  const filteredSenders = senders.filter(s => s.action_rule === activeTab);

  const fetchData = async () => {
    try {
      const [sendersRes, eventsRes] = await Promise.all([
        fetch('/api/senders'),
        fetch('/api/events')
      ]);
      const sendersData = await sendersRes.json();
      const eventsData = await eventsRes.json();
      
      setSenders(sendersData || []);
      setEvents(eventsData || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchData();
    
    // Poll every 3 seconds to keep UI responsive and instantly show new emails/events
    const intervalId = setInterval(() => {
      fetchData();
    }, 3000);
    
    return () => clearInterval(intervalId);
  }, []);

  const updateSenderAction = async (id, action_rule) => {
    // Optimistic UI update so it immediately jumps to the correct tab
    setSenders(senders.map(s => s.id === id ? { ...s, action_rule } : s));
    
    try {
      await fetch(`/api/senders/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action_rule })
      });
      // Background refetch to ensure events and true state are in sync
      fetchData();
    } catch (err) {
      console.error('Failed to update sender:', err);
      // Revert on failure by refetching
      fetchData();
    }
  };

  if (loading) return <div className="spinner"></div>;

  return (
    <div className="dashboard-layout">
      {/* Header */}
      <header className="flex-between" style={{ marginBottom: '8px' }}>
        <div>
          <h1>AI Calendar Assistant</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '4px' }}>
            System Status: Active & Monitoring
          </p>
        </div>
      </header>

      {/* Google Calendar Full Width */}
      <div className="glass-panel" style={{ padding: '0', overflow: 'hidden' }}>
        <h2 style={{ padding: '16px 24px', margin: 0, borderBottom: '1px solid var(--border-color)', background: '#f8fafc' }}>
          Schedule Overview
        </h2>
        <div style={{ height: '600px', width: '100%' }}>
          <iframe 
            src="https://calendar.google.com/calendar/embed?src=primary&mode=WEEK&ctz=Asia/Kolkata" 
            style={{ border: 0, width: '100%', height: '100%' }} 
            frameBorder="0" 
            scrolling="no"
          ></iframe>
        </div>
      </div>

      <div className="grid-cols-2">
        {/* Sender Permissions */}
        <div className="glass-panel" style={{ padding: '0', overflow: 'hidden' }}>
          <div style={{ padding: '16px 24px', borderBottom: '1px solid var(--border-color)', background: '#f8fafc' }}>
            <h2 style={{ margin: 0, borderBottom: 'none', paddingBottom: 0 }}>
              Sender Permissions
            </h2>
            <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
              <button className={`btn ${activeTab === 'ask' ? 'btn-primary' : ''}`} onClick={() => setActiveTab('ask')}>Pending</button>
              <button className={`btn ${activeTab === 'auto-sync' ? 'btn-primary' : ''}`} onClick={() => setActiveTab('auto-sync')}>Approved</button>
              <button className={`btn ${activeTab === 'ignore' ? 'btn-primary' : ''}`} onClick={() => setActiveTab('ignore')}>Ignored</button>
            </div>
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Platform</th>
                  <th>Identifier</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredSenders.map(sender => (
                  <tr key={sender.id}>
                    <td style={{ fontWeight: '500', textTransform: 'capitalize' }}>{sender.platform}</td>
                    <td>{sender.identifier}</td>
                    <td>
                      <span className={`badge badge-${sender.action_rule}`}>
                        {sender.action_rule}
                      </span>
                    </td>
                    <td className="gap-2" style={{ display: 'flex' }}>
                      {sender.action_rule !== 'auto-sync' && (
                        <button className="btn" onClick={() => updateSenderAction(sender.id, 'auto-sync')}>Approve</button>
                      )}
                      {sender.action_rule !== 'ignore' && (
                        <button className="btn" onClick={() => updateSenderAction(sender.id, 'ignore')}>Ignore</button>
                      )}
                      {sender.action_rule !== 'ask' && (
                        <button className="btn" onClick={() => updateSenderAction(sender.id, 'ask')}>Ask</button>
                      )}
                    </td>
                  </tr>
                ))}
                {filteredSenders.length === 0 && (
                  <tr><td colSpan="4" style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>No senders found in this category.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Intercepted Events */}
        <div className="glass-panel" style={{ padding: '0', overflow: 'hidden' }}>
          <h2 style={{ padding: '16px 24px', margin: 0, borderBottom: '1px solid var(--border-color)', background: '#f8fafc' }}>
            Intercepted Events
          </h2>
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Start Time</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {events.map(event => (
                  <tr key={event.id}>
                    <td style={{ fontWeight: '500' }}>{event.title}</td>
                    <td style={{ color: 'var(--text-secondary)' }}>
                      {event.start_time ? new Date(event.start_time).toLocaleString(undefined, {
                        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                      }) : 'Time unspecified'}
                    </td>
                    <td>
                      <span className={`badge badge-${event.status}`}>
                        {event.status}
                      </span>
                    </td>
                  </tr>
                ))}
                {events.length === 0 && (
                  <tr><td colSpan="3" style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>No events intercepted.</td></tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
