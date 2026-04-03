<template>
  <div class="page">
    <header class="header">
      <div>
        <h1 class="title">Alerts</h1>
        <p class="subtitle">Data from API</p>
      </div>
      <div class="filters">
        <label class="label">
          Project
          <select v-model="projectName" class="select">
            <option value="">All</option>
            <option v-for="p in projectsList" :key="p.id" :value="p.name">{{ p.name }}</option>
          </select>
        </label>
        <label class="label">
          Severity
          <select v-model="severityFilter" class="select">
            <option value="">All</option>
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
          </select>
        </label>
      </div>
    </header>

    <main class="main">
      <p v-if="loadError" class="error">{{ loadError }}</p>
      <p v-else-if="loading" class="loading">Loading…</p>
      <div v-else class="content">
        <div class="summary">
          <div class="summaryItem">
            Total alerts: <b>{{ alerts.length }}</b>
          </div>
          <div class="summaryItem">
            Total events: <b>{{ totalEvents }}</b>
          </div>
        </div>
        <div class="grid">
          <article v-for="alert in alerts" :key="alert.id" class="card">
            <div class="cardTop">
              <span class="pill">{{ alert.project_name }}</span>
              <span class="sev" :data-sev="alert.severity">{{ alert.severity }}</span>
            </div>
            <h3 class="cardTitle">{{ alert.title }}</h3>
            <div class="meta">
              <span>events: <b>{{ eventCount(alert) }}</b></span>
              <span class="dot">•</span>
              <span class="muted">{{ alert.created_at }}</span>
            </div>
          </article>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const alerts = ref([]);
const projectsList = ref([]);
const loading = ref(true);
const loadError = ref(null);

const projectName = ref("");
const severityFilter = ref("");

function alertsUrl() {
  const params = new URLSearchParams();
  if (severityFilter.value) {
    params.set("severity", severityFilter.value);
  }
  if (projectName.value) {
    params.set("project_name", projectName.value);
  }
  const qs = params.toString();
  return qs ? `${API_BASE}/alerts?${qs}` : `${API_BASE}/alerts`;
}

async function loadProjects() {
  const response = await fetch(`${API_BASE}/projects`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  projectsList.value = await response.json();
}

async function loadAlerts() {
  loading.value = true;
  try {
    const response = await fetch(alertsUrl());
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    alerts.value = await response.json();
    loadError.value = null;
  } catch (err) {
    loadError.value =
      err instanceof Error ? err.message : "Failed to load alerts";
    alerts.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  try {
    await loadProjects();
  } catch {
    projectsList.value = [];
  }
  await loadAlerts();
});

watch([projectName, severityFilter], () => {
  loadAlerts();
});

/** API uses snake_case events_count; coerce so reduce never sees NaN. */
function eventCount(alert) {
  const raw = alert?.events_count ?? alert?.eventsCount;
  const n = Number(raw);
  return Number.isFinite(n) ? n : 0;
}

const totalEvents = computed(() =>
  alerts.value.reduce((acc, alert) => acc + eventCount(alert), 0)
);
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

.summary {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 14px 0;
}

.summaryItem {
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.08);
  color: var(--text);
  font-size: 13px;
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

.loading,
.error {
  margin: 16px 0;
  font-size: 14px;
}

.error {
  color: #c45c4a;
}
</style>

