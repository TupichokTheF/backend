<template>
  <div class="products-page">
    <div class="container">
      <h1 class="page-title">Все товары</h1>

      <div class="filters">
        <button
          v-for="category in categories"
          :key="category"
          :class="['filter-btn', { active: activeCategory === category }]"
          @click="activeCategory = category"
        >
          {{ category }}
        </button>
      </div>

      <div class="products-grid">
        <ProductCard
          v-for="product in filteredProducts"
          :key="product.id"
          :product="product"
          @add-to-cart="handleAddToCart"
        />
      </div>
    </div>
  </div>
</template>

<script>
import ProductCard from '../components/ProductCard.vue'

export default {
  name: 'Products',
  components: {
    ProductCard
  },
  data() {
    return {
      activeCategory: 'Все товары',
      categories: ['Все товары', 'Электроника', 'Компьютеры', 'Умные устройства', 'Для дома'],
      allProducts: [
        {
          id: 1,
          title: 'Смартфон Apple iPhone 15 Pro 256GB',
          emoji: '📱',
          imageColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          price: 99990,
          oldPrice: 129990,
          ozonCard: true,
          ozonCardPrice: 94990,
          discount: 23,
          rating: 4.8,
          reviews: 1547,
          category: 'Электроника'
        },
        {
          id: 2,
          title: 'Ноутбук Apple MacBook Air 13" M2 256GB',
          emoji: '💻',
          imageColor: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
          price: 119990,
          oldPrice: 139990,
          ozonCard: true,
          ozonCardPrice: 114990,
          discount: 14,
          rating: 4.9,
          reviews: 892,
          category: 'Компьютеры'
        },
        {
          id: 3,
          title: 'Беспроводные наушники Sony WH-1000XM5',
          emoji: '🎧',
          imageColor: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
          price: 29990,
          oldPrice: 34990,
          ozonCard: true,
          ozonCardPrice: 27990,
          discount: 14,
          rating: 4.7,
          reviews: 2341,
          category: 'Электроника'
        },
        {
          id: 4,
          title: 'Умные часы Apple Watch Series 9 GPS 41mm',
          emoji: '⌚',
          imageColor: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
          price: 39990,
          oldPrice: 44990,
          ozonCard: true,
          ozonCardPrice: 37990,
          discount: 11,
          rating: 4.6,
          reviews: 734,
          category: 'Умные устройства'
        },
        {
          id: 5,
          title: 'Игровая консоль Sony PlayStation 5 Slim',
          emoji: '🎮',
          imageColor: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
          price: 54990,
          oldPrice: 59990,
          ozonCard: true,
          ozonCardPrice: 52990,
          discount: 8,
          rating: 4.9,
          reviews: 1123,
          category: 'Электроника'
        },
        {
          id: 6,
          title: 'Робот-пылесос Xiaomi Robot Vacuum S10+',
          emoji: '🤖',
          imageColor: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
          price: 34990,
          oldPrice: 49990,
          ozonCard: true,
          ozonCardPrice: 32990,
          discount: 30,
          rating: 4.5,
          reviews: 456,
          category: 'Для дома'
        },
        {
          id: 7,
          title: 'Кофемашина De\'Longhi Magnifica Start',
          emoji: '☕',
          imageColor: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
          price: 44990,
          oldPrice: 54990,
          ozonCard: true,
          ozonCardPrice: 42990,
          discount: 18,
          rating: 4.7,
          reviews: 623,
          category: 'Для дома'
        },
        {
          id: 8,
          title: 'Электросамокат Kugoo M4 Pro',
          emoji: '🛴',
          imageColor: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
          price: 29990,
          oldPrice: 39990,
          ozonCard: true,
          ozonCardPrice: 27990,
          discount: 25,
          rating: 4.4,
          reviews: 891,
          category: 'Электроника'
        },
        {
          id: 9,
          title: 'Умная колонка Яндекс Станция Макс',
          emoji: '🔊',
          imageColor: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
          price: 19990,
          oldPrice: 24990,
          ozonCard: true,
          ozonCardPrice: 18990,
          discount: 20,
          rating: 4.6,
          reviews: 1234,
          category: 'Умные устройства'
        },
        {
          id: 10,
          title: 'Планшет Samsung Galaxy Tab S9 128GB',
          emoji: '📱',
          imageColor: 'linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%)',
          price: 54990,
          oldPrice: 64990,
          ozonCard: true,
          ozonCardPrice: 52990,
          discount: 15,
          rating: 4.8,
          reviews: 567,
          category: 'Электроника'
        },
        {
          id: 11,
          title: 'Видеокарта NVIDIA GeForce RTX 4070',
          emoji: '🎨',
          imageColor: 'linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)',
          price: 64990,
          rating: 4.9,
          reviews: 234,
          category: 'Компьютеры'
        },
        {
          id: 12,
          title: 'Фитнес-браслет Xiaomi Mi Band 8 Pro',
          emoji: '⌚',
          imageColor: 'linear-gradient(135deg, #f77062 0%, #fe5196 100%)',
          price: 4990,
          rating: 4.5,
          reviews: 1890,
          category: 'Умные устройства'
        }
      ]
    }
  },
  computed: {
    filteredProducts() {
      if (this.activeCategory === 'Все товары') {
        return this.allProducts
      }
      return this.allProducts.filter(product => product.category === this.activeCategory)
    }
  },
  methods: {
    handleAddToCart(product) {
      alert(`Товар "${product.title}" добавлен в корзину!`)
    }
  }
}
</script>

<style scoped>
.products-page {
  padding: 32px 0;
  min-height: 70vh;
}

.page-title {
  font-size: 36px;
  font-weight: bold;
  color: var(--ozon-text);
  margin-bottom: 32px;
}

.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 12px 24px;
  border: 2px solid var(--ozon-border);
  background: white;
  color: var(--ozon-text);
  border-radius: 24px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: var(--ozon-primary);
  color: var(--ozon-primary);
}

.filter-btn.active {
  background: var(--ozon-primary);
  border-color: var(--ozon-primary);
  color: white;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 28px;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
  }
}
</style>
