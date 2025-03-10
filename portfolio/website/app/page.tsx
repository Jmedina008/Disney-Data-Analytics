import { motion } from 'framer-motion'
import Image from 'next/image'

export default function Home() {
  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <section className="relative h-screen">
        <div className="absolute inset-0">
          <Image
            src="/images/disney-castle.jpg"
            alt="Disney Castle"
            fill
            className="object-cover"
            priority
          />
          <div className="absolute inset-0 bg-black/50" />
        </div>
        <div className="relative flex h-full items-center justify-center text-white">
          <div className="text-center">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="font-display text-5xl font-bold sm:text-6xl md:text-7xl"
            >
              Disney Data Science
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="mt-6 text-xl sm:text-2xl"
            >
              Exploring the Magic Through Data
            </motion.p>
          </div>
        </div>
      </section>

      {/* Projects Overview */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center font-display text-3xl font-bold text-disney-blue sm:text-4xl">
            Featured Projects
          </h2>
          <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {/* Disney+ Content Analysis */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="overflow-hidden rounded-lg bg-white shadow-lg"
            >
              <div className="relative h-48">
                <Image
                  src="/images/disney-plus.jpg"
                  alt="Disney+"
                  fill
                  className="object-cover"
                />
              </div>
              <div className="p-6">
                <h3 className="font-display text-xl font-bold text-disney-gray">
                  Disney+ Content Analysis
                </h3>
                <p className="mt-2 text-disney-gray/80">
                  Analyzing streaming trends and content performance on Disney+
                </p>
              </div>
            </motion.div>

            {/* Theme Park Optimization */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="overflow-hidden rounded-lg bg-white shadow-lg"
            >
              <div className="relative h-48">
                <Image
                  src="/images/theme-park.jpg"
                  alt="Theme Park"
                  fill
                  className="object-cover"
                />
              </div>
              <div className="p-6">
                <h3 className="font-display text-xl font-bold text-disney-gray">
                  Theme Park Optimization
                </h3>
                <p className="mt-2 text-disney-gray/80">
                  Optimizing park operations through data-driven insights
                </p>
              </div>
            </motion.div>

            {/* Entertainment Analytics */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="overflow-hidden rounded-lg bg-white shadow-lg"
            >
              <div className="relative h-48">
                <Image
                  src="/images/entertainment.jpg"
                  alt="Entertainment"
                  fill
                  className="object-cover"
                />
              </div>
              <div className="p-6">
                <h3 className="font-display text-xl font-bold text-disney-gray">
                  Entertainment Analytics
                </h3>
                <p className="mt-2 text-disney-gray/80">
                  Analyzing box office trends and franchise performance
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="bg-disney-gray/5 py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center font-display text-3xl font-bold text-disney-blue sm:text-4xl">
            Technology Stack
          </h2>
          <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {/* Frontend */}
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="font-display text-xl font-bold text-disney-gray">
                Frontend
              </h3>
              <ul className="mt-4 space-y-2 text-disney-gray/80">
                <li>Next.js 13</li>
                <li>TailwindCSS</li>
                <li>Framer Motion</li>
                <li>Chart.js/D3.js</li>
              </ul>
            </div>

            {/* Backend */}
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="font-display text-xl font-bold text-disney-gray">
                Backend
              </h3>
              <ul className="mt-4 space-y-2 text-disney-gray/80">
                <li>FastAPI</li>
                <li>PostgreSQL</li>
                <li>Redis</li>
                <li>Docker</li>
              </ul>
            </div>

            {/* Data Science */}
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="font-display text-xl font-bold text-disney-gray">
                Data Science
              </h3>
              <ul className="mt-4 space-y-2 text-disney-gray/80">
                <li>Python</li>
                <li>Pandas</li>
                <li>NumPy</li>
                <li>Scikit-learn</li>
              </ul>
            </div>

            {/* APIs */}
            <div className="rounded-lg bg-white p-6 shadow-lg">
              <h3 className="font-display text-xl font-bold text-disney-gray">
                APIs
              </h3>
              <ul className="mt-4 space-y-2 text-disney-gray/80">
                <li>TMDB API</li>
                <li>Weather API</li>
                <li>Disney Parks API</li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
} 