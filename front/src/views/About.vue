<template>
  <div class="about-page">
    <div class="container">
      <h1 class="page-title">О нас</h1>

      <div class="about-content">
        <section class="about-section">
          <h2>Добро пожаловать в OZON</h2>
          <p>
            Мы - один из крупнейших интернет-магазинов в России, предлагающий широкий ассортимент товаров
            для всей семьи. От электроники до товаров для дома, от книг до одежды - у нас вы найдете все необходимое.
          </p>
        </section>

        <section class="about-section">
          <h2>Наши преимущества</h2>
          <div class="advantages-grid">
            <div class="advantage-card">
              <div class="advantage-icon">🚀</div>
              <h3>Быстрая доставка</h3>
              <p>Доставим ваш заказ в кратчайшие сроки по всей России</p>
            </div>
            <div class="advantage-card">
              <div class="advantage-icon">💳</div>
              <h3>Удобная оплата</h3>
              <p>Множество способов оплаты, включая Ozon Card с выгодными условиями</p>
            </div>
            <div class="advantage-card">
              <div class="advantage-icon">🎁</div>
              <h3>Выгодные предложения</h3>
              <p>Регулярные акции, скидки и специальные предложения для наших клиентов</p>
            </div>
            <div class="advantage-card">
              <div class="advantage-icon">🛡️</div>
              <h3>Гарантия качества</h3>
              <p>Все товары сертифицированы и имеют гарантию производителя</p>
            </div>
          </div>
        </section>

        <section class="about-section">
          <h2>Наша миссия</h2>
          <p>
            Сделать онлайн-шопинг доступным, удобным и приятным для каждого. Мы стремимся предложить лучший
            сервис, широкий выбор качественных товаров и конкурентные цены.
          </p>
        </section>

        <section class="about-section">
          <h2>Контакты</h2>
          <div class="contact-info">
            <p><strong>Телефон:</strong> 8-800-234-56-78 (бесплатно по России)</p>
            <p><strong>Email:</strong> support@ozon.ru</p>
            <p><strong>Адрес:</strong> Москва, ул. Пресненская набережная, д. 10</p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about-page {
  padding: 32px 0;
  min-height: 70vh;
}

.page-title {
  font-size: 36px;
  font-weight: bold;
  color: var(--ozon-text);
  margin-bottom: 32px;
}

.about-content {
  max-width: 900px;
}

.about-section {
  margin-bottom: 48px;
}

.about-section h2 {
  font-size: 24px;
  font-weight: 600;
  color: var(--ozon-text);
  margin-bottom: 16px;
}

.about-section p {
  font-size: 16px;
  line-height: 1.6;
  color: var(--ozon-text-secondary);
  margin-bottom: 12px;
}

.advantages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

.advantage-card {
  padding: 24px;
  background: white;
  border: 1px solid var(--ozon-border);
  border-radius: 12px;
  transition: all 0.3s;
}

.advantage-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-4px);
}

.advantage-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.advantage-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--ozon-text);
  margin-bottom: 8px;
}

.advantage-card p {
  font-size: 14px;
  color: var(--ozon-text-secondary);
  margin: 0;
}

.contact-info p {
  font-size: 16px;
  margin-bottom: 12px;
}

.contact-info strong {
  color: var(--ozon-text);
}

@media (max-width: 768px) {
  .page-title {
    font-size: 28px;
  }

  .about-section h2 {
    font-size: 20px;
  }

  .advantages-grid {
    grid-template-columns: 1fr;
  }
}
</style>
