export const useAuth = () => {
  const isAuthenticated = useState("isAuthenticated", () => false)
  const token = useCookie("token")  // ✅ SSR + CSR safe

  const checkAuth = async () => {
    if (!token.value) {
      isAuthenticated.value = false
      return false
    }
    try {
      const config = useRuntimeConfig()
      await $fetch(`${config.public.apiBase}/users/me`, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      isAuthenticated.value = true
      return true
    } catch (err) {
      console.error("Auth check failed:", err)
      token.value = null  // clear cookie
      isAuthenticated.value = false
      return false
    }
  }

  return { isAuthenticated, checkAuth }
}
