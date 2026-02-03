<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <h1 class="register-title">Регистрация</h1>
        <p class="register-subtitle">Создайте аккаунт для доступа к миллионам товаров</p>

        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="name">Имя и фамилия</label>
            <input
              type="text"
              id="name"
              v-model="name"
              placeholder="Введите ваше имя"
              required
            />
          </div>

          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="email"
              placeholder="example@email.com"
              required
            />
          </div>

          <div class="form-group">
            <label for="phone">Телефон</label>
            <input
              type="tel"
              id="phone"
              v-model="phone"
              placeholder="+7 (___) ___-__-__"
              required
            />
          </div>

          <div class="form-group">
            <label for="password">Пароль</label>
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="Минимум 8 символов"
              required
              minlength="8"
            />
            <div class="password-hint">
              Пароль должен содержать минимум 8 символов
            </div>
          </div>

          <div class="form-group">
            <label for="confirmPassword">Подтвердите пароль</label>
            <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="Повторите пароль"
              required
            />
            <div v-if="confirmPassword && password !== confirmPassword" class="error-hint">
              Пароли не совпадают
            </div>
          </div>

          <div class="form-checkbox">
            <label class="checkbox-label">
              <input type="checkbox" v-model="agreeTerms" required />
              <span>Я согласен с <a href="#" @click.prevent>условиями использования</a> и <a href="#" @click.prevent>политикой конфиденциальности</a></span>
            </label>
          </div>

          <div class="form-checkbox">
            <label class="checkbox-label">
              <input type="checkbox" v-model="subscribeNews" />
              <span>Получать новости и специальные предложения</span>
            </label>
          </div>

          <button type="submit" class="register-btn" :disabled="!isFormValid">
            Зарегистрироваться
          </button>
        </form>

        <div class="divider">
          <span>или</span>
        </div>

        <div class="social-register">
          <button class="social-btn vk-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12.785 16.241s.288-.032.436-.193c.136-.148.132-.425.132-.425s-.019-1.297.574-1.488c.586-.188 1.338 1.253 2.135 1.807.603.418 1.061.327 1.061.327l2.132-.03s1.115-.07.586-.96c-.043-.073-.309-.66-1.591-1.867-1.342-1.264-1.162-1.059.454-3.246.984-1.332 1.377-2.145 1.254-2.493-.117-.332-.84-.244-.84-.244l-2.4.015s-.178-.025-.31.056c-.129.079-.212.263-.212.263s-.379 1.023-.884 1.894c-1.065 1.837-1.492 1.933-1.667 1.818-.406-.267-.305-1.075-.305-1.648 0-1.792.268-2.54-.522-2.733-.262-.064-.455-.106-1.126-.113-.861-.009-1.589.003-2.001.208-.274.136-.486.44-.357.458.159.022.52.099.711.363.247.341.238 1.107.238 1.107s.142 2.11-.331 2.371c-.325.179-.77-.187-1.726-1.856-.489-.849-.859-1.787-.859-1.787s-.071-.177-.198-.272c-.154-.115-.37-.152-.37-.152l-2.281.015s-.343.01-.469.161c-.112.134-.009.411-.009.411s1.781 4.229 3.796 6.359c1.848 1.955 3.958 1.826 3.958 1.826h.951z"/>
            </svg>
            Регистрация через VK
          </button>
          <button class="social-btn google-btn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>
            Регистрация через Google
          </button>
        </div>

        <div class="login-link">
          Уже есть аккаунт? <router-link to="/login">Войти</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      name: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: '',
      agreeTerms: false,
      subscribeNews: false
    }
  },
  computed: {
    isFormValid() {
      return (
        this.name &&
        this.email &&
        this.phone &&
        this.password &&
        this.confirmPassword &&
        this.password === this.confirmPassword &&
        this.password.length >= 8 &&
        this.agreeTerms
      )
    }
  },
  methods: {
    handleRegister() {
      if (!this.isFormValid) {
        return
      }

      // TODO: Реализовать логику регистрации
      console.log('Register attempt:', {
        name: this.name,
        email: this.email,
        phone: this.phone,
        subscribeNews: this.subscribeNews
      })

      // Временная заглушка - перенаправление на главную
      alert('Регистрация успешна! Добро пожаловать на OZON!')
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: calc(100vh - 140px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.register-container {
  width: 100%;
  max-width: 520px;
}

.register-card {
  background: white;
  border-radius: 16px;
  padding: 48px 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.register-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--ozon-text);
  margin-bottom: 8px;
  text-align: center;
}

.register-subtitle {
  color: var(--ozon-text-secondary);
  text-align: center;
  margin-bottom: 32px;
  font-size: 15px;
}

.register-form {
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

.password-hint {
  margin-top: 6px;
  font-size: 13px;
  color: var(--ozon-text-secondary);
}

.error-hint {
  margin-top: 6px;
  font-size: 13px;
  color: #dc3545;
}

.form-checkbox {
  margin-bottom: 16px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
  color: var(--ozon-text);
  font-size: 14px;
  line-height: 1.5;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  margin-top: 2px;
  flex-shrink: 0;
}

.checkbox-label a {
  color: var(--ozon-primary);
  font-weight: 500;
  text-decoration: underline;
}

.checkbox-label a:hover {
  opacity: 0.8;
}

.register-btn {
  width: 100%;
  padding: 14px;
  background: var(--ozon-primary);
  color: white;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
  margin-top: 8px;
}

.register-btn:hover:not(:disabled) {
  background: var(--ozon-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 91, 255, 0.3);
}

.register-btn:active:not(:disabled) {
  transform: translateY(0);
}

.register-btn:disabled {
  background: var(--ozon-text-secondary);
  opacity: 0.5;
  cursor: not-allowed;
}

.divider {
  position: relative;
  text-align: center;
  margin: 32px 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--ozon-border);
}

.divider span {
  position: relative;
  background: white;
  padding: 0 16px;
  color: var(--ozon-text-secondary);
  font-size: 14px;
}

.social-register {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 12px;
  border: 2px solid var(--ozon-border);
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s;
}

.social-btn:hover {
  border-color: var(--ozon-text-secondary);
  transform: translateY(-1px);
}

.vk-btn {
  color: #0077FF;
}

.vk-btn:hover {
  background: rgba(0, 119, 255, 0.05);
  border-color: #0077FF;
}

.google-btn {
  color: var(--ozon-text);
}

.google-btn:hover {
  background: var(--ozon-background);
}

.login-link {
  text-align: center;
  color: var(--ozon-text-secondary);
  font-size: 15px;
}

.login-link a {
  color: var(--ozon-primary);
  font-weight: 600;
  transition: opacity 0.2s;
}

.login-link a:hover {
  opacity: 0.8;
}

@media (max-width: 768px) {
  .register-card {
    padding: 32px 24px;
  }

  .register-title {
    font-size: 28px;
  }
}
</style>
