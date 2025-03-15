import Link from 'next/link'

export const Footer = () => {
  const currentYear = new Date().getFullYear()

  const footerSections = [
    {
      title: 'Projects',
      links: [
        { href: '/projects/movies', label: 'Movie Analysis' },
        { href: '/projects/theme-parks', label: 'Theme Parks' },
        { href: '/projects/streaming', label: 'Streaming Analytics' },
      ],
    },
    {
      title: 'Resources',
      links: [
        { href: '/docs/api', label: 'API Documentation' },
        { href: '/docs/methodology', label: 'Methodology' },
        { href: '/docs/data-sources', label: 'Data Sources' },
      ],
    },
    {
      title: 'About',
      links: [
        { href: '/about', label: 'About Project' },
        { href: 'https://github.com/Jmedina008/Disney-Data-Analytics', label: 'GitHub' },
        { href: '/contact', label: 'Contact' },
      ],
    },
  ]

  return (
    <footer className="bg-white pb-6 pt-16 dark:bg-gray-900">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {footerSections.map((section) => (
            <div key={section.title}>
              <h3 className="text-sm font-semibold uppercase tracking-wider text-gray-400 dark:text-gray-300">
                {section.title}
              </h3>
              <ul className="mt-4 space-y-4">
                {section.links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="text-base text-gray-600 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-12 border-t border-gray-200 pt-8 dark:border-gray-800">
          <p className="text-center text-base text-gray-400 dark:text-gray-500">
            © {currentYear} Disney Data Analytics. Built with Next.js and D3.js
          </p>
        </div>
      </div>
    </footer>
  )
} 