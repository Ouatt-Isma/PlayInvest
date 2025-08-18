import axios from 'axios'


export async function invest(assetId, amount, onSuccess = () => {}, onError = () => {}) {
  try {
    const token = localStorage.getItem("token")
    const config = useRuntimeConfig()
   const apiBase = config.public.apiBase 
    const res = await axios.get(`${apiBase}/api/buy`, {
      params: { asset: assetId, amount },
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    onSuccess()
    return res.json()
  } catch (error) {
    const msg = error.response?.data?.detail || "Erreur inattendue lors de l'achat"
    onError(msg)
    throw error
  }
}

export function getLogo(symbol) {
  return `/logos/${symbol}.webp`
}


// export async function sell(assetId, amount, onSuccess = () => {}, onError = () => {}) {
//   try {
//     const token = localStorage.getItem("token")
//     const res = await axios.get(`${apiBase}/api/buy`, {
//       params: { asset: assetId, amount },
//       headers: {
//         Authorization: `Bearer ${token}`
//       }
//     })
//     onSuccess()
//     return res.data
//   } catch (error) {
//     const msg = error.response?.data?.detail || "Erreur inattendue lors de l'achat"
//     onError(msg)
//     throw error
//   }
// }




