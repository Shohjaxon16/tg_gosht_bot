<script setup>
import { ref, computed, onMounted } from 'vue'
import Header from './components/Header.vue'
import CategoryTabs from './components/CategoryTabs.vue'
import ProductCard from './components/ProductCard.vue'
import BottomCart from './components/BottomCart.vue'
import CartModal from './components/CartModal.vue'
import { products as initialProducts } from './data/products'

const categories = ['SOMSA', 'LAVASH', 'SHOURMA', 'BURGER']
const activeCategory = ref('SOMSA')
const isCartOpen = ref(false)
const products = ref(initialProducts)
const cart = ref([])

const getCartQuantity = (productId) => {
  const item = cart.value.find(p => p.id === productId)
  return item ? item.quantity : 0
}

const filteredProducts = computed(() => {
  return products.value.filter(p => p.category === activeCategory.value)
})

const cartTotal = computed(() => {
  return cart.value.reduce((sum, item) => sum + (item.price * item.quantity), 0)
})

const cartCount = computed(() => {
  return cart.value.reduce((sum, item) => sum + item.quantity, 0)
})

const addToCart = (product) => {
  const existingItem = cart.value.find(item => item.id === product.id)
  if (existingItem) {
    existingItem.quantity++
  } else {
    cart.value.push({ ...product, quantity: 1 })
  }
}

const updateQuantity = (productId, change) => {
  const item = cart.value.find(p => p.id === productId)
  if (item) {
    item.quantity += change
    if (item.quantity <= 0) {
      cart.value = cart.value.filter(p => p.id !== productId)
    }
  }
}

const handleCheckout = (orderData) => {
  if (window.Telegram?.WebApp) {
    // Buyurtmani botga yuborish va do'konni yopish
    window.Telegram.WebApp.sendData(JSON.stringify(orderData))
    window.Telegram.WebApp.close()
  } else {
    console.log("Order Data:", orderData)
    alert("Buyurtmangiz qabul qilindi (Demo)")
  }
}

onMounted(() => {
  if (window.Telegram?.WebApp) {
    const tg = window.Telegram.WebApp
    tg.ready()
    tg.expand()
    tg.setHeaderColor('#ffffff')
    tg.setBackgroundColor('#f7f9fc')
  }
})
</script>

<template>
  <div class="app-container">
    <Header />
    
    <main>
      <CategoryTabs 
        :categories="categories" 
        v-model="activeCategory" 
      />
      
      <div class="products-grid">
        <ProductCard 
          v-for="product in filteredProducts" 
          :key="product.id" 
          :product="product"
          :quantity="getCartQuantity(product.id)"
          @add="addToCart"
          @update="updateQuantity"
        />
      </div>
    </main>

    <BottomCart 
      v-if="cartCount > 0"
      :count="cartCount"
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
  max-width: 600px;
  margin: 0 auto;
  min-height: 100vh;
  background-color: #f7f9fc;
}

main {
  padding: 16px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 16px;
}
</style>
