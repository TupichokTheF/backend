<template>
  <div class="cart-page">
    <div class="container">
      <h1 class="page-title">Корзина</h1>

      <!-- Загрузка -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Загрузка корзины...</p>
      </div>

      <!-- Ошибка -->
      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchCart" class="btn-primary">Попробовать снова</button>
      </div>

      <!-- Пустая корзина -->
      <div v-else-if="cartItems.length === 0" class="empty-cart">
        <div class="empty-icon">🛒</div>
        <h2>Корзина пуста</h2>
        <p>Добавьте товары из каталога, чтобы оформить заказ</p>
        <router-link to="/products" class="btn-primary">Перейти к покупкам</router-link>
      </div>

      <!-- Содержимое корзины -->
      <div v-else class="cart-content">
        <div class="cart-items">
          <div v-for="item in cartItems" :key="item.product_id" class="cart-item">
            <div class="item-image">
              <img
                v-if="item.image"
                :src="'data:image/png;base64,' + item.image"
                :alt="item.product_name"
              />
              <span v-else class="no-image">Нет фото</span>
            </div>
            <div class="item-info">
              <h3 class="item-title">{{ item.product_name }}</h3>
              <div class="item-price">{{ formatPrice(item.price) }} ₽</div>
            </div>
            <div class="item-quantity">
              <button @click="decreaseQuantity(item.product_id)" class="qty-btn">-</button>
              <span class="qty-value">{{ item.quantity || 1 }}</span>
              <button @click="increaseQuantity(item.product_id)" class="qty-btn">+</button>
            </div>
            <div class="item-total">{{ formatPrice(item.price * (item.quantity || 1)) }} ₽</div>
            <button @click="removeItem(item.product_id)" class="remove-btn">×</button>
          </div>
        </div>

        <div class="cart-summary">
          <h2>Итого</h2>
          <div class="summary-row">
            <span>Товары ({{ totalItems }})</span>
            <span>{{ formatPrice(totalPrice) }} ₽</span>
          </div>
          <div class="summary-row">
            <span>Доставка</span>
            <span class="free">Бесплатно</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-row total">
            <span>К оплате</span>
            <span>{{ formatPrice(totalPrice) }} ₽</span>
          </div>
          <button class="checkout-btn">Оформить заказ</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { handle401, logout } from '../utils/api.js'

export default {
  name: 'Cart',
  data() {
    return {
      cartItems: [],
      originalQuantities: {},
      loading: true,
      error: null
    }
  },
  computed: {
    totalItems() {
      return this.cartItems.reduce((total, item) => total + (item.quantity || 1), 0)
    },
    totalPrice() {
      return this.cartItems.reduce((total, item) => total + (item.price * (item.quantity || 1)), 0)
    },
    hasQuantityChanges() {
      return this.cartItems.some(item =>
        this.originalQuantities[item.product_id] !== item.quantity
      )
    }
  },
  mounted() {
    this.fetchCart()
  },
  beforeUnmount() {
    this.saveQuantityChanges()
  },
  beforeRouteLeave(to, from, next) {
    this.saveQuantityChanges()
    next()
  },
  methods: {
    formatPrice(price) {
      return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    },

    async fetchCart(retry = true) {
      let token = localStorage.getItem('access_token')

      if (!token) {
        this.$router.push('/login')
        return
      }

      this.loading = true
      this.error = null

      try {
        const response = await fetch('http://localhost:8000/api/cart/get', {
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
              return this.fetchCart(false) // Повторяем запрос с новым токеном
            }
          } else {
            logout()
            this.$router.push('/')
          }
          return
        }

        if (!response.ok) {
          throw new Error('Не удалось загрузить корзину')
        }

        const data = await response.json()
        console.log('Ответ корзины:', data)

        // Обработка разных форматов ответа
        const items = Array.isArray(data) ? data : (data.cart_data || data.items || [])

        this.cartItems = items.map(item => ({
          ...item,
          quantity: parseInt(item.quantity, 10) || 1
        }))

        // Сохраняем оригинальные значения количества
        this.originalQuantities = {}
        this.cartItems.forEach(item => {
          this.originalQuantities[item.product_id] = item.quantity
        })

      } catch (error) {
        console.error('Ошибка:', error)
        this.error = 'Не удалось загрузить корзину. Проверьте соединение с сервером.'
      } finally {
        this.loading = false
      }
    },

    increaseQuantity(productId) {
      const item = this.cartItems.find(item => item.product_id === productId)
      if (item) {
        item.quantity = (parseInt(item.quantity, 10) || 1) + 1
      }
    },

    decreaseQuantity(productId) {
      const item = this.cartItems.find(item => item.product_id === productId)
      const qty = parseInt(item?.quantity, 10) || 1
      if (item && qty > 1) {
        item.quantity = qty - 1
      }
    },

    async saveQuantityChanges() {
      if (!this.hasQuantityChanges || this.cartItems.length === 0) {
        return
      }

      const token = localStorage.getItem('access_token')
      if (!token) return

      const cartData = this.cartItems.map(item => ({
        product_id: item.product_id,
        quantity: item.quantity
      }))

      try {
        await fetch('http://localhost:8000/api/cart/update_quantity', {
          method: 'PATCH',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            cart_data: cartData
          })
        })
      } catch (error) {
        console.error('Ошибка при сохранении количества:', error)
      }
    },

    async removeItem(productId, retry = true) {
      let token = localStorage.getItem('access_token')

      try {
        const response = await fetch('http://localhost:8000/api/cart/delete_product', {
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
              return this.removeItem(productId, false)
            }
          } else {
            logout()
            this.$router.push('/')
          }
          return
        }

        if (response.ok) {
          this.cartItems = this.cartItems.filter(item => item.product_id !== productId)
          delete this.originalQuantities[productId]
        }
      } catch (error) {
        console.error('Ошибка при удалении:', error)
      }
    }
  }
}
</script>

