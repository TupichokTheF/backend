<template>
  <div>
    <Categories />
    <Banner />

    <main class="main-content">
      <!-- Индикатор загрузки -->
      <div v-if="loading" class="loading-state">
        <div class="loader"></div>
        <p>Загрузка товаров...</p>
      </div>

      <!-- Сообщение об ошибке -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <p>{{ error }}</p>
        <button @click="fetchProducts" class="retry-btn">Попробовать снова</button>
      </div>

      <!-- Основной контент -->
      <div v-else>
        <section class="products-section" v-if="popularProducts.length > 0">
          <div class="container">
            <div class="section-header">
              <h2 class="section-title">Популярные товары</h2>
              <router-link to="/products" class="see-all-link">Смотреть все →</router-link>
            </div>

            <div class="products-grid">
              <ProductCard
                v-for="product in popularProducts"
                :key="product.id"
                :product="product"
                @add-to-cart="handleAddToCart"
              />
            </div>
          </div>
        </section>

        <section class="products-section" v-if="allProducts.length > 0">
          <div class="container">
            <div class="section-header">
              <h2 class="section-title">Все товары</h2>
              <router-link to="/products" class="see-all-link">Смотреть все →</router-link>
            </div>

            <div class="products-grid">
              <ProductCard
                v-for="product in allProducts"
                :key="product.id"
                :product="product"
                @add-to-cart="handleAddToCart"
              />
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script>
import Categories from '../components/Categories.vue'
import Banner from '../components/Banner.vue'
import ProductCard from '../components/ProductCard.vue'

export default {
  name: 'Home',
  components: {
    Categories,
    Banner,
    ProductCard
  },
  data() {
    return {
      popularProducts: [],
      allProducts: [],
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchProducts()
  },
  methods: {
    async fetchProducts() {
      this.loading = true
      this.error = null

      try {
        // Параллельная загрузка популярных товаров и всех товаров
        const [popularResponse, allProductsResponse] = await Promise.all([
          fetch('http://localhost:8000/api/products/get_popular_products'),
          fetch('http://localhost:8000/api/products/get_products?limit=20&offset=0')
        ])

        if (!popularResponse.ok || !allProductsResponse.ok) {
          throw new Error('Ошибка загрузки данных с сервера')
        }

        const popularData = await popularResponse.json()
        const allProductsData = await allProductsResponse.json()

        // Преобразуем данные с API в формат компонента
        this.popularProducts = popularData.map(product => ({
          id: product.product_id,
          title: product.product_name,
          price: product.price,
          image: product.image,
          rating: 4.5 + Math.random() * 0.5,
          reviews: Math.floor(Math.random() * 1000) + 100
        }))

        this.allProducts = allProductsData.map(product => ({
          id: product.product_id,
          title: product.product_name,
          price: product.price,
          image: product.image,
          rating: 4.5 + Math.random() * 0.5,
          reviews: Math.floor(Math.random() * 1000) + 100
        }))

      } catch (error) {
        console.error('Ошибка при загрузке товаров:', error)
        this.error = 'Не удалось загрузить товары. Проверьте подключение к API.'
      } finally {
        this.loading = false
      }
    },
    handleAddToCart(product) {
      alert(`Товар "${product.title}" добавлен в корзину!`)
    }
  }
}
</script>

<style scoped>
.main-content {
  padding: 24px 0;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  text-align: center;
  padding: 40px 20px;
}

.loader {
  width: 50px;
  height: 50px;
  border: 5px solid var(--ozon-border);
  border-top-color: var(--ozon-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  font-size: 18px;
  color: var(--ozon-text-secondary);
}

.error-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.error-state p {
  font-size: 18px;
  color: var(--ozon-text);
  margin-bottom: 20px;
}

.retry-btn {
  padding: 12px 24px;
  background: var(--ozon-primary);
  color: white;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
}

.retry-btn:hover {
  background: var(--ozon-primary-dark);
  transform: translateY(-1px);
}

.products-section {
  margin-bottom: 48px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 28px;
  font-weight: bold;
  color: var(--ozon-text);
  margin: 0;
}

.see-all-link {
  color: var(--ozon-primary);
  font-size: 16px;
  font-weight: 500;
  transition: color 0.2s;
}

.see-all-link:hover {
  color: var(--ozon-primary-dark);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .section-title {
    font-size: 22px;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
  }
}
</style>
