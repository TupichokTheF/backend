<template>
  <div class="tfa-page">
    <div class="tfa-container">
      <div class="tfa-card">
        <h1 class="tfa-title">Двухфакторная аутентификация</h1>
        <p class="tfa-subtitle">Введите код, который был отправлен вам</p>

        <form @submit.prevent="handleSubmit" class="tfa-form">
          <div class="form-group">
            <label for="code">Код подтверждения</label>
            <input
              type="text"
              id="code"
              v-model="code"
              placeholder="Введите код"
              autocomplete="one-time-code"
              required
            />
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <button type="submit" class="tfa-btn" :disabled="loading || !code">
            <span v-if="loading">Проверяем...</span>
            <span v-else>Войти</span>
          </button>
        </form>

        <div class="back-link">
          <router-link to="/login">Вернуться к входу</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TwoFactorAuth',
  data() {
    return {
      username: '',
      code: '',
      errorMessage: '',
      loading: false
    }
  },
  async mounted() {
    this.username = this.$route.query.username || ''
    if (!this.username) {
      this.$router.push('/login')
      return
    }
    await this.sendCode()
  },
  methods: {
    async sendCode() {
      try {
        const response = await fetch('http://localhost:8000/api/auth/make_two_factor_auth', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            username: this.username
          })
        })

        if (!response.ok) {
          const data = await response.json().catch(() => null)
          this.errorMessage = data?.detail || 'Не удалось отправить код'
        }
      } catch (error) {
        console.error('Ошибка отправки кода:', error)
        this.errorMessage = 'Не удалось подключиться к серверу'
      }
    },

    async handleSubmit() {
      if (!this.code) return

      this.loading = true
      this.errorMessage = ''

      try {
        const response = await fetch('http://localhost:8000/api/auth/check_two_factor_auth', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            code: this.code,
            username: this.username
          })
        })

        if (!response.ok) {
          const data = await response.json().catch(() => null)
          this.errorMessage = data?.detail || 'Неверный код'
          return
        }

        const data = await response.json()
        if (data.access_token) {
          localStorage.setItem('access_token', data.access_token)
        }
        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token)
        }

        this.$router.push('/')
      } catch (error) {
        console.error('Ошибка проверки кода:', error)
        this.errorMessage = 'Не удалось подключиться к серверу. Попробуйте снова.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.tfa-page {
  min-height: calc(100vh - 140px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.tfa-container {
  width: 100%;
  max-width: 440px;
}

.tfa-card {
  background: white;
  border-radius: 16px;
  padding: 48px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.tfa-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--ozon-text);
  margin-bottom: 8px;
  text-align: center;
}

.tfa-subtitle {
  color: var(--ozon-text-secondary);
  text-align: center;
  margin-bottom: 32px;
  font-size: 15px;
}

.tfa-form {
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--ozon-text);
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--ozon-border);
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.2s;
  outline: none;
}

.form-group input:focus {
  border-color: var(--ozon-primary);
  box-shadow: 0 0 0 3px rgba(0, 91, 255, 0.1);
}

.error-message {
  background: #fee;
  border: 1px solid #fcc;
  color: #c33;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
  text-align: center;
}

.tfa-btn {
  width: 100%;
  padding: 14px;
  background: var(--ozon-primary);
  color: white;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
}

.tfa-btn:hover:not(:disabled) {
  background: var(--ozon-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 91, 255, 0.3);
}

.tfa-btn:active:not(:disabled) {
  transform: translateY(0);
}

.tfa-btn:disabled {
  background: var(--ozon-text-secondary);
  opacity: 0.6;
  cursor: not-allowed;
}

.back-link {
  text-align: center;
}

.back-link a {
  color: var(--ozon-primary);
  font-size: 14px;
  font-weight: 500;
  transition: opacity 0.2s;
}

.back-link a:hover {
  opacity: 0.8;
}

@media (max-width: 768px) {
  .tfa-card {
    padding: 32px 24px;
  }

  .tfa-title {
    font-size: 24px;
  }
}
</style>
