import { issuesToString, riskBadgeClass } from "../lib/dashboardUtils";

export default function AIInsightCard({ insight, loading, error }) {
  if (!loading && !insight && !error) {
    return null;
  }

  return (
    <section className="ai-insight" aria-labelledby="ai-insight-title">
      <div className="ai-insight__glow" aria-hidden="true" />
      <header className="ai-insight__header">
        <div className="ai-insight__icon" aria-hidden="true">
          AI
        </div>
        <div>
          <h2 id="ai-insight-title" className="ai-insight__title">
            AI health insight
          </h2>
          <p className="ai-insight__subtitle">
            Analysis from your latest prediction and medical knowledge base
          </p>
        </div>
      </header>

      {loading && (
        <div className="ai-insight__loading" role="status">
          <span className="health-input__spinner" aria-hidden="true" />
          Generating AI explanation…
        </div>
      )}

      {error && !loading && (
        <div className="ai-insight__alert ai-insight__alert--error" role="alert">
          {error}
        </div>
      )}

      {insight && !loading && (
        <div className="ai-insight__body">
          <div className="ai-insight__risk-row">
            <span className={riskBadgeClass(insight.riskLevel)}>
              {insight.riskLevel ?? "—"}
            </span>
            <span className="ai-insight__score">
              Risk score: <strong>{insight.riskScore ?? "—"}</strong>
            </span>
          </div>

          <article className="ai-insight__block">
            <h3 className="ai-insight__block-title">Health analysis</h3>
            <p className="ai-insight__text">{insight.analysis || "—"}</p>
          </article>

          <article className="ai-insight__block">
            <h3 className="ai-insight__block-title">Detected issues</h3>
            <p className="ai-insight__text ai-insight__text--issues">
              {issuesToString(insight.issues)}
            </p>
          </article>

          {insight.riskExplanation && (
            <article className="ai-insight__block">
              <h3 className="ai-insight__block-title">Risk explanation</h3>
              <p className="ai-insight__text">{insight.riskExplanation}</p>
            </article>
          )}

          {insight.actions?.length > 0 && (
            <article className="ai-insight__block ai-insight__block--actions">
              <h3 className="ai-insight__block-title">Recommended actions</h3>
              <ul className="ai-insight__actions">
                {insight.actions.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            </article>
          )}
        </div>
      )}
    </section>
  );
}
