export default defineNuxtPlugin(() => {
  const auth = useAuth()

  addRouteMiddleware('dynamic-layout', (to) => {
    const authPages = ['/login', '/register']
    const isAuthPage = authPages.includes(to.path)

    if (isAuthPage) {
      to.meta.layout = 'auth'
    } else {
      to.meta.layout = auth.isAuthenticated.value ? 'connected' : 'default'
    }
  }, { global: true })
})