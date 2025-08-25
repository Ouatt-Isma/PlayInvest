export default defineNuxtPlugin(async () => {
  const { checkAuth } = useAuth()
  await checkAuth() // validate token before rendering
})