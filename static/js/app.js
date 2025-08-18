document.addEventListener('DOMContentLoaded', () => {
  const newsList = document.getElementById('news-list');
  if (newsList) {
    fetch('/static/data/news.json')
      .then(r => r.json())
      .then(items => {
        if (!Array.isArray(items) || !items.length) {
          newsList.innerHTML = `<div class="col-12"><div class="alert alert-info">No news available.</div></div>`;
          return;
        }
        newsList.innerHTML = items.map(n => `
          <div class="col-md-6">
            <div class="card p-3 h-100">
              <div class="d-flex justify-content-between align-items-start">
                <div class="fw-bold">${n.title}</div>
                <span class="badge bg-light text-dark border">${n.source}</span>
              </div>
              <div class="small text-muted mb-2">${n.date}</div>
              <p class="mb-2">${n.summary}</p>
              <a class="btn btn-sm btn-outline-primary" href="${n.url}">Read</a>
            </div>
          </div>
        `).join('');
      })
      .catch(() => {
        newsList.innerHTML = `<div class="col-12"><div class="alert alert-danger">Failed to load news.</div></div>`;
      });
  }
});
