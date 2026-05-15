export function issuesToString(issues) {
  if (!issues) return "—";
  if (Array.isArray(issues)) return issues.length ? issues.join(", ") : "—";
  return String(issues);
}

export function normalizeRisk(level) {
  return String(level || "")
    .trim()
    .toUpperCase();
}

export function riskBadgeClass(level) {
  const l = normalizeRisk(level);
  if (l === "HIGH") return "risk-badge risk-badge--high";
  if (l === "MEDIUM") return "risk-badge risk-badge--medium";
  return "risk-badge risk-badge--low";
}

export function riskTextClass(level) {
  const l = normalizeRisk(level);
  if (l === "HIGH") return "risk-high";
  if (l === "MEDIUM") return "risk-medium";
  return "risk-low";
}

export function isRowCritical(row) {
  if (!row) return false;
  const lvl = normalizeRisk(row.risk_level);
  const score = Number(row.risk_score);
  return lvl === "HIGH" || score > 100;
}

export function recommendedActionsFromIssues(issues) {
  const blob = (Array.isArray(issues) ? issues.join(" ") : String(issues || "")).toLowerCase();
  const out = [];
  if (blob.includes("dehydration")) {
    out.push("Drink fluids regularly; consider electrolytes if advised");
    out.push("Limit alcohol and excess caffeine until you feel better");
  }
  if (blob.includes("stress")) {
    out.push("Use short relaxation breaks and steady sleep routines");
    out.push("Reach out for mental health support if stress stays high");
  }
  if (blob.includes("fever")) {
    out.push("Monitor temperature on a schedule");
    out.push("Rest, hydrate, and seek care for high or persistent fever");
  }
  if (!out.length) {
    out.push("Track symptoms you have been asked to monitor");
    out.push("Rest and contact your clinician if anything worsens");
  }
  return [...new Set(out)];
}
