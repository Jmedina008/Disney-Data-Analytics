'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import WaitTimePrediction from '@/app/components/visualizations/WaitTimePrediction';
import { api, WaitTimeData, ParkMetrics } from '@/app/lib/api';

const ATTRACTIONS = [
  'Space Mountain',
  'Big Thunder Mountain',
  'Pirates of the Caribbean',
  'Haunted Mansion',
  'Splash Mountain'
];

export default function ThemeParkOptimization() {
  const [selectedAttraction, setSelectedAttraction] = useState(ATTRACTIONS[0]);
  const [waitTimeData, setWaitTimeData] = useState<WaitTimeData[] | null>(null);
  const [metrics, setMetrics] = useState<ParkMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [waitTimes, parkMetrics] = await Promise.all([
          api.getWaitTimes(selectedAttraction),
          api.getParkMetrics()
        ]);
        setWaitTimeData(waitTimes);
        setMetrics(parkMetrics);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [selectedAttraction]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-xl text-disney-gray">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-xl text-red-500">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"
      >
        <div className="text-center">
          <h1 className="font-display text-4xl font-bold text-disney-blue sm:text-5xl">
            Theme Park Optimization
          </h1>
          <p className="mt-4 text-xl text-disney-gray">
            Data-driven insights for enhancing park operations and guest experience
          </p>
        </div>

        <div className="mt-12 grid gap-8 lg:grid-cols-2">
          {/* Attraction Selector */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="lg:col-span-2"
          >
            <div className="flex justify-center space-x-4">
              {ATTRACTIONS.map((attraction) => (
                <button
                  key={attraction}
                  onClick={() => setSelectedAttraction(attraction)}
                  className={`rounded-md px-4 py-2 text-sm font-medium transition-colors ${
                    selectedAttraction === attraction
                      ? 'bg-disney-blue text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {attraction}
                </button>
              ))}
            </div>
          </motion.div>

          {/* Wait Time Predictions */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="lg:col-span-2"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Wait Time Predictions
            </h2>
            <div className="mt-4">
              {waitTimeData && (
                <WaitTimePrediction
                  data={waitTimeData}
                  attractionName={selectedAttraction}
                />
              )}
            </div>
          </motion.div>

          {/* Key Metrics */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="rounded-lg bg-white p-6 shadow-lg"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Model Performance
            </h2>
            <div className="mt-4 grid gap-4">
              <div className="rounded-md bg-disney-blue/5 p-4">
                <h3 className="font-semibold text-disney-blue">
                  Prediction Accuracy (R²)
                </h3>
                <p className="mt-1 text-3xl font-bold">
                  {(metrics?.r2 ?? 0 * 100).toFixed(1)}%
                </p>
              </div>
              <div className="rounded-md bg-disney-yellow/5 p-4">
                <h3 className="font-semibold text-disney-yellow">
                  Average Error (RMSE)
                </h3>
                <p className="mt-1 text-3xl font-bold">
                  {metrics?.rmse.toFixed(1)} min
                </p>
              </div>
            </div>
          </motion.div>

          {/* Weather Impact */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="rounded-lg bg-white p-6 shadow-lg"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Weather Impact
            </h2>
            <div className="mt-4 space-y-4">
              <div className="flex items-center justify-between">
                <span>Rain</span>
                <span className="text-red-500">-25% attendance</span>
              </div>
              <div className="flex items-center justify-between">
                <span>High Temperature</span>
                <span className="text-orange-500">-15% outdoor rides</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Perfect Weather</span>
                <span className="text-green-500">+20% attendance</span>
              </div>
            </div>
          </motion.div>

          {/* Methodology */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="lg:col-span-2"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Methodology
            </h2>
            <div className="mt-4 rounded-lg bg-white p-6 shadow-lg">
              <div className="prose max-w-none">
                <p>
                  Our theme park optimization analysis combines multiple data sources
                  to predict wait times and optimize park operations:
                </p>
                <ul>
                  <li>Historical wait time data</li>
                  <li>Weather data and forecasts</li>
                  <li>Special event schedules</li>
                  <li>Crowd flow patterns</li>
                </ul>
                <p>
                  Machine learning models are trained on this data to predict wait
                  times and suggest optimal staffing levels. The system continuously
                  learns from new data to improve its predictions.
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
} 