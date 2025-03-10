'use client';

import { motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import BoxOfficeChart from '@/app/components/visualizations/BoxOfficeChart';
import { api, BoxOfficeData } from '@/app/lib/api';

export default function EntertainmentAnalytics() {
  const [boxOfficeData, setBoxOfficeData] = useState<BoxOfficeData[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await api.getBoxOfficeData();
        setBoxOfficeData(data);
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
            Entertainment Analytics
          </h1>
          <p className="mt-4 text-xl text-disney-gray">
            Analyzing box office performance and franchise success patterns
          </p>
        </div>

        <div className="mt-12 grid gap-8 lg:grid-cols-2">
          {/* Box Office Performance */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="lg:col-span-2"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Box Office Performance
            </h2>
            <div className="mt-4">
              {boxOfficeData && <BoxOfficeChart data={boxOfficeData} />}
            </div>
          </motion.div>

          {/* Franchise Success */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="rounded-lg bg-white p-6 shadow-lg"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Top Franchises
            </h2>
            <div className="mt-4 space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-semibold">Marvel Cinematic Universe</span>
                <span className="text-disney-blue">$22.5B+</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="font-semibold">Star Wars</span>
                <span className="text-disney-blue">$10.3B+</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="font-semibold">Frozen</span>
                <span className="text-disney-blue">$2.7B+</span>
              </div>
            </div>
          </motion.div>

          {/* Release Strategy */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="rounded-lg bg-white p-6 shadow-lg"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Release Strategy
            </h2>
            <div className="mt-4 space-y-4">
              <div className="rounded-md bg-disney-blue/5 p-4">
                <h3 className="font-semibold text-disney-blue">
                  Optimal Release Windows
                </h3>
                <ul className="mt-2 space-y-2">
                  <li>Summer Blockbusters: May-July</li>
                  <li>Holiday Season: Nov-Dec</li>
                  <li>Spring Break: March</li>
                </ul>
              </div>
            </div>
          </motion.div>

          {/* Methodology */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="lg:col-span-2"
          >
            <h2 className="font-display text-2xl font-bold text-disney-gray">
              Methodology
            </h2>
            <div className="mt-4 rounded-lg bg-white p-6 shadow-lg">
              <div className="prose max-w-none">
                <p>
                  Our entertainment analytics combines multiple data sources to
                  analyze box office performance and identify success patterns:
                </p>
                <ul>
                  <li>Box office revenue data</li>
                  <li>Production and marketing budgets</li>
                  <li>Critical reception and audience scores</li>
                  <li>Release timing and competition analysis</li>
                </ul>
                <p>
                  Advanced statistical analysis and machine learning techniques are
                  used to identify patterns and predict potential performance of
                  upcoming releases.
                </p>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
} 