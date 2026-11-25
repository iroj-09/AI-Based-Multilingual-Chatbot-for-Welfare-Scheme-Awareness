import { useState } from "react";
import { Link } from "react-router-dom";

import Navbar from "../components/layout/Navbar";
import { checkEligibility } from "../services/api";

const inputClass =
  "w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-teal-600 focus:outline-none";

export default function Eligibility() {
  const [form, setForm] = useState({
    age: "",
    gender: "Female",
    occupation: "",
    income: "",
  });
  const [schemes, setSchemes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSchemes(null);

    try {
      const data = await checkEligibility({
        age: Number(form.age),
        gender: form.gender,
        occupation: form.occupation.trim(),
        income: Number(form.income),
      });
      setSchemes(data.recommended_schemes);
    } catch {
      setError("Something went wrong. Please check your details and try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-slate-50 py-10">
        <div className="mx-auto max-w-xl rounded-2xl bg-white p-8 shadow-lg">
          <h1 className="mb-6 text-2xl font-bold text-teal-700">
            Check Your Eligibility
          </h1>

          <form onSubmit={handleSubmit} className="space-y-4">
            <label className="block">
              <span className="mb-1 block text-sm font-medium">Age</span>
              <input
                type="number"
                min="0"
                max="120"
                required
                className={inputClass}
                value={form.age}
                onChange={(e) => update("age", e.target.value)}
              />
            </label>

            <label className="block">
              <span className="mb-1 block text-sm font-medium">Gender</span>
              <select
                className={inputClass}
                value={form.gender}
                onChange={(e) => update("gender", e.target.value)}
              >
                <option>Female</option>
                <option>Male</option>
                <option>Other</option>
              </select>
            </label>

            <label className="block">
              <span className="mb-1 block text-sm font-medium">Occupation</span>
              <input
                type="text"
                required
                placeholder="e.g. Farmer, Student"
                className={inputClass}
                value={form.occupation}
                onChange={(e) => update("occupation", e.target.value)}
              />
            </label>

            <label className="block">
              <span className="mb-1 block text-sm font-medium">
                Annual income (₹)
              </span>
              <input
                type="number"
                min="0"
                required
                className={inputClass}
                value={form.income}
                onChange={(e) => update("income", e.target.value)}
              />
            </label>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-teal-700 py-2 font-semibold text-white hover:bg-teal-800 disabled:opacity-60"
            >
              {loading ? "Checking..." : "Find Schemes"}
            </button>
          </form>

          {error && <p className="mt-4 text-red-600">{error}</p>}

          {schemes && (
            <div className="mt-6">
              {schemes.length === 0 ? (
                <p>
                  No matching schemes found.{" "}
                  <Link to="/chat" className="font-semibold text-teal-700 hover:underline">
                    Try asking the chatbot.
                  </Link>
                </p>
              ) : (
                <>
                  <h2 className="mb-2 font-semibold">You may be eligible for:</h2>
                  <ul className="space-y-3">
                    {schemes.map((s) => (
                      <li key={s.name} className="rounded-lg border p-3">
                        <p className="font-medium">{s.name}</p>
                        <p className="text-sm text-slate-600">{s.reason}</p>
                        <Link
                          to={`/chat?q=${encodeURIComponent(s.ask)}`}
                          className="mt-1 inline-block text-sm font-semibold text-teal-700 hover:underline"
                        >
                          Ask the chatbot about this →
                        </Link>
                      </li>
                    ))}
                  </ul>
                </>
              )}
              <p className="mt-3 text-sm text-slate-500">
                This is only a suggestion. Verify details on the official scheme
                page or ask the chatbot.
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
