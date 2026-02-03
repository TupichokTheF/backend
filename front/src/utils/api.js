const API_BASE = 'http://localhost:8000'

// Попытка обновить access_token
export async function refreshToken() {
  try {
    const response = await fetch(`${API_BASE}/api/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data = await response.json()
      const newToken = data.access_token || data.token
      if (newToken) {
        localStorage.setItem('access_token', newToken)
        return newToken
      }
    }

    // Refresh не удался - выходим
    return null
  } catch (error) {
    console.error('Ошибка обновления токена:', error)
    return null
  }
}

// Выход из аккаунта
export function logout() {
  localStorage.removeItem('access_token')
}

// Обработка 401 ошибки с попыткой refresh
export async function handle401(router) {
  const newToken = await refreshToken()

  if (newToken) {
    return newToken // Токен обновлён успешно
  }

  // Refresh не удался - выходим
  logout()
  if (router) {
    router.push('/')
  }
  return null
}
