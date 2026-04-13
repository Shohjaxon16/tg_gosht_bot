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
  <div class="product-card fade-in">
    <div class="image-wrapper">
      <img :src="product.image" :alt="product.name" />
      <button v-if="quantity === 0" class="add-btn" @click="$emit('add', product)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
          <line x1="12" y1="5" x2="12" y2="19" />
          <line x1="5" y1="12" x2="19" y2="12" />
        </svg>
      </button>
      <div v-else class="card-quantity-controls">
        <button @click="$emit('update', product.id, -1)">-</button>
        <span>{{ quantity }}</span>
        <button @click="$emit('update', product.id, 1)">+</button>
      </div>
    </div>
    <div class="info">
      <p class="price">{{ product.price.toLocaleString() }} so'm</p>
      <h3 class="name">{{ product.name }}</h3>
    </div>
  </div>
</template>

<style scoped>
.product-card {
  background-color: var(--secondary-color);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  min-width: 0; /* Grid blowoutni oldini oladi */
}

.image-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 1/1;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: contain; 
  padding: 8px; 
  box-sizing: border-box; /* padding rasmni kattalashtirib pachoqlab yubormasligi uchun */
  background-color: #ffffff; 
}

.add-btn {
  position: absolute;
  bottom: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  background-color: white;
  border: 1px solid #eee;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-color);
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.add-btn:active {
  transform: scale(0.9);
}

.add-btn svg {
  width: 16px;
  height: 16px;
}

.card-quantity-controls {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background-color: white;
  border: 1px solid #eee;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.card-quantity-controls button {
  border: none;
  background: none;
  font-weight: bold;
  font-size: 16px;
  color: var(--text-color);
  cursor: pointer;
  padding: 0 4px;
}

.card-quantity-controls span {
  font-size: 14px;
  font-weight: bold;
  min-width: 16px;
  text-align: center;
}

.info {
  padding: 12px;
  min-width: 0;
}

.price {
  margin: 0;
  font-size: 14px;
  font-weight: 700;
  color: var(--text-color);
  white-space: nowrap;
}

.name {
  margin: 4px 0 0;
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  word-wrap: break-word;
  white-space: pre-wrap;
}
</style>
