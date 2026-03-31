<template>
  <div class="page">
    <header class="header">
      <div>
        <h1 class="title">Alerts</h1>
        <p class="subtitle">Mocked data</p>
      </div>
      <div class="filters">
        <label class="label">
          Project
          <select v-model="project" class="select">
            <option value="">All</option>
            <option v-for="project in projects" :key="project" :value="project">{{ project }}</option>
          </select>
        </label>
        <label class="label">
          Severity
          <select v-model="severity" class="select">
            <option value="">All</option>
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
          </select>
        </label>
      </div>
    </header>

    <main class="main">
      <div class="grid">
        <article v-for="alert in filtered" :key="alert.id" class="card">
          <div class="cardTop">
            <span class="pill">{{ alert.project }}</span>
            <span class="sev" :data-sev="alert.severity">{{ alert.severity }}</span>
          </div>
          <h3 class="cardTitle">{{ alert.title }}</h3>
          <div class="meta">
            <span>events: <b>{{ alert.events_count }}</b></span>
            <span class="dot">•</span>
            <span class="muted">{{ alert.created_at }}</span>
          </div>
        </article>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";

const alerts = ref([
  {
    id: 1,
    project: "core",
    title: "test alert 1",
    severity: "medium",
    created_at: "2026-03-31 12:00:00",
    events_count: 1
  },
  {
    id: 2,
    project: "core",
    title: "test alert 2",
    severity: "high",
    created_at: "2026-03-31 12:10:00",
    events_count: 0
  },
  {
    id: 3,
    project: "payments",
    title: "test alert 3",
    severity: "high",
    created_at: "2026-03-31 12:20:00",
    events_count: 2
  },
  {
    id: 4,
    project: "infra",
    title: "test alert 4",
    severity: "low",
    created_at: "2026-03-31 12:30:00",
    events_count: 0
  }
]);

const projects = computed(() => Array.from(new Set(alerts.value.map((alert) => alert.project))).sort());
const project = ref("");
const severity = ref("");

const filtered = computed(() => {
  return alerts.value.filter((alert) => {
    if (project.value && alert.project !== project.value) return false;
    return !(severity.value && alert.severity !== severity.value);

  });
});
</script>

<style>
:root {
  color-scheme: dark;
  --bg: #141414;
  --panel: linear-gradient(112deg, rgba(255, 255, 255, 0.00) 63.38%, #FFF 74.62%, rgba(255, 255, 255, 0.00) 86.49%), linear-gradient(284deg, #CCFE77 -5.91%, #FFF 101%);;
  --text: #002417;
  --muted: rgba(20, 20, 20, 0.7);
  --glow1: #022E21;
  --glow2: #FAFAFA;
  --border: #141414
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
  background: radial-gradient(900px 500px at 15% 10%, rgba(241, 241, 241, 0.2), transparent 60%),
    radial-gradient(900px 500px at 85% 90%, rgba(204, 254, 119, 0.1), transparent 60%),
    var(--bg);
  color: var(--text);
}

code {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  padding: 2px 6px;
  border-radius: 8px;
}

.page {
  min-height: 100vh;
  padding: 28px 22px;
  max-width: 1100px;
  margin: 0 auto;
}

.header {
  display: flex;
  gap: 18px;
  align-items: flex-end;
  justify-content: space-between;
  padding: 18px 18px;
  border-radius: 18px;
  border: 1px solid var(--border);
  background: linear-gradient(112deg, rgba(255, 255, 255, 0.00) 63.38%, #FFF 74.62%, rgba(255, 255, 255, 0.00) 86.49%), linear-gradient(284deg, #CCFE77 -5.91%, #FFF 101%);
  backdrop-filter: blur(8px);
}

.title {
  margin: 0;
  font-size: 34px;
  letter-spacing: 0.2px;
}

.subtitle {
  margin: 6px 0 0;
  color: var(--muted);
}

.filters {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.label {
  display: grid;
  gap: 6px;
  font-size: 12px;
  color: var(--muted);
}

.select {
  color: var(--text);
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgb(255, 255, 255);
  border-radius: 12px;
  padding: 10px 12px;
  outline: none;
  min-width: 150px;
}

.main {
  margin-top: 16px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 12px;
}

.card {
  grid-column: span 6;
  padding: 14px 14px;
  border-radius: 16px;
  border: 1px solid var(--border);
  background: var(--panel);
}

@media (max-width: 900px) {
  .card {
    grid-column: span 12;
  }
  .header {
    flex-direction: column;
    align-items: stretch;
  }
}

.cardTop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.pill {
  font-size: 14px;
  padding: 6px 10px 0 0;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 1);
  background: rgba(255, 255, 255, 1);
}

.sev {
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.06);
}

.sev[data-sev="high"] {
  border: 1px solid rgba(232, 121, 92, 1);
  background: rgba(232, 121, 92, 0.2);
}
.sev[data-sev="medium"] {
  border: 1px solid rgba(239, 206, 114, 1);
  background: rgba(239, 206, 114, 0.2);
}
.sev[data-sev="low"] {
  border: 1px solid rgba(90, 183, 132, 1);
  background: rgba(90, 183, 132, 0.2);
}

.cardTitle {
  margin: 10px 0 8px;
  font-size: 18px;
  letter-spacing: 0.2px;
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--muted);
  font-size: 12px;
}

.dot {
  opacity: 0.5;
}

.muted {
  opacity: 0.9;
}
</style>

