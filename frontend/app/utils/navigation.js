export const NAV_ITEMS = [
  { label: 'souhaits', icon: '🌟', to: '/wishes/' },
  { label: 'cadeaux', icon: '🎁', to: '/gifts/' },
  { label: 'dépenses', icon: '🏷️', to: '/expenses/' },
  { label: 'Configuration', icon: '⚙️', to: '/settings', condition: (user) => user?.role && user.role !== 'user' }
]

// 📜 📦 🎀 🛒