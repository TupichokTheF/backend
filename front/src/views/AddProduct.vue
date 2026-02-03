<template>
  <div class="add-product-page">
    <div class="container">
      <div class="add-product-card">
        <h1 class="page-title">Добавить товар</h1>
        <p class="page-subtitle">Все поля обязательны для заполнения</p>

        <form @submit.prevent="handleSubmit" class="product-form">
          <div class="form-row">
            <div class="form-group full-width">
              <label for="name">Название товара *</label>
              <input
                type="text"
                id="name"
                v-model="product.name"
                placeholder="Введите название товара"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label for="description">Описание товара *</label>
              <textarea
                id="description"
                v-model="product.description"
                placeholder="Введите описание товара"
                rows="4"
                required
              ></textarea>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="price">Цена (₽) *</label>
              <input
                type="number"
                id="price"
                v-model.number="product.price"
                placeholder="0"
                min="0"
                step="0.01"
                required
              />
            </div>

            <div class="form-group">
              <label for="stock">Количество на складе *</label>
              <input
                type="number"
                id="stock"
                v-model.number="product.stock"
                placeholder="0"
                min="0"
                required
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group full-width">
              <label for="image">Фото товара *</label>
              <div class="image-upload">
                <input
                  type="file"
                  id="image"
                  @change="handleImageUpload"
                  accept="image/*"
                  ref="fileInput"
                />
                <div v-if="imagePreview" class="image-preview">
                  <img :src="imagePreview" alt="Предпросмотр" />
                  <button type="button" @click="removeImage" class="remove-image-btn">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                    </svg>
                  </button>
                </div>
                <div v-else class="upload-placeholder">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 7v2.99s-1.99.01-2 0V7h-3s.01-1.99 0-2h3V2h2v3h3v2h-3zm-3 4V8h-3V5H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-8h-3zM5 19l3-4 2 3 3-4 4 5H5z"/>
                  </svg>
                  <p>Нажмите для загрузки фото</p>
                </div>
              </div>
            </div>
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>

          <div class="form-actions">
            <button type="button" @click="$router.push('/')" class="cancel-btn">
              Отмена
            </button>
            <button type="submit" class="submit-btn" :disabled="loading">
              <span v-if="loading">Добавление...</span>
              <span v-else>Добавить товар</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddProduct',
  data() {
    return {
      product: {
        name: '',
        description: '',
        price: null,
        stock: null,
        image: ''
      },
      imagePreview: null,
      loading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  async mounted() {
    await this.checkAuth()
  },
  methods: {
    async checkAuth() {
      const token = localStorage.getItem('access_token')

      if (!token) {
        this.$router.push('/')
        return
      }

      try {
        const response = await fetch('http://localhost:8000/api/auth/check_auth', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          credentials: 'include'
        })

        if (response.status === 401) {
          // Неавторизован - удаляем токен и переходим на главную
          localStorage.removeItem('access_token')
          this.$router.push('/')
        }
      } catch (error) {
        console.error('Ошибка при проверке авторизации:', error)
        // При ошибке сети оставляем пользователя на странице
      }
    },
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (!file) return

      // Проверка типа файла
      if (!file.type.startsWith('image/')) {
        this.errorMessage = 'Пожалуйста, выберите изображение'
        return
      }

      // Проверка размера файла (максимум 5MB)
      if (file.size > 5 * 1024 * 1024) {
        this.errorMessage = 'Размер изображения не должен превышать 5MB'
        return
      }

      const reader = new FileReader()

      reader.onload = (e) => {
        this.imagePreview = e.target.result
        // Сохраняем base64 без префикса data:image/...;base64,
        this.product.image = e.target.result.split(',')[1]
      }

      reader.readAsDataURL(file)
    },
    removeImage() {
      this.imagePreview = null
      this.product.image = ''
      this.$refs.fileInput.value = ''
    },
    async handleSubmit() {
      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''

      // Проверка всех обязательных полей
      if (!this.product.name || !this.product.price || !this.product.stock) {
        this.errorMessage = 'Пожалуйста, заполните все обязательные поля'
        this.loading = false
        return
      }

      if (!this.product.description) {
        this.errorMessage = 'Пожалуйста, заполните описание товара'
        this.loading = false
        return
      }

      if (!this.product.image) {
        this.errorMessage = 'Пожалуйста, загрузите фото товара'
        this.loading = false
        return
      }

      const token = localStorage.getItem('access_token')
      if (!token) {
        localStorage.removeItem('access_token')
        this.$router.push('/')
        return
      }

      try {
        const response = await fetch('http://localhost:8000/api/products/create_product', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            product_name: this.product.name,
            description: this.product.description,
            price: this.product.price,
            stock: this.product.stock,
            image: this.product.image
          })
        })

        if (response.status === 401) {
          // Неавторизован - выходим и переходим на главную
          localStorage.removeItem('access_token')
          this.$router.push('/')
          return
        }

        if (!response.ok) {
          throw new Error('Ошибка при добавлении товара')
        }

        this.successMessage = 'Товар успешно добавлен!'

        // Очищаем форму
        this.product = {
          name: '',
          description: '',
          price: null,
          stock: null,
          image: ''
        }
        this.imagePreview = null
        this.$refs.fileInput.value = ''

        // Перенаправляем на главную через 2 секунды
        setTimeout(() => {
          this.$router.push('/')
        }, 2000)

      } catch (error) {
        console.error('Ошибка при добавлении товара:', error)
        this.errorMessage = 'Не удалось добавить товар. Попробуйте снова.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.add-product-page {
  min-height: calc(100vh - 140px);
  padding: 40px 20px;
  background: var(--ozon-background);
}

