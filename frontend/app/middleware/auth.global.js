// middleware/auth.global.js
export default defineNuxtRouteMiddleware((to) => {
  const token = useCookie('access_token')

  
  const publicRoutes = ['/auth/login', '/auth/signup']

  
  const isPublicRoute = publicRoutes.includes(to.path)

  
  if (!token.value && !isPublicRoute) {
    return navigateTo('/auth/login')
  }

  
  if (token.value && isPublicRoute) {
    return navigateTo('/')
  }
})