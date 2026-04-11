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
    <div class="modal-content animate-slide-up">
      <div class="modal-header">
        <h3>Savat</h3>
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
        <p>Savatchangiz bo'sh</p>
      </div>

      <div class="checkout-form" v-if="cart.length > 0">
        <h4>Ma'lumotlar:</h4>
        <input v-model="name" type="text" placeholder="Ism" />
        <input v-model="phone" type="tel" placeholder="Telefon" />
        <textarea v-model="address" placeholder="Manzil"></textarea>
        
        <div class="summary">
          <span>Jami:</span>
          <strong>{{ total.toLocaleString() }} so'm</strong>
        </div>
        
        <button 
          class="submit-btn" 
          :disabled="!isFormValid"
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
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: flex-end;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 100%;
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
  max-height: 85vh;
  overflow-y: auto;
  padding: 20px;
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}

@keyframes slide-up {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: #f1f3f5;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f1f3f5;
}

.cart-item img {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
}

.item-details { flex: 1; }
.item-details h4 { margin: 0; font-size: 14px; }
.item-details p { margin: 2px 0 0; color: #ff5722; font-weight: 600; font-size: 14px; }

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 20px;
}

.quantity-controls button {
  border: none;
  background: none;
  font-weight: bold;
  font-size: 16px;
  color: #333;
  width: 20px;
}

.checkout-form {
  gap: 12px;
  display: flex;
  flex-direction: column;
  margin-top: 20px;
}

.checkout-form input, .checkout-form textarea {
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  background: #f8f9fa;
  font-size: 14px;
}

.summary {
  display: flex;
  justify-content: space-between;
  font-size: 18px;
  padding: 10px 0;
}

.submit-btn {
  background: #2196f3;
  color: white;
  border: none;
  padding: 16px;
  border-radius: 14px;
  font-weight: 600;
  width: 100%;
}

.submit-btn:disabled {
  background: #adb5bd;
}

.empty-cart { text-align: center; padding: 40px 0; }
</style>
