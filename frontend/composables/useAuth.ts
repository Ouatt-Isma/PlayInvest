export const useAuth = () => {
    const isAuthenticated = useState("isAuthenticated", () => false)
    const checkAuth = async () => {
    const token = process.client ? localStorage.getItem("token") : null
    if (!token) {
      isAuthenticated.value = false
      return false
    }
    try {
      const config = useRuntimeConfig()
      await $fetch(`${config.public.apiBase}/users/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      isAuthenticated.value = true   // ✅ backend confirms token is valid
      return true
    } catch (err) {
      console.error("Auth check failed:", err)
      localStorage.removeItem("token")
      isAuthenticated.value = false
      return false
    }
  }



  return { isAuthenticated, checkAuth}
}
