// composables/useToast.js
export const useToast = () => {
  const toasts = useState('global_toasts', () => [])

  const show = (message, type = 'success', duration = 4000) => {
    const id = Date.now()
    toasts.value.push({ id, message, type })

    // Suppression automatique après x millisecondes
    setTimeout(() => {
      remove(id)
    }, duration)
  }

  const remove = (id) => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  return {
    toasts,
    show,
    success: (msg, duration) => show(msg, 'success', duration),
    error: (msg, duration) => show(msg, 'error', duration),
    info: (msg, duration) => show(msg, 'info', duration),
    warning: (msg, duration) => show(msg, 'warning', duration),
    remove
  }
}