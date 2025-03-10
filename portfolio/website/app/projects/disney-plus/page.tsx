'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import StreamingTrendsChart from '@/app/components/visualizations/StreamingTrendsChart';
import { api, StreamingTrends, StreamingMetrics } from '@/app/lib/api';

export default function DisneyPlusAnalysis() {
  const [trendsData, setTrendsData] = useState<StreamingTrends | null>(null);
  const [metrics, setMetrics] = useState<StreamingMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [trendsResponse, metricsResponse] = await Promise.all([
          api.getStreamingTrends(),
          api.getStreamingMetrics()
        ]);
        setTrendsData(trendsResponse);
        setMetrics(metricsResponse);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

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
            Disney+ Content Analysis
          </h1>
          <p className="mt-4 text-xl text-disney-gray">
            Exploring the streaming platform's content library and viewer engagement
          </p>
        </div>

        <div className="mt-12 grid gap-8 lg:grid-cols-2">
          {/* Content Overview */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="rounded-lg bg-white p-6 shadow-lg"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Content Overview
            </h2>
            <div className="mt-4 grid gap-4">
              <div className="rounded-md bg-disney-blue/5 p-4">
                <h3 className="font-semibold text-disney-blue">Total Titles</h3>
                <p className="mt-1 text-3xl font-bold">
                  {metrics?.total_titles.toLocaleString()}
                </p>
              </div>
              <div className="rounded-md bg-disney-yellow/5 p-4">
                <h3 className="font-semibold text-disney-yellow">Average Rating</h3>
                <p className="mt-1 text-3xl font-bold">
                  {metrics?.avg_rating.toFixed(1)}/5
                </p>
              </div>
            </div>
          </motion.div>

          {/* Content Growth */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="rounded-lg bg-white p-6 shadow-lg"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Content Growth
            </h2>
            <div className="mt-4">
              {trendsData && <StreamingTrendsChart data={trendsData} />}
            </div>
          </motion.div>

          {/* Top Genres */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="rounded-lg bg-white p-6 shadow-lg"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Top Genres
            </h2>
            <div className="mt-4 space-y-2">
              {metrics?.top_genres &&
                Object.entries(metrics.top_genres).map(([genre, count]) => (
                  <div
                    key={genre}
                    className="flex items-center justify-between rounded-md bg-disney-blue/5 p-2"
                  >
                    <span className="font-medium">{genre}</span>
                    <span className="text-disney-blue">{count}</span>
                  </div>
                ))}
            </div>
          </motion.div>

          {/* Language Distribution */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="rounded-lg bg-white p-6 shadow-lg"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Language Distribution
            </h2>
            <div className="mt-4 space-y-2">
              {metrics?.language_distribution &&
                Object.entries(metrics.language_distribution)
                  .sort(([, a], [, b]) => b - a)
                  .slice(0, 5)
                  .map(([language, count]) => (
                    <div
                      key={language}
                      className="flex items-center justify-between rounded-md bg-disney-yellow/5 p-2"
                    >
                      <span className="font-medium">{language.toUpperCase()}</span>
                      <span className="text-disney-yellow">{count}</span>
                    </div>
                  ))}
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
                  This analysis combines data from multiple sources to provide insights
                  into Disney+'s content library and viewer engagement:
                </p>
                <ul>
                  <li>Content metadata from TMDB API</li>
                  <li>Viewer ratings and reviews</li>
                  <li>Historical content availability data</li>
                  <li>Genre and category distribution</li>
                </ul>
                <p>
                  The data is processed using Python and pandas, with visualizations
                  created using Chart.js and D3.js. Regular updates ensure the analysis
                  reflects the current state of the platform.
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
} 