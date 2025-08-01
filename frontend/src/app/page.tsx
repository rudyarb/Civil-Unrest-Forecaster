'use client';

import { useState } from 'react';

export default function PredictionPage() {
  const [region, setRegion] = useState('');
  const [month, setMonth] = useState('');
  const [result, setResult] = useState<null | {
    region: string;
    month: string;
    prediction: number;
    probability_of_unrest: number;
  }>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const res = await fetch(`https://civil-unrest-forecaster-backend.onrender.com/predict?region=${region}&month=${month}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!res.ok) {
      alert('Something went wrong.');
      return;
    }

    const data = await res.json();
    setResult(data);
  };

  const regionOptions = Array.from({ length: 50 }, (_, i) => `R${i + 1}`);

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      {/* Intro Section */}
      <section className="bg-blue-50 p-4 rounded shadow">
        <h1 className="text-2xl font-bold mb-2">Civil Unrest Forecaster</h1>
        <p className="text-gray-700">
          This tool allows you to view the likelihood of civil unrest in a specific region for a given month.
          Select a region and the month for which you would like to see the forecast from the dropdown menus below, then click <strong>View Forecast</strong>.
        </p>
      </section>

      {/* Form Section */}
      <form onSubmit={handleSubmit} className="space-y-4 bg-white p-4 rounded shadow">
        <div>
          <label className="block mb-1 font-medium">Region:</label>
          <select
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            className="w-full border px-3 py-2 rounded"
            required
          >
            <option value="" disabled>Select a region</option>
            {regionOptions.map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block mb-1 font-medium">Month:</label>
          <select
            value={month}
            onChange={(e) => setMonth(e.target.value)}
            className="w-full border px-3 py-2 rounded"
            required
          >
            <option value="" disabled>Select a month</option>
            <option value="2032-01">January 2032</option>
          </select>
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          View Forecast
        </button>
      </form>

      {/* Result Section */}
      {result && (
        <div className="p-4 border rounded bg-gray-50 shadow space-y-2">
          <h2 className="text-lg font-semibold mb-2">Forecast</h2>
          <p><strong>Region:</strong> {result.region}</p>
          <p><strong>Month:</strong> {result.month}</p>
          <p>
            <strong>Projected Condition:</strong>{' '}
            {result.prediction === 1 ? (
              <span className="text-red-600 font-medium">Unrest</span>
            ) : (
              <span className="text-green-600 font-medium">No Unrest</span>
            )}
          </p>
          <p>
            <strong>Probability of Unrest:</strong>{' '}
            <span className={`font-semibold ${
              result.probability_of_unrest > 0.5 ? 'text-red-600' : 'text-green-600'
            }`}>
              {(result.probability_of_unrest * 100).toFixed(2)}%
            </span>
          </p>
        </div>
      )}
    </div>
  );
}
