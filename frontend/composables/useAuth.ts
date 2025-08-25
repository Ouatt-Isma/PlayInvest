interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  avatar_url?: string
  currency?: string
}

export const useAuth = () => {
  const isAuthenticated = useState("isAuthenticated", () => false)
  const user = useState<User | null>("user", () => null)
  const token = useCookie<string | null>("token")

  /**
   * Runs on app init / refresh → validates the token with backend.
   * Use only when you need to confirm session is still valid.
   */
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

  const login = (userData: User, jwt: string) => {
    token.value = jwt
    isAuthenticated.value = true
    user.value = userData
  }

  const logout = async () => {
    console.log("Logging out…")
    // Clear state
    isAuthenticated.value = false
    user.value = null

    // Clear cookies
    token.value = null
    useCookie("avatar_url").value = null
    useCookie("first_name").value = null
    useCookie("user").value = null
    useCookie("cash").value = null

    // Redirect
    await navigateTo("/login", { replace: true })
  }

  return { isAuthenticated, user, checkAuth, login, logout }
}