<style scoped>
.cart-page {
  padding: 32px 0;
  min-height: 70vh;
}

.page-title {
  font-size: 36px;
  font-weight: bold;
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

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  color: var(--ozon-text-secondary);
}

.empty-cart {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 24px;
}

.empty-cart h2 {
  font-size: 28px;
  color: var(--ozon-text);
  margin-bottom: 12px;
}

.empty-cart p {
  font-size: 16px;
  color: var(--ozon-text-secondary);
  margin-bottom: 32px;
}

.btn-primary {
  display: inline-block;
  padding: 14px 32px;
  background: var(--ozon-primary);
  color: white;
  border-radius: 12px;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: var(--ozon-primary-dark);
}

.cart-content {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 32px;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto auto;
  gap: 20px;
  align-items: center;
  padding: 20px;
  background: white;
  border: 1px solid var(--ozon-border);
  border-radius: 12px;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--ozon-background);
  overflow: hidden;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  font-size: 12px;
  color: var(--ozon-text-secondary);
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--ozon-text);
  margin: 0;
}

.item-price {
  font-size: 18px;
  font-weight: 600;
  color: var(--ozon-text);
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid var(--ozon-border);
  border-radius: 8px;
  padding: 4px;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: var(--ozon-background);
  color: var(--ozon-text);
  border-radius: 6px;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s;
}

.qty-btn:hover {
  background: var(--ozon-border);
}

.qty-value {
  font-size: 16px;
  font-weight: 500;
  min-width: 30px;
  text-align: center;
}

.item-total {
  font-size: 20px;
  font-weight: 600;
  color: var(--ozon-text);
  min-width: 150px;
  text-align: right;
}

.remove-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: var(--ozon-background);
  color: var(--ozon-text-secondary);
  border-radius: 8px;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: #ffe4e4;
  color: #ff4444;
}

.cart-summary {
  padding: 24px;
  background: white;
  border: 1px solid var(--ozon-border);
  border-radius: 12px;
  height: fit-content;
  position: sticky;
  top: 20px;
}

.cart-summary h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: var(--ozon-text);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 16px;
  color: var(--ozon-text-secondary);
}

.summary-row.total {
  font-size: 20px;
  font-weight: 600;
  color: var(--ozon-text);
}

.summary-row .free {
  color: #4caf50;
  font-weight: 500;
}

.summary-divider {
  height: 1px;
  background: var(--ozon-border);
  margin: 16px 0;
}

.checkout-btn {
  width: 100%;
  padding: 16px;
  background: var(--ozon-primary);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 16px;
}

.checkout-btn:hover {
  background: var(--ozon-primary-dark);
}

@media (max-width: 1024px) {
  .cart-content {
    grid-template-columns: 1fr;
  }

  .cart-summary {
    position: static;
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 28px;
  }

  .cart-item {
    grid-template-columns: 60px 1fr;
    gap: 12px;
  }

  .item-image {
    width: 60px;
    height: 60px;
  }

  .item-quantity,
  .item-total,
  .remove-btn {
    grid-column: 2;
  }

  .item-total {
    text-align: left;
  }
}
</style>
