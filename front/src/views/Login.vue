<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <h1 class="login-title">Вход</h1>
        <p class="login-subtitle">Войдите, чтобы получить доступ ко всем возможностям OZON</p>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="username">Логин</label>
            <input
              type="text"
              id="username"
              v-model="username"
              placeholder="Введите ваш логин"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">Пароль</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="Введите пароль"
              required
            />
          </div>

          <div class="form-options">
            <label class="checkbox-label">
              <input type="checkbox" v-model="rememberMe" />
              <span>Запомнить меня</span>
            </label>
            <a href="#" class="forgot-password">Забыли пароль?</a>
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <button type="submit" class="login-btn" :disabled="loading">
            <span v-if="loading">Вход...</span>
            <span v-else>Войти</span>
          </button>
        </form>

        <div class="register-link">
          Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      loading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.errorMessage = ''

      try {
        const response = await fetch('http://localhost:8000/api/auth/signin', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        })

        if (!response.ok) {
          const errorData = await response.json()
          this.errorMessage = errorData.detail || 'Неверный логин или пароль'
          return
        }

        this.$router.push(`/two-factor-auth?username=${encodeURIComponent(this.username)}`)

      } catch (error) {
        console.error('Ошибка авторизации:', error)
        this.errorMessage = 'Не удалось подключиться к серверу. Проверьте соединение.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 140px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.login-container {
  width: 100%;
  max-width: 480px;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 48px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.login-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--ozon-text);
  margin-bottom: 8px;
  text-align: center;
}

.login-subtitle {
  color: var(--ozon-text-secondary);
  text-align: center;
  margin-bottom: 32px;
  font-size: 15px;
}

.login-form {
  margin-bottom: 32px;
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

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  font-size: 14px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--ozon-text);
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.forgot-password {
  color: var(--ozon-primary);
  font-weight: 500;
  transition: opacity 0.2s;
}

.forgot-password:hover {
  opacity: 0.8;
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

.login-btn {
  width: 100%;
  padding: 14px;
  background: var(--ozon-primary);
  color: white;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
}

.login-btn:hover:not(:disabled) {
  background: var(--ozon-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 91, 255, 0.3);
}

.login-btn:active:not(:disabled) {
  transform: translateY(0);
}

.login-btn:disabled {
  background: var(--ozon-text-secondary);
  opacity: 0.6;
  cursor: not-allowed;
}

.register-link {
  text-align: center;
  color: var(--ozon-text-secondary);
  font-size: 15px;
}

.register-link a {
  color: var(--ozon-primary);
  font-weight: 600;
  transition: opacity 0.2s;
}

.register-link a:hover {
  opacity: 0.8;
}

@media (max-width: 768px) {
  .login-card {
    padding: 32px 24px;
  }

  .login-title {
    font-size: 28px;
  }

  .form-options {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
}
</style>
