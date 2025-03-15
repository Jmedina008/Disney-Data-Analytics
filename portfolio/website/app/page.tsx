'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { MovieAnalytics } from './components/visualizations/MovieAnalytics'
import { BoxOfficeChart } from './components/visualizations/BoxOfficeChart'
import { WaitTimePrediction } from './components/visualizations/WaitTimePrediction'

export default function Home() {
  const fadeIn = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  }

  const features = [
    {
      title: 'Movie Analytics',
      description: 'Deep dive into Disney movie performance, genres, and trends',
      icon: '🎬',
      href: '/projects/movies'
    },
    {
      title: 'Theme Park Insights',
      description: 'Real-time wait times and crowd prediction analytics',
      icon: '🎡',
      href: '/projects/theme-parks'
    },
    {
      title: 'Streaming Trends',
      description: 'Disney+ content analysis and viewer engagement metrics',
      icon: '📺',
      href: '/projects/streaming'
    }
  ]

  return (
    <div className="space-y-24 pb-16">
      {/* Hero Section */}
      <section className="relative pt-32">
        <motion.div
          initial="initial"
          animate="animate"
          variants={fadeIn}
          className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8"
        >
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
              Disney Data Analytics
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
              Exploring the magic of Disney through data science, from box office performance to theme park operations.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/projects"
                className="rounded-md bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600"
              >
                View Projects
              </Link>
              <Link
                href="/about"
                className="text-sm font-semibold leading-6 text-gray-900 dark:text-gray-100"
              >
                Learn more <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="initial"
          animate="animate"
          variants={fadeIn}
          className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3"
        >
          {features.map((feature) => (
            <Link key={feature.title} href={feature.href}>
              <div className="group relative rounded-xl border border-gray-200 p-6 dark:border-gray-800">
                <div className="text-4xl">{feature.icon}</div>
                <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">{feature.title}</h3>
                <p className="mt-2 text-gray-600 dark:text-gray-400">{feature.description}</p>
              </div>
            </Link>
          ))}
        </motion.div>
      </section>

      {/* Visualization Previews */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <motion.div
          initial="initial"
          animate="animate"
          variants={fadeIn}
          className="space-y-12"
        >
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Interactive Visualizations
            </h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
              Explore our data through beautiful, interactive charts and graphs
            </p>
          </div>

          <div className="grid gap-8 lg:grid-cols-2">
            <div className="rounded-xl border border-gray-200 p-6 dark:border-gray-800">
              <h3 className="mb-4 text-xl font-semibold text-gray-900 dark:text-white">Box Office Performance</h3>
              <BoxOfficeChart />
            </div>
            <div className="rounded-xl border border-gray-200 p-6 dark:border-gray-800">
              <h3 className="mb-4 text-xl font-semibold text-gray-900 dark:text-white">Wait Time Predictions</h3>
              <WaitTimePrediction />
            </div>
          </div>

          <div className="rounded-xl border border-gray-200 p-6 dark:border-gray-800">
            <h3 className="mb-4 text-xl font-semibold text-gray-900 dark:text-white">Movie Analytics Overview</h3>
            <MovieAnalytics />
          </div>
        </motion.div>
      </section>
    </div>
  )
} 