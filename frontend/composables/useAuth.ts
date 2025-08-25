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
  const token = useCookie<string | null>("token", { path: "/" })
  const userCookie = useCookie<User | null>("user", { path: "/" })

  const checkAuth = async () => {
    if (!token.value) {
      isAuthenticated.value = false
      user.value = null
      return false
    }
    try {
      const config = useRuntimeConfig()
      const data = await $fetch<User>(`${config.public.apiBase}/users/me`)
      isAuthenticated.value = true
      user.value = data
      userCookie.value = data // refresh persisted user
      return true
    } catch (err) {
      token.value = null
      isAuthenticated.value = false
      user.value = null
      userCookie.value = null
      return false
    }
  }

  const login = (userData: User, jwt: string) => {
    token.value = jwt
    isAuthenticated.value = true
    user.value = userData
    userCookie.value = userData
  }

  const logout = async () => {
    isAuthenticated.value = false
    user.value = null
    token.value = null
    userCookie.value = null
    useCookie("cash").value = null
    await navigateTo("/login", { replace: true })
  }

  return { isAuthenticated, user, checkAuth, login, logout }
}
