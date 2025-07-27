// // composables/useAuth.ts
// export const useAuth = () => {
//   const user = useState('user') // SSR-safe
//   const token = import.meta.client ? localStorage.getItem('token') : null

//   const isAuthenticated = computed(() => {
//     return !!token || !!user.value
//   })

//   return {
//     isAuthenticated,
//     user,
//     token,
//   }
// }
