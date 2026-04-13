<script setup>
defineProps({
  product: Object,
  quantity: {
    type: Number,
    default: 0
  }
})
defineEmits(['add', 'update'])
</script>

<template>
  <div class="product-card-clean fade-in">
    <div class="info-row">
      <div class="details">
        <h3 class="name">{{ product.name }}</h3>
        <p class="price">{{ product.price.toLocaleString() }} so'm</p>
      </div>
      
      <div class="actions">
        <button v-if="quantity === 0" class="add-btn" @click="$emit('add', product)">
          Qo'shish
        </button>
        <div v-else class="card-quantity-controls">
          <button @click="$emit('update', product.id, -1)">-</button>
          <span>{{ quantity }}</span>
          <button @click="$emit('update', product.id, 1)">+</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product-card-clean {
  background-color: var(--secondary-color);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--shadow);
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-width: 0;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.name {
  margin: 0;
  font-size: 16px;
  color: var(--text-color);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 700;
}

.price {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--primary-color);
}

.actions {
  display: flex;
  align-items: center;
}

.add-btn {
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: transform 0.2s;
}

.add-btn:active {
  transform: scale(0.95);
}

.card-quantity-controls {
  background-color: #f1f3f5;
  border: none;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
}

.card-quantity-controls button {
  border: none;
  background: white;
  border-radius: 6px;
  font-weight: bold;
  font-size: 16px;
  color: var(--text-color);
  cursor: pointer;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.card-quantity-controls span {
  font-size: 16px;
  font-weight: bold;
  min-width: 20px;
  text-align: center;
}
</style>
