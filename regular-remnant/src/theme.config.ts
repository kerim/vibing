import { defineThemeConfig } from './types'

export default defineThemeConfig({
  site: 'https://vibing.kerim.one',
  title: 'Vibing With Kerim',
  description: 'Experiments in AI Coding',
  author: 'P. Kerim Friedman',
  navbarItems: [
    { label: 'Blog', href: '/' },
    { label: 'Tags', href: '/tags/' },
    { label: 'About', href: '/about/' }
  ],
  footerItems: [
    {
      icon: 'tabler--brand-github',
      href: 'https://github.com/kerim',
      label: 'Github'
    },
    {
      icon: 'tabler--rss',
      href: '/feed.xml',
      label: 'RSS feed'
    }
  ],

  // optional settings
  locale: 'en',
  mode: 'dark',
  modeToggle: true,
  colorScheme: 'scheme-mono',
  openGraphImage: undefined,
  postsPerPage: 5,
  postsView: 'list',
  scrollProgress: false,
  scrollToTop: true,
  tagIcons: {},
  expressiveCodeThemes: ['vitesse-light', 'vitesse-black']
})
