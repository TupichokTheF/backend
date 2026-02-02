<template>
  <div class="favorites-page">
    <div class="container">
      <h1 class="page-title">Избранное</h1>

      <!-- Загрузка -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Загрузка избранных товаров...</p>
      </div>

      <!-- Ошибка -->
      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchFavorites" class="retry-btn">Попробовать снова</button>
      </div>

      <!-- Пустой список -->
      <div v-else-if="favorites.length === 0" class="empty-state">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="currentColor">
          <path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z"/>
        </svg>
        <h2>В избранном пока ничего нет</h2>
        <p>Добавляйте товары в избранное, чтобы не потерять их</p>
        <router-link to="/products" class="browse-btn">Перейти к товарам</router-link>
      </div>

      <!-- Список избранных товаров -->
      <div v-else class="favorites-grid">
        <article v-for="item in favorites" :key="item.product_id" class="favorite-card">
          <div class="favorite-image">
            <img
              v-if="item.image"
              :src="'data:image/png;base64,' + item.image"
              :alt="item.product_name"
            />
            <div v-else class="no-image">Нет фото</div>
          </div>
          <div class="favorite-info">
            <h3 class="favorite-name">{{ item.product_name }}</h3>
            <p class="favorite-price">{{ formatPrice(item.price) }} ₽</p>
          </div>
          <button @click="removeFromFavorites(item.product_id)" class="remove-btn" title="Удалить из избранного">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
import { handle401, logout } from '../utils/api.js'

export default {
  name: 'Favorites',
  data() {
    return {
      favorites: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.fetchFavorites()
  },
  methods: {
    formatPrice(price) {
      return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    },

    async fetchFavorites(retry = true) {
      let token = localStorage.getItem('access_token')

      if (!token) {
        this.$router.push('/login')
        return
      }

      this.loading = true
      this.error = null

      try {
        const response = await fetch('http://localhost:8000/api/products/favourite_products', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        })

        if (response.status === 401) {
          if (retry) {
            const newToken = await handle401(this.$router)
            if (newToken) {
              return this.fetchFavorites(false)
            }
          } else {
            logout()
            this.$router.push('/')
          }
          return
        }

        if (!response.ok) {
          throw new Error('Не удалось загрузить избранное')
        }

        const data = await response.json()
        this.favorites = data

      } catch (error) {
        console.error('Ошибка:', error)
        this.error = 'Не удалось загрузить избранные товары. Проверьте соединение с сервером.'
      } finally {
        this.loading = false
      }
    },

    async removeFromFavorites(productId, retry = true) {
      let token = localStorage.getItem('access_token')

      try {
        const response = await fetch('http://localhost:8000/api/products/delete_favourite', {
          method: 'DELETE',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            product_id: productId
          })
        })

        if (response.status === 401) {
          if (retry) {
            const newToken = await handle401(this.$router)
            if (newToken) {
              return this.removeFromFavorites(productId, false)
            }
          } else {
            logout()
            this.$router.push('/')
          }
          return
        }

        if (response.ok) {
          this.favorites = this.favorites.filter(item => item.product_id !== productId)
        }
      } catch (error) {
        console.error('Ошибка при удалении:', error)
      }
    }
  }
}
</script>

<style scoped>
.favorites-page {
  min-height: calc(100vh - 140px);
  padding: 40px 0;
  background: var(--ozon-background);
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--ozon-text);
  margin-bottom: 32px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: var(--ozon-text-secondary);
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--ozon-border);
  border-top-color: var(--ozon-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  color: var(--ozon-text-secondary);
}

.empty-state svg {
  color: var(--ozon-border);
  margin-bottom: 24px;
}

.empty-state h2 {
  font-size: 24px;
  color: var(--ozon-text);
  margin-bottom: 8px;
}

.empty-state p {
  margin-bottom: 24px;
}

.browse-btn,
.retry-btn {
  padding: 14px 32px;
  background: var(--ozon-primary);
  color: white;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: background 0.2s;
}

.browse-btn:hover,
.retry-btn:hover {
  background: var(--ozon-primary-dark);
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.favorite-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all 0.3s;
}

.favorite-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
}

.favorite-image {
  aspect-ratio: 1;
  background: var(--ozon-background);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.favorite-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  color: var(--ozon-text-secondary);
  font-size: 14px;
}

.favorite-info {
  padding: 16px;
}

.favorite-name {
  font-size: 15px;
  font-weight: 500;
  color: var(--ozon-text);
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.favorite-price {
  font-size: 20px;
  font-weight: 700;
  color: var(--ozon-text);
}

.remove-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ozon-text-secondary);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.remove-btn:hover {
  background: #fee;
  color: #dc3545;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 24px;
  }

  .favorites-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}
</style>
