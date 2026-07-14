export default function GlobalSearch() {
  return (
    <div style={{ position: 'relative', width: '100%', maxWidth: '600px', margin: '0 auto' }}>
      <input 
        type="text" 
        className="search-input" 
        placeholder="Search events, people, and notifications..." 
      />
      <span style={{ position: 'absolute', right: '16px', top: '12px', fontSize: '1.2rem', color: 'var(--text-secondary)' }}>
        🔍
      </span>
    </div>
  );
}
