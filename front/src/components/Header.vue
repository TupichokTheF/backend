<template>
  <header class="header">
    <div class="header-top">
      <div class="container">
        <div class="header-top-content">
          <div class="header-location">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 0C5.243 0 3 2.243 3 5c0 4.5 5 11 5 11s5-6.5 5-11c0-2.757-2.243-5-5-5zm0 7.5c-1.381 0-2.5-1.119-2.5-2.5S6.619 2.5 8 2.5s2.5 1.119 2.5 2.5S9.381 7.5 8 7.5z"/>
            </svg>
            <span>Москва</span>
          </div>
          <nav class="header-nav">
            <router-link to="/">Главная</router-link>
            <router-link to="/products">Товары</router-link>
            <router-link to="/about">О нас</router-link>
            <router-link v-if="isAuthenticated" to="/add-product" class="add-product-link">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
              </svg>
              Добавить товар
            </router-link>
          </nav>
        </div>
      </div>
    </div>

    <div class="header-main">
      <div class="container">
        <div class="header-main-content">
          <router-link to="/" class="logo">OZON</router-link>

          <button class="catalog-btn">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <rect y="3" width="20" height="2"/>
              <rect y="9" width="20" height="2"/>
              <rect y="15" width="20" height="2"/>
            </svg>
            <span>Каталог</span>
          </button>

          <form class="search-bar" @submit.prevent="handleSearch">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Искать на OZON"
              @keyup.enter="handleSearch"
            />
            <button type="submit" class="search-btn">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path d="M8.5 3C5.46 3 3 5.46 3 8.5S5.46 14 8.5 14 14 11.54 14 8.5 11.54 3 8.5 3zm6.93 11.26l3.4 3.4c.2.2.2.51 0 .71-.1.1-.22.15-.35.15s-.26-.05-.35-.15l-3.4-3.4c-.95.7-2.12 1.12-3.38 1.12-3.04 0-5.5-2.46-5.5-5.5S5.46 3.5 8.5 3.5 14 5.96 14 9c0 1.26-.42 2.43-1.12 3.38z"/>
              </svg>
            </button>
          </form>

          <div class="header-actions">
            <!-- Кнопка входа для неавторизованных пользователей -->
            <router-link v-if="!isAuthenticated" to="/login" class="header-action-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
              </svg>
              <span>Войти</span>
            </router-link>

            <!-- Профиль для авторизованных пользователей -->
            <div v-else class="user-profile">
              <div class="header-action-btn user-btn">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
                </svg>
                <span>Профиль</span>
                <div class="user-badge"></div>
              </div>
              <button @click="logout" class="logout-btn" title="Выйти">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
                </svg>
              </button>
            </div>

            <router-link to="/favorites" class="header-action-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"/>
              </svg>
              <span>Избранное</span>
            </router-link>

            <router-link to="/cart" class="header-action-btn cart-btn">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z"/>
              </svg>
              <span>Корзина</span>
              <span class="cart-badge">0</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      isAuthenticated: false,
      searchQuery: ''
    }
  },
  mounted() {
    this.checkAuth()
  },
  watch: {
    $route() {
      // Проверяем авторизацию при каждом изменении маршрута
      this.checkAuth()
    }
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('access_token')
      this.isAuthenticated = !!token
    },
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push(`/search/${encodeURIComponent(this.searchQuery.trim())}`)
      }
    },
    async logout() {
      const token = localStorage.getItem('access_token')

      if (!token) {
        this.isAuthenticated = false
        return
      }

      try {
        // Отправляем запрос на сервер для выхода
        const response = await fetch('http://localhost:8000/api/auth/logout', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        })

        // Удаляем токен независимо от ответа сервера
        localStorage.removeItem('access_token')
        this.isAuthenticated = false

      } catch (error) {
        console.error('Ошибка при выходе:', error)
        // Даже при ошибке удаляем токен и выходим
        localStorage.removeItem('access_token')
        this.isAuthenticated = false
      }
    }
  }
}
</script>

<style scoped>
.header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-top {
  background: var(--ozon-background);
  padding: 8px 0;
  font-size: 13px;
  border-bottom: 1px solid var(--ozon-border);
}

.header-top-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-location {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--ozon-text-secondary);
  cursor: pointer;
}

.header-location:hover {
  color: var(--ozon-primary);
}

.header-nav {
  display: flex;
  gap: 24px;
}

.header-nav a {
  color: var(--ozon-text-secondary);
  transition: color 0.2s;
}

.header-nav a:hover {
  color: var(--ozon-primary);
}

.header-nav a.router-link-active {
  color: var(--ozon-primary);
  font-weight: 600;
}

.add-product-link {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--ozon-success) !important;
  font-weight: 600 !important;
}

.add-product-link:hover {
  opacity: 0.8;
}

.header-main {
  padding: 16px 0;
}

.header-main-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo {
  font-size: 28px;
  font-weight: bold;
  color: var(--ozon-primary);
  letter-spacing: 2px;
}

.catalog-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--ozon-primary);
  color: white;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  transition: background 0.2s;
}

.catalog-btn:hover {
  background: var(--ozon-primary-dark);
}

.search-bar {
  flex: 1;
  display: flex;
  position: relative;
}

.search-bar input {
  flex: 1;
  padding: 12px 50px 12px 16px;
  border: 2px solid var(--ozon-border);
  border-radius: 8px;
  font-size: 15px;
  outline: none;
  transition: border-color 0.2s;
}

.search-bar input:focus {
  border-color: var(--ozon-primary);
}

.search-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  padding: 8px;
  background: transparent;
  color: var(--ozon-text-secondary);
  border-radius: 6px;
  transition: all 0.2s;
}

.search-btn:hover {
  background: var(--ozon-background);
  color: var(--ozon-primary);
}

.header-actions {
  display: flex;
  gap: 8px;
}

.header-action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  background: transparent;
  color: var(--ozon-text);
  border-radius: 8px;
  font-size: 12px;
  transition: all 0.2s;
  position: relative;
}

.header-action-btn:hover {
  background: var(--ozon-background);
  color: var(--ozon-primary);
}

.cart-btn {
  color: var(--ozon-primary);
  font-weight: 600;
}

.cart-badge {
  position: absolute;
  top: 4px;
  right: 8px;
  background: var(--ozon-secondary);
  color: white;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 11px;
  font-weight: bold;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 4px;
  position: relative;
}

.user-btn {
  color: var(--ozon-success);
  font-weight: 600;
  cursor: default;
}

.user-btn:hover {
  background: transparent;
  color: var(--ozon-success);
}

.user-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: var(--ozon-success);
  border: 2px solid white;
  border-radius: 50%;
}

.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  background: transparent;
  color: var(--ozon-text-secondary);
  border-radius: 8px;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #fee;
  color: #dc3545;
}

@media (max-width: 768px) {
  .header-nav {
    display: none;
  }

  .header-action-btn span {
    display: none;
  }

  .catalog-btn span {
    display: none;
  }
}
</style>
