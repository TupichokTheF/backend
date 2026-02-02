<template>
  <article class="product-card">
    <div class="product-image-wrapper">
      <button
        class="favorite-btn"
        :class="{ active: isFavorite, loading: isLoading }"
        :disabled="isLoading"
        @click.stop="toggleFavorite"
      >
        <svg v-if="!isLoading" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
          <path d="M14.5 2c-1.45 0-2.84.67-3.75 1.74C9.84 2.67 8.45 2 7 2 4.52 2 2.5 4.02 2.5 6.5c0 3.15 2.83 5.72 7.13 9.62L10 16.46l.38-.34C14.67 12.22 17.5 9.65 17.5 6.5 17.5 4.02 15.48 2 14.5 2zm-4.42 12.96l-.08.08-.08-.08C5.48 11.36 3 9.15 3 6.5 3 4.29 4.79 2.5 7 2.5c1.29 0 2.53.83 2.98 1.97h.05C10.47 3.33 11.71 2.5 13 2.5c2.21 0 4 1.79 4 4 0 2.65-2.48 4.86-6.92 8.46z"/>
        </svg>
        <span v-else class="spinner"></span>
      </button>

      <div class="product-image" :style="{ background: product.imageColor || 'var(--ozon-background)' }">
        <img
          v-if="product.image"
          :src="'data:image/png;base64,' + product.image"
          :alt="product.title"
          class="product-img"
        />
        <span v-else-if="product.emoji" class="product-emoji">{{ product.emoji }}</span>
      </div>

      <div v-if="product.discount" class="discount-badge">
        -{{ product.discount }}%
      </div>
    </div>

    <div class="product-info">
      <div class="product-price-block">
        <div class="product-price">
          <span class="current-price">{{ formatPrice(product.price) }} ₽</span>
          <span v-if="product.oldPrice" class="old-price">{{ formatPrice(product.oldPrice) }} ₽</span>
        </div>
        <div v-if="product.ozonCard" class="ozon-card-price">
          {{ formatPrice(product.ozonCardPrice) }} ₽ с Ozon Картой
        </div>
      </div>

      <div class="product-rating">
        <div class="stars">
          <span v-for="n in 5" :key="n" class="star" :class="{ filled: n <= Math.round(product.rating) }">★</span>
        </div>
        <span class="reviews-count">{{ product.reviews }}</span>
      </div>

      <h3 class="product-title">{{ product.title }}</h3>

      <button class="add-to-cart-btn" @click="addToCart">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
          <path d="M6 15c-.83 0-1.5.67-1.5 1.5S5.17 18 6 18s1.5-.67 1.5-1.5S6.83 15 6 15zm9 0c-.83 0-1.5.67-1.5 1.5s.67 1.5 1.5 1.5 1.5-.67 1.5-1.5-.67-1.5-1.5-1.5zM6.17 11l1.59-2.88L6.5 5H2V3h4.27l3.8 8H15l3-5.5h2L16.5 11H6.17zm8.33 0H7l-.5-1h7.5l.5 1z"/>
        </svg>
        <span>В корзину</span>
      </button>
    </div>
  </article>
</template>

<script>
import { handle401, logout } from '../utils/api.js'

export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isFavorite: false,
      isLoading: false
    }
  },
  methods: {
    formatPrice(price) {
      return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    },
    async toggleFavorite(retry = true) {
      if (this.isLoading) return

      let token = localStorage.getItem('access_token')
      if (!token) {
        alert('Для добавления в избранное необходимо авторизоваться')
        this.$router.push('/login')
        return
      }

      this.isLoading = true

      try {
        const response = await fetch('http://localhost:8000/api/products/add_to_favourite', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            product_id: this.product.id
          })
        })

        if (response.status === 401) {
          if (retry) {
            const newToken = await handle401(this.$router)
            if (newToken) {
              this.isLoading = false
              return this.toggleFavorite(false)
            }
          } else {
            logout()
            this.$router.push('/')
          }
          return
        }

        if (response.ok) {
          this.isFavorite = !this.isFavorite
        } else {
          const error = await response.json()
          alert(error.message || 'Ошибка при добавлении в избранное')
        }
      } catch (error) {
        console.error('Ошибка:', error)
        alert('Не удалось добавить в избранное. Проверьте соединение с сервером.')
      } finally {
        this.isLoading = false
      }
    },
    async addToCart(retry = true) {
      let token = localStorage.getItem('access_token')
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
            product_id: this.product.id
          })
        })

        if (response.status === 401) {
          if (retry) {
            const newToken = await handle401(this.$router)
            if (newToken) {
              return this.addToCart(false)
            }
          } else {
            logout()
            this.$router.push('/')
          }
          return
        }

        if (response.ok) {
          this.$emit('add-to-cart', this.product)
        } else {
          const error = await response.json()
          alert(error.message || 'Ошибка при добавлении в корзину')
        }
      } catch (error) {
        console.error('Ошибка:', error)
        alert('Не удалось добавить в корзину. Проверьте соединение с сервером.')
      }
    }
  }
}
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.product-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
}

.product-image-wrapper {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.favorite-btn {
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
  transition: all 0.2s;
  z-index: 1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.favorite-btn:hover {
  color: var(--ozon-secondary);
  transform: scale(1.1);
}

.favorite-btn.active {
  color: var(--ozon-secondary);
}

.favorite-btn.loading {
  pointer-events: none;
  opacity: 0.7;
}

.favorite-btn:disabled {
  cursor: not-allowed;
}

.favorite-btn .spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--ozon-border);
  border-top-color: var(--ozon-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.product-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--ozon-background);
}

.product-emoji {
  font-size: 80px;
  user-select: none;
}

.product-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.discount-badge {
  position: absolute;
  bottom: 12px;
  left: 12px;
  background: var(--ozon-secondary);
  color: white;
  padding: 6px 12px;
  border-radius: 6px;
  font-weight: bold;
  font-size: 14px;
}

.product-info {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.product-price-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.product-price {
  display: flex;
  align-items: center;
  gap: 8px;
}

.current-price {
  font-size: 20px;
  font-weight: bold;
  color: var(--ozon-text);
}

.old-price {
  font-size: 14px;
  color: var(--ozon-text-secondary);
  text-decoration: line-through;
}

.ozon-card-price {
  font-size: 13px;
  color: var(--ozon-primary);
  font-weight: 500;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stars {
  display: flex;
  gap: 2px;
}

.star {
  color: var(--ozon-border);
  font-size: 14px;
}

.star.filled {
  color: #ffa500;
}

.reviews-count {
  font-size: 13px;
  color: var(--ozon-text-secondary);
}

.product-title {
  font-size: 14px;
  line-height: 1.4;
  color: var(--ozon-text);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 0;
  font-weight: 400;
}

.add-to-cart-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: var(--ozon-primary);
  color: white;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.2s;
  margin-top: auto;
}

.add-to-cart-btn:hover {
  background: var(--ozon-primary-dark);
  transform: scale(1.02);
}

@media (max-width: 768px) {
  .product-emoji {
    font-size: 60px;
  }

  .current-price {
    font-size: 18px;
  }

  .product-title {
    font-size: 13px;
  }
}
</style>
