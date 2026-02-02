<template>
  <section class="categories">
    <div class="container">
      <div class="categories-scroll">
        <a
          v-for="category in categories"
          :key="category.id"
          href="#"
          class="category-card"
        >
          <div class="category-icon" :style="{ background: category.color }">
            {{ category.icon }}
          </div>
          <span class="category-name">{{ category.name }}</span>
        </a>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Categories',
  data() {
    return {
      categories: [
        { id: 1, name: 'Электроника', icon: '📱', color: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
        { id: 2, name: 'Одежда', icon: '👕', color: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
        { id: 3, name: 'Обувь', icon: '👟', color: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' },
        { id: 4, name: 'Дом и сад', icon: '🏡', color: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' },
        { id: 5, name: 'Детские товары', icon: '🧸', color: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
        { id: 6, name: 'Красота', icon: '💄', color: 'linear-gradient(135deg, #30cfd0 0%, #330867 100%)' },
        { id: 7, name: 'Здоровье', icon: '⚕️', color: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)' },
        { id: 8, name: 'Бытовая техника', icon: '🔌', color: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)' },
        { id: 9, name: 'Спорт', icon: '⚽', color: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)' },
        { id: 10, name: 'Автотовары', icon: '🚗', color: 'linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%)' },
        { id: 11, name: 'Книги', icon: '📚', color: 'linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)' },
        { id: 12, name: 'Продукты', icon: '🍎', color: 'linear-gradient(135deg, #f77062 0%, #fe5196 100%)' }
      ]
    }
  }
}
</script>

<style scoped>
.categories {
  padding: 20px 0;
  background: white;
  border-bottom: 1px solid var(--ozon-border);
}

.categories-scroll {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding: 8px 0;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.categories-scroll::-webkit-scrollbar {
  display: none;
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 90px;
  padding: 12px;
  background: var(--ozon-background);
  border-radius: 12px;
  transition: all 0.2s;
  cursor: pointer;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.category-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
}

.category-name {
  font-size: 13px;
  text-align: center;
  color: var(--ozon-text);
  font-weight: 500;
  line-height: 1.2;
}

@media (max-width: 768px) {
  .category-card {
    min-width: 80px;
    padding: 8px;
  }

  .category-icon {
    width: 48px;
    height: 48px;
    font-size: 24px;
  }

  .category-name {
    font-size: 12px;
  }
}
</style>
