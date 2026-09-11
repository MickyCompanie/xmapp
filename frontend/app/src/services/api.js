export const apiFetch = (endpoint, options = {}) => {
  const config = useRuntimeConfig()

  return $fetch(endpoint, {
    baseURL: config.public.apiBase,
    ...options,
    headers: {
      ...options?.headers,
    },
  })
}