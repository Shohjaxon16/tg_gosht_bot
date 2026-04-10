<script setup>
import { ref, computed, onMounted } from 'vue'
import Header from './components/Header.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import ProductCard from './components/ProductCard.vue'
import BottomCart from './components/BottomCart.vue'
import CartModal from './components/CartModal.vue'

const categories = ['SOMSA', 'LAVASH', 'SHOURMA', 'BURGER']
const activeCategory = ref('SOMSA')
const isCartOpen = ref(false)

const products = ref([
  { id: 1, name: "GO'SHTLI SOMSA", price: 12000, category: 'SOMSA', image: 'https://media-cdn.tripadvisor.com/media/photo-s/17/84/8f/33/caption.jpg' },
  { id: 2, name: "SIRLI SOMSA", price: 15000, category: 'SOMSA', image: 'https://www.gazeta.uz/media/img/2019/02/ZfXv9H15502287431268_l.jpg' },
  { id: 3, name: "KATTA LAVASH", price: 28000, category: 'LAVASH', image: 'https://cp.lider-food.uz/uploads/products/12/12_1623321600.jpg' },
  { id: 4, name: "MINI LAVASH", price: 22000, category: 'LAVASH', image: 'https://cp.lider-food.uz/uploads/products/12/12_1623321600.jpg' },
  { id: 5, name: "SHOURMA XL", price: 25000, category: 'SHOURMA', image: 'https://cp.lider-food.uz/uploads/products/11/11_1623321600.jpg' },
  { id: 6, name: "SHOURMA MINI", price: 18000, category: 'SHOURMA', image: 'https://cp.lider-food.uz/uploads/products/11/11_1623321600.jpg' },
  { id: 7, name: "CHEESE BURGER", price: 24000, category: 'BURGER', image: 'https://cp.lider-food.uz/uploads/products/10/10_1623321600.jpg' },
  { id: 8, name: "DOUBLE BURGER", price: 32000, category: 'BURGER', image: 'https://cp.lider-food.uz/uploads/products/10/10_1623321600.jpg' },
])

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
