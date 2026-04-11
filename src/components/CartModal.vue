<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  cart: Array,
  total: Number,
  isOpen: Boolean
})

const emit = defineEmits(['close', 'update-quantity', 'checkout'])

const name = ref('')
const phone = ref('')
const address = ref('')

const isFormValid = computed(() => {
  return name.value.length >= 2 && phone.value.length >= 5 && address.value.length >= 3
})

const submitOrder = () => {
  if (!isFormValid.value) return
  
  const orderData = {
    user: {
      name: name.value,
      phone: phone.value,
      address: address.value
    },
    items: props.cart,
    total: props.total
  }
  
  emit('checkout', orderData)
}
</script>

<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content fade-in">
      <div class="modal-header">
        <h3>Savatcha</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <div class="cart-items" v-if="cart.length > 0">
        <div v-for="item in cart" :key="item.id" class="cart-item">
          <img :src="item.image" :alt="item.name" />
          <div class="item-details">
            <h4>{{ item.name }}</h4>
            <p>{{ item.price.toLocaleString() }} so'm</p>
          </div>
          <div class="quantity-controls">
            <button @click="$emit('update-quantity', item.id, -1)">-</button>
            <span>{{ item.quantity }}</span>
            <button @click="$emit('update-quantity', item.id, 1)">+</button>
          </div>
        </div>
      </div>
      <div v-else class="empty-cart">
        <p>Savatchangiz hozircha bo'sh</p>
      </div>

      <div class="checkout-form" v-if="cart.length > 0">
        <h4>Ma'lumotlaringiz:</h4>
        <input v-model="name" type="text" placeholder="Ismingiz" required />
        <input v-model="phone" type="tel" placeholder="Telefon raqamingiz" required />
        <textarea v-model="address" placeholder="Yetkazib berish manzili" required></textarea>
        
        <div class="summary">
          <span>Umumiy:</span>
          <strong>{{ total.toLocaleString() }} so'm</strong>
        </div>
        
        <button 
          class="submit-btn" 
          @click="submitOrder"
        >
          Buyurtmani tasdiqlash
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-end;
  z-index: 1000;
  max-width: 500px;
  margin: 0 auto;
}

.modal-content {
  background: white;
  width: 100%;
  border-top-left-radius: 24px;
  border-top-right-radius: 24px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 24px;
  padding-bottom: 40px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  color: var(--primary-color);
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: var(--text-secondary);
  cursor: pointer;
}

.cart-items {
  margin-bottom: 24px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.cart-item img {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  object-fit: cover;
}

.item-details {
  flex: 1;
}

.item-details h4 {
  margin: 0;
  font-size: 14px;
}

.item-details p {
  margin: 2px 0 0;
  font-size: 12px;
  color: var(--primary-color);
  font-weight: 600;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f1f3f5;
  padding: 4px;
  border-radius: 20px;
}

.quantity-controls button {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: none;
  background: white;
  color: var(--primary-color);
  font-weight: bold;
  cursor: pointer;
}

.checkout-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-top: 2px solid #f1f3f5;
  padding-top: 20px;
}

.checkout-form h4 {
  margin: 0 0 8px;
}

.checkout-form input, .checkout-form textarea {
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #ddd;
  font-size: 14px;
  outline: none;
}

.checkout-form input:focus {
  border-color: var(--primary-color);
}

.summary {
  display: flex;
  justify-content: space-between;
  font-size: 18px;
  margin: 12px 0;
}

.submit-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 16px;
  border-radius: 16px;
  font-weight: 700;
  font-size: 16px;
  cursor: pointer;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.empty-cart {
  text-align: center;
  padding: 40px 0;
  color: var(--text-secondary);
}
</style>