.add-product-card {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--ozon-text);
  margin-bottom: 8px;
}

.page-subtitle {
  color: var(--ozon-text-secondary);
  margin-bottom: 32px;
  font-size: 15px;
}

.product-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--ozon-text);
  font-size: 14px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--ozon-border);
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
  transition: all 0.2s;
  outline: none;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--ozon-primary);
  box-shadow: 0 0 0 3px rgba(0, 91, 255, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.image-upload {
  position: relative;
  cursor: pointer;
}

.image-upload input[type="file"] {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 1;
}

.upload-placeholder {
  border: 2px dashed var(--ozon-border);
  border-radius: 12px;
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--ozon-text-secondary);
  transition: all 0.2s;
}

.upload-placeholder:hover {
  border-color: var(--ozon-primary);
  background: rgba(0, 91, 255, 0.02);
}

.upload-placeholder svg {
  color: var(--ozon-text-secondary);
}

.image-preview {
  position: relative;
  border: 2px solid var(--ozon-border);
  border-radius: 12px;
  overflow: hidden;
  background: var(--ozon-background);
}

.image-preview img {
  width: 100%;
  height: 300px;
  object-fit: contain;
  display: block;
}

.remove-image-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #dc3545;
  transition: all 0.2s;
  z-index: 2;
}

.remove-image-btn:hover {
  background: white;
  transform: scale(1.1);
}

.error-message {
  background: #fee;
  border: 1px solid #fcc;
  color: #c33;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}

.success-message {
  background: #efe;
  border: 1px solid #cfc;
  color: #363;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 16px;
}

.cancel-btn,
.submit-btn {
  padding: 12px 32px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
}

.cancel-btn {
  background: white;
  color: var(--ozon-text);
  border: 2px solid var(--ozon-border);
}

.cancel-btn:hover {
  background: var(--ozon-background);
  border-color: var(--ozon-text-secondary);
}

.submit-btn {
  background: var(--ozon-primary);
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: var(--ozon-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 91, 255, 0.3);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  background: var(--ozon-text-secondary);
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .add-product-card {
    padding: 24px;
  }

  .page-title {
    font-size: 24px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .cancel-btn,
  .submit-btn {
    width: 100%;
  }
}
</style>
