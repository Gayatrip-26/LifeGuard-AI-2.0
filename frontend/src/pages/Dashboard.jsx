import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import AIInsightCard from "../components/AIInsightCard";
import HealthInputCard from "../components/HealthInputCard";
import {
  AI_ENABLED,
  apiFetch,
  apiJson,
  jsonAuthHeaders,
  networkErrorMessage,
} from "../lib/api";
import { authHeaders, clearToken } from "../lib/auth";
import {
  isRowCritical,
  issuesToString,
  recommendedActionsFromIssues,
  riskBadgeClass,
  riskTextClass,
} from "../lib/dashboardUtils";
import "./Dashboard.css";

const LOG = "[LifeGuard Dashboard]";

function formatDateTime(iso) {
  if (!iso) return "—";
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return String(iso);
  }
}

function formatChartTime(iso) {
  if (!iso) return "";
  try {
    return new Date(iso).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } catch {
    return "";
  }
}

function trendArrow(trend) {
  const t = String(trend || "").toLowerCase();
  if (t === "increasing") return "↑";
  if (t === "decreasing") return "↓";
  return "→";
}

function trendLabel(trend) {
  const t = String(trend || "").toLowerCase();
  if (t === "increasing") return "Risk increasing";
  if (t === "decreasing") return "Risk decreasing";
  return "Risk stable";
}

const PREDICTION_POLL_MS = 1000;
const PREDICTION_POLL_MAX = 30;

function sortPredictions(rows) {
  return [...rows].sort(
    (a, b) => new Date(b.created_at) - new Date(a.created_at)
  );
}

