import './globals.css'
import { Inter, Playfair_Display } from 'next/font/google'
import { Metadata } from 'next'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const playfairDisplay = Playfair_Display({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-playfair-display',
})

export const metadata: Metadata = {
  title: 'Disney Data Science Portfolio',
  description: 'A showcase of data science projects focused on Disney entertainment and theme park operations.',
  keywords: ['Disney', 'Data Science', 'Analytics', 'Theme Parks', 'Streaming', 'Entertainment'],
  authors: [{ name: 'Your Name' }],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${playfairDisplay.variable}`}>
      <body className="bg-white">
        <nav className="fixed top-0 z-50 w-full bg-white/80 backdrop-blur-md">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 justify-between">
              <div className="flex">
                <a href="/" className="flex items-center">
                  <span className="font-display text-xl text-disney-blue">Disney Data</span>
                </a>
              </div>
              <div className="flex items-center space-x-4">
                <a href="/projects" className="text-disney-gray hover:text-disney-blue">Projects</a>
                <a href="/about" className="text-disney-gray hover:text-disney-blue">About</a>
                <a href="/contact" className="text-disney-gray hover:text-disney-blue">Contact</a>
              </div>
            </div>
          </div>
        </nav>
        <main className="min-h-screen pt-16">
          {children}
        </main>
        <footer className="bg-disney-gray/5 py-8">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center text-sm text-disney-gray">
              <p>© {new Date().getFullYear()} Disney Data Science Portfolio</p>
              <p className="mt-2">
                Built with Next.js and FastAPI. Data from TMDB, Weather API, and Disney Parks API.
              </p>
            </div>
          </div>
        </footer>
      </body>
    </html>
  )
} 