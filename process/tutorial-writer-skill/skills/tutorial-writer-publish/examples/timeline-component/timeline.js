class RagTimeline {
  constructor(containerId, dataUrl) {
    this.container = document.getElementById(containerId);
    this.dataUrl = dataUrl;
    this.activePhase = 0;
    this.isDragging = false;
    this.init();
  }

  async init() {
    const resp = await fetch(this.dataUrl);
    this.data = await resp.json();
    this.render();
    this.bindEvents();
  }

  render() {
    const { phases, display } = this.data;
    const active = phases[this.activePhase];

    this.container.innerHTML = `
      <div class="rag-timeline">
        <div class="timeline-track">
          <div class="timeline-slider" style="left: ${this.activePhase * 25}%"></div>
          ${phases.map((p, i) => `
            <div class="timeline-node ${i === this.activePhase ? 'active' : ''}"
                 data-index="${i}" data-phase="${p.id}">
              <span class="node-label">${p.label}</span>
              <span class="node-period">${p.period}</span>
            </div>
          `).join('')}
        </div>
        <div class="timeline-content">
          <h3>${active.label} <small>${active.period}</small></h3>
          <p>${active.description}</p>
          <div class="metrics-grid">
            ${Object.entries(active.metrics).map(([key, val]) => `
              <div class="metric-card">
                <div class="metric-label">${display.metricLabels[key]}</div>
                <div class="metric-bar">
                  <div class="metric-fill" style="width: ${typeof val === 'number' && val <= 1 ? val * 100 : Math.min(val / 40, 100)}%"></div>
                </div>
                <div class="metric-value">${typeof val === 'number' && val <= 1 ? (val * 100).toFixed(0) + '%' : val}</div>
              </div>
            `).join('')}
          </div>
          <pre><code>${active.codeSnippet}</code></pre>
        </div>
      </div>
    `;
  }

  bindEvents() {
    const slider = this.container.querySelector('.timeline-slider');
    const track = this.container.querySelector('.timeline-track');

    const moveTo = (clientX) => {
      const rect = track.getBoundingClientRect();
      const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
      const phase = Math.round(x / rect.width * (this.data.phases.length - 1));
      if (phase !== this.activePhase) {
        this.activePhase = phase;
        this.render();
        this.bindEvents();
      }
    };

    slider.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      document.addEventListener('mousemove', onDrag);
      document.addEventListener('mouseup', () => {
        this.isDragging = false;
        document.removeEventListener('mousemove', onDrag);
      });
    });

    const onDrag = (e) => { if (this.isDragging) moveTo(e.clientX); };

    track.addEventListener('click', (e) => {
      if (!this.isDragging) moveTo(e.clientX);
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const el = document.getElementById('rag-timeline');
  if (el) new RagTimeline('rag-timeline', 'js/timeline-data.json');
});