export default function Dashboard() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [aiActions, setAiActions] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitSuccess, setSubmitSuccess] = useState(null);
  const [postSubmitBusy, setPostSubmitBusy] = useState(false);
  const [aiInsight, setAiInsight] = useState(null);
  const [aiInsightLoading, setAiInsightLoading] = useState(false);
  const [aiInsightError, setAiInsightError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await apiFetch("/users/me", { headers: authHeaders() }, {
          label: "profile",
        });
        if (res.status === 401) {
          clearToken();
          navigate("/login", { replace: true });
          return;
        }
        if (res.ok) {
          const data = await res.json();
          if (!cancelled) setProfile(data);
        }
      } catch (err) {
        console.error(`${LOG} profile load failed`, err);
        if (!cancelled) setProfile(null);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [navigate]);

  const fetchAiInsightForRow = useCallback(async (row) => {
    if (!AI_ENABLED || !row) {
      return null;
    }
    const q = `Analyze health risks for issues: ${issuesToString(row.issues)}. Risk level ${row.risk_level}, score ${row.risk_score}. Explain concerns and next steps.`;
    console.log(`${LOG} → AI insight query`, { issues: row.issues });
    const body = await apiJson(
      "/ai/query",
      {
        method: "POST",
        headers: jsonAuthHeaders(),
        body: JSON.stringify({ query: q }),
      },
      { label: "ai-insight" }
    );
    console.log(`${LOG} ← AI insight response`, body);
    const actions = Array.isArray(body.recommended_actions)
      ? body.recommended_actions
      : [];
    if (actions.length) {
      setAiActions(actions);
    }
    return {
      analysis: body.answer || "No analysis available.",
      issues: row.issues,
      riskLevel: row.risk_level,
      riskScore: row.risk_score,
      riskExplanation: row.ai_explanation || "",
      actions,
    };
  }, []);

  const load = useCallback(async () => {
    try {
      setError(null);
      const headers = authHeaders();
      console.log(`${LOG} → dashboard refresh`);

      const [sumRes, predRes, alertRes] = await Promise.all([
        apiFetch("/dashboard/summary", { headers }, { label: "summary" }),
        apiFetch("/prediction?limit=100", { headers }, { label: "predictions" }),
        apiFetch("/alert?limit=20", { headers }, { label: "alerts" }),
      ]);

      if (sumRes.status === 401 || predRes.status === 401 || alertRes.status === 401) {
        clearToken();
        navigate("/login", { replace: true });
        return null;
      }
      if (!sumRes.ok) {
        throw new Error(`Summary request failed (${sumRes.status})`);
      }
      if (!predRes.ok) {
        throw new Error(`Predictions request failed (${predRes.status})`);
      }

      const sumData = await sumRes.json();
      const predData = await predRes.json();
      const predList = Array.isArray(predData) ? predData : [];
      setSummary(sumData ?? null);
      setPredictions(predList);

      let alertList = [];
      if (alertRes.ok) {
        const alertData = await alertRes.json();
        alertList = Array.isArray(alertData) ? alertData : [];
        setAlerts(alertList);
      } else {
        setAlerts([]);
      }

      console.log(`${LOG} ← dashboard refresh`, {
        totalRecords: sumData?.total_records,
        predictions: predList.length,
        alerts: alertList.length,
      });

      return { summary: sumData, predictions: predList, alerts: alertList };
    } catch (e) {
      const message = networkErrorMessage(e, "Dashboard load");
      console.error(`${LOG} dashboard refresh failed`, e);
      setError(message);
      return null;
    } finally {
      setLoading(false);
    }
  }, [navigate]);

  const handleHealthSubmitSuccess = useCallback(
    async () => {
      console.log(`${LOG} ingestion succeeded — polling for prediction`);
      setSubmitSuccess("Health data submitted successfully");
      setPostSubmitBusy(true);
      setAiInsight(null);
      setAiInsightError(null);
      setAiInsightLoading(true);

      const baselineIds = new Set(predictions.map((p) => p.id));
      const baselineCount = predictions.length;
      const submittedAt = Date.now();

      let latestPrediction = null;
      await load();

      for (let attempt = 0; attempt < PREDICTION_POLL_MAX; attempt += 1) {
        if (attempt > 0) {
          await new Promise((resolve) => setTimeout(resolve, PREDICTION_POLL_MS));
        }
        const data = await load();
        if (!data) continue;

        const sorted = sortPredictions(data.predictions ?? []);
        const candidate = sorted[0];
        if (!candidate) {
          console.log(`${LOG} prediction poll ${attempt + 1}: no rows yet`);
          continue;
        }

        const isNewId = candidate.id != null && !baselineIds.has(candidate.id);
        const isNewCount = (data.predictions?.length ?? 0) > baselineCount;
        const isRecent =
          candidate.created_at &&
          new Date(candidate.created_at).getTime() >= submittedAt - 5000;

        console.log(`${LOG} prediction poll ${attempt + 1}`, {
          id: candidate.id,
          isNewId,
          isNewCount,
          isRecent,
        });

        if (isNewId || isNewCount || isRecent) {
          latestPrediction = candidate;
          break;
        }
      }

      if (!latestPrediction) {
        const data = await load();
        latestPrediction = data
          ? sortPredictions(data.predictions ?? [])[0] ?? null
          : null;
      }

      if (latestPrediction) {
        console.log(`${LOG} prediction ready`, latestPrediction);
        try {
          const insight = await fetchAiInsightForRow(latestPrediction);
          setAiInsight(insight);
        } catch (e) {
          console.error(`${LOG} AI insight failed`, e);
          setAiInsightError(
            networkErrorMessage(e, "AI insight")
          );
        }
      } else {
        setAiInsightError(
          "Prediction is still processing via Kafka. The dashboard will keep refreshing every 5s."
        );
      }

      setAiInsightLoading(false);
      setPostSubmitBusy(false);
      console.log(`${LOG} post-submit refresh complete`);
    },
    [fetchAiInsightForRow, load, predictions]
  );

  useEffect(() => {
    if (!submitSuccess) return undefined;
    const id = setTimeout(() => setSubmitSuccess(null), 8000);
    return () => clearTimeout(id);
  }, [submitSuccess]);

  useEffect(() => {
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, [load]);

  const sortedPred = useMemo(() => sortPredictions(predictions), [predictions]);

  const latestRow = sortedPred[0] ?? null;

  useEffect(() => {
    if (!AI_ENABLED || !latestRow?.issues?.length) {
      setAiActions([]);
      return;
    }
    const q = `Summarize risks and actions for: ${issuesToString(latestRow.issues)}`;
    let cancelled = false;
    (async () => {
      try {
        const body = await apiJson(
          "/ai/query",
          {
            method: "POST",
            headers: jsonAuthHeaders(),
            body: JSON.stringify({ query: q }),
          },
          { label: "ai-recommendations" }
        );
        if (!cancelled && Array.isArray(body.recommended_actions)) {
          setAiActions(body.recommended_actions);
        }
      } catch (err) {
        console.warn(`${LOG} AI recommendations fetch failed`, err);
        if (!cancelled) setAiActions([]);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [latestRow?.id, latestRow?.issues, AI_ENABLED]);

  const chartData = useMemo(() => {
    return [...predictions]
      .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
      .map((p) => ({
        time: formatChartTime(p.created_at),
        risk_score: p.risk_score,
        created_at: p.created_at,
      }));
  }, [predictions]);

  const tableRows = sortedPred;

  const latestRisk = summary?.latest_risk ?? null;
  const riskTrend = summary?.risk_trend ?? null;
  const showAlertBanner = isRowCritical(latestRow) || alerts.length > 0;
  const displayPatientId = latestRow?.patient_id ?? (profile ? `user_${profile.id}` : "—");

  const displayRecommendations =
    aiInsight?.actions?.length > 0
      ? aiInsight.actions
      : aiActions.length > 0
        ? aiActions
        : recommendedActionsFromIssues(latestRow?.issues);

  return (
    <div className="dashboard">
      <h1 className="dashboard__title">Patient health dashboard</h1>
      <p className="dashboard__subtitle">
        {profile ? (
          <>
            Signed in as <strong>{profile.email}</strong> · patient{" "}
            <strong>{displayPatientId}</strong> · refreshes every 5s
          </>
        ) : (
          <>Loading profile… · refreshes every 5s</>
        )}
      </p>

      {showAlertBanner && (
        <div className="dashboard__banner dashboard__banner--alert" role="alert">
          <strong>Alert:</strong> Critical health risk detected ({displayPatientId}).
          Latest level {latestRow?.risk_level ?? "—"} (score{" "}
          {latestRow?.risk_score ?? "—"}). Recent alerts logged: {alerts.length}.
        </div>
      )}

      {error && (
        <div className="dashboard__banner dashboard__banner--error" role="alert">
          {error}
        </div>
      )}
      {loading && !summary && !error && (
        <div className="dashboard__banner dashboard__banner--loading">
          Loading…
        </div>
      )}

      {submitSuccess && (
        <div
          className="dashboard__banner dashboard__banner--success"
          role="status"
        >
          {submitSuccess}
        </div>
      )}

      {postSubmitBusy && (
        <div className="dashboard__banner dashboard__banner--loading" role="status">
          Processing prediction and refreshing dashboard…
        </div>
      )}

      <HealthInputCard
        profile={profile}
        onSubmitSuccess={handleHealthSubmitSuccess}
        disabled={postSubmitBusy}
      />

      <AIInsightCard
        insight={aiInsight}
        loading={aiInsightLoading}
        error={aiInsightError}
      />

      <div className="dashboard__cards">
        <article className="dashboard__card">
          <p className="dashboard__card-label">Total records</p>
          <p className="dashboard__card-value">
            {summary != null ? summary.total_records : "—"}
          </p>
        </article>
        <article className="dashboard__card">
          <p className="dashboard__card-label">High risk count</p>
          <p className="dashboard__card-value">
            {summary != null ? summary.high_risk_count : "—"}
          </p>
        </article>
        <article className="dashboard__card">
          <p className="dashboard__card-label">Latest risk</p>
          <p
            className={`dashboard__card-value dashboard__card-value--risk ${
              latestRisk ? riskTextClass(latestRisk) : ""
            }`}
          >
            {latestRisk ?? "—"}
          </p>
        </article>
        <article className="dashboard__card">
          <p className="dashboard__card-label">Average score</p>
          <p className="dashboard__card-value">
            {summary != null
              ? Number(summary.average_score).toFixed(2)
              : "—"}
          </p>
        </article>
        <article className="dashboard__card dashboard__card--trend">
          <p className="dashboard__card-label">Risk trend</p>
          <p className="dashboard__card-value dashboard__card-value--trend">
            {riskTrend ? (
              <>
                <span className="dashboard__trend-arrow" title={trendLabel(riskTrend.trend)}>
                  {trendArrow(riskTrend.trend)}
                </span>{" "}
                <span className="dashboard__trend-text">
                  {trendLabel(riskTrend.trend)}
                </span>
              </>
            ) : (
              "—"
            )}
          </p>
          {riskTrend &&
            riskTrend.last_score != null &&
            riskTrend.previous_score != null && (
              <p className="dashboard__trend-meta">
                Last {riskTrend.last_score} · prev {riskTrend.previous_score}
              </p>
            )}
        </article>
      </div>

      {displayRecommendations.length > 0 && (
        <section className="dashboard__section dashboard__section--actions">
          <h2 className="dashboard__section-title">Recommended actions</h2>
          <ul className="dashboard__actions-list">
            {displayRecommendations.map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </section>
      )}

      <section className="dashboard__section">
        <h2 className="dashboard__section-title">Risk score over time</h2>
        <div className="dashboard__chart-wrap">
          {chartData.length === 0 ? (
            <p className="dashboard__subtitle" style={{ margin: 0 }}>
              No prediction history yet.
            </p>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={chartData}
                margin={{ top: 8, right: 16, left: 0, bottom: 8 }}
              >
                <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" />
                <XAxis
                  dataKey="time"
                  tick={{ fontSize: 11, fill: "#64748b" }}
                  stroke="#94a3b8"
                />
                <YAxis
                  dataKey="risk_score"
                  tick={{ fontSize: 11, fill: "#64748b" }}
                  stroke="#94a3b8"
                  domain={["auto", "auto"]}
                />
                <Tooltip
                  labelFormatter={(_label, payload) => {
                    const row = payload?.[0]?.payload;
                    return row?.created_at
                      ? formatDateTime(row.created_at)
                      : "";
                  }}
                  contentStyle={{
                    borderRadius: 8,
                    border: "1px solid #e2e8f0",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="risk_score"
                  stroke="#0ea5e9"
                  strokeWidth={2}
                  dot={{ r: 3, fill: "#0ea5e9" }}
                  activeDot={{ r: 5 }}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </section>

      <section className="dashboard__section">
        <h2 className="dashboard__section-title">Prediction history</h2>
        <div className="dashboard__table-wrap">
          <table className="dashboard__table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Risk level</th>
                <th>Score</th>
                <th>Patient ID</th>
                <th>Issues</th>
                <th>AI explanation</th>
              </tr>
            </thead>
            <tbody>
              {tableRows.length === 0 ? (
                <tr>
                  <td colSpan={6} style={{ color: "#64748b" }}>
                    No rows yet.
                  </td>
                </tr>
              ) : (
                tableRows.map((row) => (
                  <tr
                    key={row.id}
                    className={
                      isRowCritical(row) ? "dashboard__row--critical" : undefined
                    }
                  >
                    <td>{formatDateTime(row.created_at)}</td>
                    <td>
                      <span className={riskBadgeClass(row.risk_level)}>
                        {row.risk_level ?? "—"}
                      </span>
                    </td>
                    <td>{row.risk_score ?? "—"}</td>
                    <td className="dashboard__patient-id">
                      {row.patient_id ?? "—"}
                    </td>
                    <td className="dashboard__issues">
                      {issuesToString(row.issues)}
                    </td>
                    <td className="dashboard__explanation">
                      {row.ai_explanation || "—"}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
