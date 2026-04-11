<script setup>
import { ref, computed, onMounted } from 'vue'
import Header from './components/Header.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import ProductCard from './components/ProductCard.vue'
import BottomCart from './components/BottomCart.vue'
import CartModal from './components/CartModal.vue'
import { products as initialProducts } from './data/products'

const categories = ['KOLBASALAR', 'LAVASH', 'SHOURMA', 'BURGER']
const activeCategory = ref('KOLBASALAR')
const isCartOpen = ref(false)

const products = ref(initialProducts)

const cart = ref([])

const filteredProducts = computed(() => {
  return products.value.filter(p => p.category === activeCategory.value)
})

const cartTotal = computed(() => {
  return cart.value.reduce((total, item) => total + (item.price * item.quantity), 0)
})

const addToCart = (product) => {
  const existing = cart.value.find(item => item.id === product.id)
  if (existing) {
    existing.quantity++
  } else {
    cart.value.push({ ...product, quantity: 1 })
  }
  
  if (window.Telegram?.WebApp?.HapticFeedback) {
    window.Telegram.WebApp.HapticFeedback.impactOccurred('light')
  }
}

const updateQuantity = (id, delta) => {
  const item = cart.value.find(item => item.id === id)
  if (item) {
    item.quantity += delta
    if (item.quantity <= 0) {
      cart.value = cart.value.filter(i => i.id !== id)
    }
  }
}

const handleCheckout = (orderData) => {
  if (window.Telegram?.WebApp) {
    // Send data to bot and close Mini App
    window.Telegram.WebApp.sendData(JSON.stringify(orderData))
    window.Telegram.WebApp.close()
  } else {
    console.log("Order Data:", orderData)
    alert("Buyurtmangiz qabul qilindi (Demo modeda)")
  }
}

onMounted(() => {
  if (window.Telegram?.WebApp) {
    window.Telegram.WebApp.ready()
    window.Telegram.WebApp.expand()
    window.Telegram.WebApp.setHeaderColor('#ffffff')
    window.Telegram.WebApp.setBackgroundColor('#f7f9fc')
  }
})
</script>

<template>
  <div class="app-container">
    <Header />
    <CategoryTabs 
      :categories="categories" 
      :activeCategory="activeCategory"
      @change-category="activeCategory = $event"
    />
    
    <main class="content">
      <div class="category-title">
        <h2>{{ activeCategory }}</h2>
        <div class="underline"></div>
      </div>
      
      <div class="product-grid">
        <ProductCard 
          v-for="product in filteredProducts" 
          :key="product.id" 
          :product="product"
          @add="addToCart"
        />
      </div>
    </main>

    <BottomCart 
      :total="cartTotal" 
      @open-cart="isCartOpen = true"
    />

    <CartModal 
      :isOpen="isCartOpen" 
      :cart="cart" 
      :total="cartTotal"
      @close="isCartOpen = false"
      @update-quantity="updateQuantity"
      @checkout="handleCheckout"
    />
  </div>
</template>

<style>
@import './assets/main.css';

.app-container {
  padding-bottom: 80px;
}

.content {
  padding: 16px;
}

.category-title {
  margin-bottom: 16px;
}

.category-title h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: var(--text-color);
}

.category-title .underline {
  width: 40px;
  height: 3px;
  background-color: var(--primary-color);
  margin-top: 4px;
  border-radius: 2px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
</style>
