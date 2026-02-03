<template>
  <section class="banner-section">
    <div class="container">
      <div class="banner-carousel">
        <div class="banner-track" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
          <div
            v-for="banner in banners"
            :key="banner.id"
            class="banner-slide"
            :style="{ background: banner.gradient }"
          >
            <div class="banner-content">
              <h2 class="banner-title">{{ banner.title }}</h2>
              <p class="banner-subtitle">{{ banner.subtitle }}</p>
              <button class="banner-btn">{{ banner.buttonText }}</button>
            </div>
            <div class="banner-emoji">{{ banner.emoji }}</div>
          </div>
        </div>

        <button class="carousel-btn prev" @click="prevSlide">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
          </svg>
        </button>
        <button class="carousel-btn next" @click="nextSlide">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </button>

        <div class="carousel-dots">
          <button
            v-for="(banner, index) in banners"
            :key="banner.id"
            :class="['dot', { active: currentSlide === index }]"
            @click="goToSlide(index)"
          ></button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Banner',
  data() {
    return {
      currentSlide: 0,
      autoplayInterval: null,
      banners: [
        {
          id: 1,
          title: 'Скидки до 70%',
          subtitle: 'На электронику и технику для дома',
          buttonText: 'Перейти к акции',
          emoji: '🎉',
          gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
        },
        {
          id: 2,
          title: 'Ozon Premium',
          subtitle: 'Бесплатная доставка и эксклюзивные предложения',
          buttonText: 'Оформить',
          emoji: '⭐',
          gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
        },
        {
          id: 3,
          title: 'Новинки сезона',
          subtitle: 'Модная одежда и аксессуары по выгодным ценам',
          buttonText: 'Смотреть',
          emoji: '👗',
          gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
        },
        {
          id: 4,
          title: 'Электроника',
          subtitle: 'Смартфоны, ноутбуки, планшеты со скидкой',
          buttonText: 'Выбрать',
          emoji: '📱',
          gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
        }
      ]
    }
  },
  mounted() {
    this.startAutoplay()
  },
  beforeUnmount() {
    this.stopAutoplay()
  },
  methods: {
    nextSlide() {
      this.currentSlide = (this.currentSlide + 1) % this.banners.length
      this.resetAutoplay()
    },
    prevSlide() {
      this.currentSlide = (this.currentSlide - 1 + this.banners.length) % this.banners.length
      this.resetAutoplay()
    },
    goToSlide(index) {
      this.currentSlide = index
      this.resetAutoplay()
    },
    startAutoplay() {
      this.autoplayInterval = setInterval(() => {
        this.nextSlide()
      }, 5000)
    },
    stopAutoplay() {
      if (this.autoplayInterval) {
        clearInterval(this.autoplayInterval)
      }
    },
    resetAutoplay() {
      this.stopAutoplay()
      this.startAutoplay()
    }
  }
}
</script>

<style scoped>
.banner-section {
  padding: 24px 0;
}

.banner-carousel {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  height: 320px;
}

.banner-track {
  display: flex;
  height: 100%;
  transition: transform 0.5s ease;
}

.banner-slide {
  min-width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 60px;
  color: white;
  position: relative;
  overflow: hidden;
}

.banner-content {
  max-width: 500px;
  z-index: 1;
}

.banner-title {
  font-size: 42px;
  font-weight: bold;
  margin-bottom: 16px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.banner-subtitle {
  font-size: 18px;
  margin-bottom: 24px;
  opacity: 0.95;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.banner-btn {
  padding: 14px 32px;
  background: white;
  color: var(--ozon-primary);
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.banner-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.banner-emoji {
  font-size: 180px;
  opacity: 0.3;
  position: absolute;
  right: 80px;
  z-index: 0;
  user-select: none;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ozon-text);
  transition: all 0.2s;
  z-index: 2;
}

.carousel-btn:hover {
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.carousel-btn.prev {
  left: 20px;
}

.carousel-btn.next {
  right: 20px;
}

.carousel-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 2;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  transition: all 0.3s;
  padding: 0;
}

.dot.active {
  width: 24px;
  border-radius: 4px;
  background: white;
}

@media (max-width: 768px) {
  .banner-carousel {
    height: 240px;
  }

  .banner-slide {
    padding: 30px;
  }

  .banner-title {
    font-size: 28px;
  }

  .banner-subtitle {
    font-size: 14px;
  }

  .banner-emoji {
    font-size: 100px;
    right: 20px;
  }

  .carousel-btn {
    width: 36px;
    height: 36px;
  }

  .carousel-btn.prev {
    left: 10px;
  }

  .carousel-btn.next {
    right: 10px;
  }
}
</style>
