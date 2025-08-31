// composables/useAuth.ts
import { ref, computed } from 'vue'
import { useRouter, useCookie } from '#app'

const user = ref<any | null>(null)
const token = ref<string | null>(null)
const isInitialized = ref(false)

export function useAuth() {
  const router = useRouter()

  /**
   * Initialize auth state from cookies
   */
  function init() {
    if (isInitialized.value) return

    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<string | null>('user')

    console.log('[init] raw tokenCookie =', tokenCookie.value)
  console.log('[init] raw userCookie =', userCookie.value)

    if (tokenCookie.value) {
    token.value = tokenCookie.value
    }
    if (userCookie.value) {
      try {
        user.value = JSON.parse(userCookie.value)
      } catch (e) {
        console.error('[init] failed to parse user cookie:', e)
        user.value = null
      }
    }
        isInitialized.value = true
      }

  /**
   * Save user + token after successful login
   */
  function login(userData: string, authToken: string) {
    const tokenCookie = useCookie<string>('token', {
    sameSite: 'lax',
    secure: true,
    path: '/',
  })
    const userCookie = useCookie<string>('user', {
      sameSite: 'lax',
      secure: true,
      path: '/',
    })

    token.value = authToken
    user.value = userData

    tokenCookie.value = authToken
    userCookie.value = JSON.stringify(userData)

    console.log('[login] token =', authToken)
  console.log('[login] userData =', userData)
  console.log('[login] userCookie.value =', userCookie.value)
  }

  /**
   * Logout: clear cookies + state
   */
  function logout() {
    const tokenCookie = useCookie<string| null>('token')
    const userCookie = useCookie<string| null>('user')

    token.value = null
    user.value = null

    tokenCookie.value = null
    userCookie.value = null

    router.push('/login')
  }

  /**
   * Check if user is authenticated
   */
  function checkAuth() {
    if (!isInitialized.value) {
      init()
    }
    return isAuthenticated.value
  }

  const isAuthenticated = computed(() => !!user.value && !!token.value)

  return {
    user,
    token,
    isInitialized,
    init,
    login,
    logout,
    checkAuth,
    isAuthenticated,
  }
}
