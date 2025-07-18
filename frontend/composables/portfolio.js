import axios from 'axios'
export function usePortfolio() {
  const assets = ref([])
  const cash = ref(0)
  const totalInvested = ref(0)

  const fetchPortfolio = async () => {
    const token = localStorage.getItem("token")
    const response = await axios.get(`http://localhost:8000/api/portfolio/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    const data = response.data
    assets.value = data.assets
    cash.value = data.cash
    totalInvested.value = data.total_investi
  }

  return {
    assets,
    cash,
    totalInvested,
    fetchPortfolio
  }
}

export const formatCurrency = (value, currency = 'USD') => {
  if (typeof value !== 'number') return '--'

  try {
    return new Intl.NumberFormat(
      currency === 'XOF' || currency === 'CFA' ? 'fr-FR' : 'en-US',
      {
        style: 'currency',
        currency,
        currencyDisplay: 'symbol', // key line!
        minimumFractionDigits: 0,
        maximumFractionDigits: 2,
      }
    ).format(value)
  } catch (error) {
    return `${currency} ${value.toLocaleString()}`
  }
}