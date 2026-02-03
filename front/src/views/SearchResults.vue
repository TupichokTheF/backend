<template>
  <div class="search-page">
    <div class="container">
      <h1 class="page-title">Результаты поиска: "{{ searchQuery }}"</h1>

      <!-- Загрузка -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Поиск товаров...</p>
      </div>

      <!-- Ошибка -->
      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="search" class="retry-btn">Попробовать снова</button>
      </div>

      <!-- Ничего не найдено -->
      <div v-else-if="products.length === 0" class="empty-state">
        <svg width="80" height="80" viewBox="0 0 24 24" fill="currentColor">
          <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
        </svg>
        <h2>Ничего не найдено</h2>
        <p>Попробуйте изменить запрос или посмотрите наш каталог</p>
        <router-link to="/products" class="browse-btn">Перейти в каталог</router-link>
      </div>

      <!-- Результаты поиска -->
      <div v-else class="search-results">
        <p class="results-count">Найдено товаров: {{ products.length }}</p>
        <div class="products-grid">
          <article v-for="product in products" :key="product.product_id" class="product-card">
            <div class="product-image">
              <img
                v-if="product.image"
                :src="'data:image/png;base64,' + product.image"
                :alt="product.product_name"
              />
              <span v-else class="no-image">Нет фото</span>
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.product_name }}</h3>
              <p class="product-price">{{ formatPrice(product.price) }} ₽</p>
              <button @click="addToCart(product)" class="add-to-cart-btn">В корзину</button>
            </div>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { handle401, logout } from '../utils/api.js'

export default {
  name: 'SearchResults',
  data() {
    return {
      products: [],
      loading: true,
      error: null
    }
  },
  computed: {
    searchQuery() {
      return this.$route.params.query || ''
    }
  },
  watch: {
    '$route.params.query': {
      handler() {
        this.search()
      },
      immediate: true
    }
  },
  methods: {
    formatPrice(price) {
      return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    },

    async search(retry = true) {
      if (!this.searchQuery) {
        this.products = []
        this.loading = false
        return
      }

      this.loading = true
      this.error = null

      const token = localStorage.getItem('access_token')

      try {
        const response = await fetch(`http://localhost:8000/api/products/search/${encodeURIComponent(this.searchQuery)}`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Accept': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
          }
        })

        if (response.status === 401 && token) {
          if (retry) {
            const newToken = await handle401(this.$router)
            if (newToken) {
              return this.search(false)
            }
          } else {
            logout()
            this.$router.push('/')
          }
          return
        }

        if (!response.ok) {
          throw new Error('Не удалось выполнить поиск')
        }

        const data = await response.json()
        this.products = Array.isArray(data) ? data : (data.products || data.items || [])

      } catch (error) {
        console.error('Ошибка поиска:', error)
        this.error = 'Не удалось выполнить поиск. Проверьте соединение с сервером.'
      } finally {
        this.loading = false
      }
    },

    async addToCart(product, retry = true) {
      const token = localStorage.getItem('access_token')
      if (!token) {
        alert('Для добавления в корзину необходимо авторизоваться')
        this.$router.push('/login')
        return
      }

      try {
        const response = await fetch('http://localhost:8000/api/cart/add', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            product_id: product.product_id
          })
        })

        if (response.status === 401) {
          if (retry) {
            const newToken = await handle401(this.$router)
            if (newToken) {
              return this.addToCart(product, false)
            }
          } else {
            logout()
            this.$router.push('/')
          }
          return
        }

        if (response.ok) {
          alert('Товар добавлен в корзину')
        } else {
          const error = await response.json()
          alert(error.message || 'Ошибка при добавлении в корзину')
        }
      } catch (error) {
        console.error('Ошибка:', error)
        alert('Не удалось добавить в корзину')
      }
    }
  }
}
</script>

<style scoped>
.search-page {
  min-height: calc(100vh - 140px);
  padding: 40px 0;
  background: var(--ozon-background);
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--ozon-text);
  margin-bottom: 24px;
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

.results-count {
  color: var(--ozon-text-secondary);
  margin-bottom: 24px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 24px;
}

.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
}

.product-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
}

.product-image {
  aspect-ratio: 1;
  background: var(--ozon-background);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  color: var(--ozon-text-secondary);
  font-size: 14px;
}

.product-info {
  padding: 16px;
}

.product-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--ozon-text);
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-price {
  font-size: 20px;
  font-weight: 700;
  color: var(--ozon-text);
  margin-bottom: 12px;
}

.add-to-cart-btn {
  width: 100%;
  padding: 10px;
  background: var(--ozon-primary);
  color: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.2s;
}

.add-to-cart-btn:hover {
  background: var(--ozon-primary-dark);
}

@media (max-width: 768px) {
  .page-title {
    font-size: 22px;
  }

  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}
</style>
