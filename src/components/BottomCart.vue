<script setup>
defineProps({
  total: Number
})
defineEmits(['open-cart'])
</script>

<template>
  <div v-if="total > 0" class="bottom-cart fade-in" @click="$emit('open-cart')">
    <div class="cart-container">
      <div class="total-info">
        <div class="cart-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="9" cy="21" r="1" />
            <circle cx="20" cy="21" r="1" />
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" />
          </svg>
        </div>
        <span class="total-text">{{ total.toLocaleString() }} so'm</span>
      </div>
      <button class="checkout-btn">
        Savatcha
      </button>
    </div>
  </div>
</template>

<style scoped>
.bottom-cart {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--secondary-color);
  padding: 16px;
  box-shadow: 0 -4px 15px rgba(0,0,0,0.1);
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
  z-index: 100;
  max-width: 500px;
  margin: 0 auto;
}

.cart-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--primary-color);
  padding: 8px 8px 8px 16px;
  border-radius: 12px;
  color: white;
}

.total-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cart-icon {
  width: 24px;
  height: 24px;
}

.total-text {
  font-weight: 700;
  font-size: 16px;
}

.checkout-btn {
  background-color: rgba(255, 255, 255, 0.2);
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
}

.checkout-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
</style>
