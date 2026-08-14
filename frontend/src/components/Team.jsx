const  MEMBERS = [
  { name: 'Kristi Koju',  email: 'KCE080BCT010', icon: 'fa-user-circle' },
  { name: 'Aamod Baral', email: 'KCE080BCT025', icon: 'fa-user-circle' },
  { name: 'Nishana Budha',  email: 'KCE080BCT017', icon: 'fa-user-circle' },
  { name: 'Reeshav Khyaju',  email: 'KCE080BCT028', icon: 'fa-user-circle' },
];

export default function Team() {
  return (
    <section id="team" className="mt-5 pt-4 fade-section">
      <h2 className="fw-bold">
        <i className="fas fa-users text-primary me-2" />
        Team
      </h2>
      <div className="row g-4 mt-3">
        {MEMBERS.map((member) => (
          <div className="col-md-3 col-sm-6" key={member.name}>
            <div className="card shadow-sm border-0 rounded-4 p-3 text-center h-100">
              <i className={`fas ${member.icon} fa-4x text-secondary`} />
              <h6 className="mt-2 mb-0">{member.name}</h6>
              <p className="text-muted small mb-2">{member.role}</p>
              <span className="badge bg-light text-dark text-truncate">{member.email}</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
