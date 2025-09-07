// composables/useAuth.ts
import { ref, computed } from 'vue'
import { useRouter, useCookie } from '#app'

const user = ref<any | null>(null)
const token = ref<string | null>(null)
const isInitialized = ref(false)

export function useAuth() {
  const router = useRouter()

  function init() {
    if (isInitialized.value) return

    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<string | null>('user')

    if (tokenCookie.value) {
      token.value = tokenCookie.value
    }

    if (userCookie.value) {
//       try {
//         console.log(userCookie.value)
//         console.log('[login] typeof userCookie.value =', typeof userCookie.value)
// console.log('[login] raw userCookie.value =', String(userCookie.value))
//         const lightUser = JSON.parse(userCookie.value)
//         const avatar_url = localStorage.getItem('avatar_url') || null

//         user.value = { ...lightUser, avatar_url }
//       } catch (e) {
//         console.error('[init] failed to parse user cookie:', e)
//         user.value = null
//       }


    // already an object (Nuxt auto-parsed)
  try{
    const lightUser = userCookie.value


  let avatar_url = null
  if (import.meta.client) {
    avatar_url = localStorage.getItem('avatar_url')
  }

  user.value = { ...lightUser, avatar_url }
} catch (e) {
  console.error('[init] failed to parse user cookie:', e)
  user.value = null
}

    }

    isInitialized.value = true
  }

  function login(userData: any, authToken: string) {
    const isProd = process.env.NODE_ENV === 'production'

    const tokenCookie = useCookie<string>('token', {
      sameSite: 'lax',
      secure: isProd,
      path: '/',
    })
    const userCookie = useCookie<any>('user', {
      sameSite: 'lax',
      secure: isProd,
      path: '/',
    })

    const { avatar_url, ...lightUser } = userData
    if (import.meta.client && avatar_url) {
      localStorage.setItem('avatar_url', avatar_url)
    }

    token.value = authToken
    user.value = { ...lightUser, avatar_url }   // ✅ keep avatar in memory too

    tokenCookie.value = authToken
    userCookie.value = JSON.stringify(lightUser)
    console.log('[setting login] typeof userCookie.value =', typeof userCookie.value)
console.log('[setting login] raw userCookie.value =', String(userCookie.value))
    console.log('[login] token =', authToken)
    console.log('[login] userData =', userData)
    console.log('[login] userCookie.value =', userCookie.value)
  }

  function logout() {
    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<string | null>('user')

    token.value = null
    user.value = null

    tokenCookie.value = null
    userCookie.value = null
    if (import.meta.client) {
  localStorage.removeItem('avatar_url')
}
   

    router.push('/login')
  }

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
