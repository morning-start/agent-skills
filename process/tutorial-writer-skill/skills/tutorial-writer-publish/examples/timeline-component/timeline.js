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
    this.bindKeyboard();
  }

  render() {
    const { phases, display } = this.data;
    const active = phases[this.activePhase];

    this.container.innerHTML = `
      <div class="rag-timeline" role="region" aria-label="技术演进时间轴">
        <div class="timeline-track" role="slider" aria-valuenow="${this.activePhase + 1}" aria-valuemin="1" aria-valuemax="${phases.length}">
          <div class="timeline-slider" style="left: ${this.activePhase * 25}%"></div>
          ${phases.map((p, i) => `
            <div class="timeline-node ${i === this.activePhase ? 'active' : ''}"
                 data-index="${i}" data-phase="${p.id}" tabindex="0" role="button" aria-label="${p.label}：${p.period}">
              <span class="node-label">${p.label}</span>
              <span class="node-period">${p.period}</span>
            </div>
          `).join('')}
        </div>
        <div class="timeline-content timeline-fade-in">
          <h3>${active.label} <small>${active.period}</small></h3>
          <p>${active.description}</p>
          <div class="metrics-grid">
            ${Object.entries(active.metrics).map(([key, val]) => {
              const pct = typeof val === 'number' && val <= 1 ? val * 100 : Math.min(val / 40, 100);
              return `
              <div class="metric-card">
                <div class="metric-label">${display.metricLabels[key]}</div>
                <div class="metric-bar">
                  <div class="metric-fill" style="width: 0%" data-target="${pct}"></div>
                </div>
                <div class="metric-value" data-counter="${typeof val === 'number' && val <= 1 ? (val * 100).toFixed(0) : val}">0</div>
              </div>
            `}).join('')}
          </div>
          <pre><code>${active.codeSnippet}</code></pre>
        </div>
      </div>
    `;

    this.animateMetrics();
  }

  animateMetrics() {
    const fills = this.container.querySelectorAll('.metric-fill');
    const counters = this.container.querySelectorAll('.metric-value');

    fills.forEach(fill => {
      const target = parseFloat(fill.dataset.target);
      requestAnimationFrame(() => { fill.style.width = target + '%'; });
    });

    counters.forEach(counter => {
      const target = parseFloat(counter.dataset.counter);
      const duration = 600;
      const start = performance.now();
      const step = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        counter.textContent = Math.floor(target * eased);
        if (progress < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    });
  }

  bindEvents() {
    const slider = this.container.querySelector('.timeline-slider');
    const track = this.container.querySelector('.timeline-track');

    const moveTo = (clientX) => {
      const rect = track.getBoundingClientRect();
      const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
      const phase = Math.round(x / rect.width * (this.data.phases.length - 1));
      if (phase !== this.activePhase) {
        this.goTo(phase);
      }
    };

    slider.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      slider.style.cursor = 'grabbing';
      document.addEventListener('mousemove', onDrag);
      document.addEventListener('mouseup', () => {
        this.isDragging = false;
        slider.style.cursor = 'grab';
        document.removeEventListener('mousemove', onDrag);
      });
    });

    const onDrag = (e) => { if (this.isDragging) moveTo(e.clientX); };

    track.addEventListener('click', (e) => {
      if (!this.isDragging) moveTo(e.clientX);
    });

    // Touch support
    slider.addEventListener('touchstart', (e) => {
      this.isDragging = true;
      document.addEventListener('touchmove', onTouchDrag, { passive: true });
      document.addEventListener('touchend', () => {
        this.isDragging = false;
        document.removeEventListener('touchmove', onTouchDrag);
      });
    }, { passive: true });

    const onTouchDrag = (e) => {
      if (this.isDragging) moveTo(e.touches[0].clientX);
    };

    // Click on node labels
    this.container.querySelectorAll('.timeline-node').forEach(node => {
      node.addEventListener('click', () => {
        const idx = parseInt(node.dataset.index);
        if (idx !== this.activePhase) this.goTo(idx);
      });
    });
  }

  bindKeyboard() {
    document.addEventListener('keydown', (e) => {
      const isFocused = this.container.contains(document.activeElement);
      if (!isFocused) return;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        this.goTo(Math.min(this.activePhase + 1, this.data.phases.length - 1));
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        this.goTo(Math.max(this.activePhase - 1, 0));
      } else if (e.key === 'Home') {
        e.preventDefault();
        this.goTo(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        this.goTo(this.data.phases.length - 1);
      }
    });
  }

  goTo(index) {
    this.activePhase = index;
    this.render();
    this.bindEvents();
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const el = document.getElementById('rag-timeline');
  if (el) new RagTimeline('rag-timeline', 'js/timeline-data.json');
});
