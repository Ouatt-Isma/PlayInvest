interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  avatar_url?: string
  currency?: string
  // extend as needed
}

export const useAuth = () => {
  const isAuthenticated = useState("isAuthenticated", () => false)
  const user = useState<User | null>("user", () => null)
  const token = useCookie<string | null>("token")

  const checkAuth = async () => {
    if (!token.value) {
      isAuthenticated.value = false
      user.value = null
      return false
    }
    try {
      const config = useRuntimeConfig()
      const data = await $fetch<User>(`${config.public.apiBase}/users/me`, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      isAuthenticated.value = true
      user.value = data
      return true
    } catch (err) {
      console.error("Auth check failed:", err)
      token.value = null
      isAuthenticated.value = false
      user.value = null
      return false
    }
  }

  return { isAuthenticated, user, checkAuth }
}
