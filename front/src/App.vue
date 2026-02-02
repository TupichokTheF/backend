<template>
  <div id="app">
    <Header />
    <router-view />
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h3>О компании</h3>
            <ul>
              <li><router-link to="/about">О нас</router-link></li>
              <li><a href="#">Вакансии</a></li>
              <li><a href="#">Пресс-служба</a></li>
            </ul>
          </div>

          <div class="footer-section">
            <h3>Покупателям</h3>
            <ul>
              <li><a href="#">Как сделать заказ</a></li>
              <li><a href="#">Способы оплаты</a></li>
              <li><a href="#">Доставка</a></li>
            </ul>
          </div>

          <div class="footer-section">
            <h3>Партнерам</h3>
            <ul>
              <li><a href="#">Продавайте на Ozon</a></li>
              <li><a href="#">Ozon Premium</a></li>
              <li><a href="#">Партнерская программа</a></li>
            </ul>
          </div>

          <div class="footer-section">
            <h3>Служба поддержки</h3>
            <ul>
              <li><a href="#">Помощь</a></li>
              <li><a href="#">Возврат товара</a></li>
              <li><a href="#">Обратная связь</a></li>
            </ul>
          </div>
        </div>

        <div class="footer-bottom">
          <p>&copy; 2026 OZON - Vue Demo Project</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import Header from './components/Header.vue'

export default {
  name: 'App',
  components: {
    Header
  }
}
</script>

<style scoped>
.footer {
  background: var(--ozon-text);
  color: white;
  padding: 48px 0 24px;
  margin-top: 48px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 32px;
  margin-bottom: 32px;
}

.footer-section h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section ul li {
  margin-bottom: 12px;
}

.footer-section ul li a {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
  transition: color 0.2s;
}

.footer-section ul li a:hover {
  color: white;
}

.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 24px;
  text-align: center;
}

.footer-bottom p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}
</style>
