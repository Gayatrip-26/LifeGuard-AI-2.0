import { useState } from "react";
import { ingestHealthData, networkErrorMessage } from "../lib/api";

const FIELDS = [
  {
    name: "heart_rate",
    label: "Heart rate",
    unit: "bpm",
    min: 40,
    max: 200,
    step: 1,
    placeholder: "72",
  },
  {
    name: "temperature",
    label: "Temperature",
    unit: "°C",
    min: 30,
    max: 45,
    step: 0.1,
    placeholder: "36.6",
  },
  {
    name: "stress_level",
    label: "Stress level",
    unit: "1–100",
    min: 1,
    max: 100,
    step: 1,
    placeholder: "30",
  },
  {
    name: "sleep_hours",
    label: "Sleep hours",
    unit: "hrs",
    min: 0,
    max: 24,
    step: 0.5,
    placeholder: "7.5",
  },
];

function validateField(field, raw) {
  const trimmed = String(raw ?? "").trim();
  if (trimmed === "") {
    return `${field.label} is required.`;
  }
  const value = Number(trimmed);
  if (!Number.isFinite(value)) {
    return `${field.label} must be a number.`;
  }
  if (value < field.min || value > field.max) {
    return `${field.label} must be between ${field.min} and ${field.max}.`;
  }
  return null;
}

export default function HealthInputCard({ profile, onSubmitSuccess, disabled }) {
  const [values, setValues] = useState({
    heart_rate: "",
    temperature: "",
    stress_level: "",
    sleep_hours: "",
  });
  const [fieldErrors, setFieldErrors] = useState({});
  const [submitError, setSubmitError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function handleChange(name, next) {
    setValues((prev) => ({ ...prev, [name]: next }));
    setFieldErrors((prev) => {
      if (!prev[name]) return prev;
      const copy = { ...prev };
      delete copy[name];
      return copy;
    });
    setSubmitError(null);
  }

  function validateAll() {
    const errors = {};
    for (const field of FIELDS) {
      const msg = validateField(field, values[field.name]);
      if (msg) errors[field.name] = msg;
    }
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitError(null);
    if (!profile?.id) {
      setSubmitError("Profile not loaded. Please wait or sign in again.");
      return;
    }
    if (!validateAll()) return;

    const payload = {
      patient_id: `user_${profile.id}`,
      user_id: profile.id,
      heart_rate: Number(values.heart_rate),
      temperature: Number(values.temperature),
      stress_level: Number(values.stress_level),
      sleep_hours: Number(values.sleep_hours),
      timestamp: new Date().toISOString(),
    };

    setSubmitting(true);
    try {
      await ingestHealthData(payload);
      setValues({
        heart_rate: "",
        temperature: "",
        stress_level: "",
        sleep_hours: "",
      });
      await onSubmitSuccess?.(payload);
    } catch (err) {
      console.error("[LifeGuard] health form submit failed", err);
      setSubmitError(networkErrorMessage(err, "Health data submission"));
    } finally {
      setSubmitting(false);
    }
  }

  const formDisabled = disabled || submitting || !profile?.id;

  return (
    <section className="health-input" aria-labelledby="health-input-title">
      <div className="health-input__header">
        <div>
          <h2 id="health-input-title" className="health-input__title">
            Health data input
          </h2>
          <p className="health-input__subtitle">
            Submit vitals for real-time risk analysis. Patient ID and timestamp are
            assigned automatically.
          </p>
        </div>
        {profile?.id && (
          <span className="health-input__patient-chip">
            {`user_${profile.id}`}
          </span>
        )}
      </div>

      {submitError && (
        <div className="health-input__alert health-input__alert--error" role="alert">
          {submitError}
        </div>
      )}

      <form className="health-input__form" onSubmit={handleSubmit} noValidate>
        <div className="health-input__grid">
          {FIELDS.map((field) => (
            <label key={field.name} className="health-input__field">
              <span className="health-input__label">
                {field.label}
                <span className="health-input__unit">{field.unit}</span>
              </span>
              <input
                className={`health-input__control${
                  fieldErrors[field.name] ? " health-input__control--invalid" : ""
                }`}
                type="number"
                name={field.name}
                min={field.min}
                max={field.max}
                step={field.step}
                placeholder={field.placeholder}
                value={values[field.name]}
                onChange={(e) => handleChange(field.name, e.target.value)}
                disabled={formDisabled}
                aria-invalid={Boolean(fieldErrors[field.name])}
                aria-describedby={
                  fieldErrors[field.name] ? `${field.name}-error` : undefined
                }
              />
              {fieldErrors[field.name] && (
                <span
                  id={`${field.name}-error`}
                  className="health-input__error"
                  role="alert"
                >
                  {fieldErrors[field.name]}
                </span>
              )}
            </label>
          ))}
        </div>

        <div className="health-input__actions">
          <button
            type="submit"
            className="health-input__submit"
            disabled={formDisabled}
          >
            {submitting ? (
              <>
                <span className="health-input__spinner" aria-hidden="true" />
                Submitting…
              </>
            ) : (
              "Submit health data"
            )}
          </button>
        </div>
      </form>
    </section>
  );
}
