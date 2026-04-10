<script setup>
defineProps({
  categories: Array,
  activeCategory: String
})
defineEmits(['change-category'])
</script>

<template>
  <div class="categories">
    <button 
      v-for="cat in categories" 
      :key="cat"
      :class="['cat-btn', { active: activeCategory === cat }]"
      @click="$emit('change-category', cat)"
    >
      {{ cat }}
    </button>
  </div>
</template>

<style scoped>
.categories {
  display: flex;
  gap: 10px;
  padding: 12px 16px;
  overflow-x: auto;
  background-color: var(--secondary-color);
  scrollbar-width: none;
}

.categories::-webkit-scrollbar {
  display: none;
}

.cat-btn {
  padding: 8px 20px;
  border-radius: 20px;
  border: none;
  background-color: #f1f3f5;
  color: var(--text-color);
  font-weight: 600;
  font-size: 13px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cat-btn.active {
  background-color: var(--primary-color);
  color: white;
  box-shadow: 0 4px 10px rgba(0, 122, 255, 0.3);
}
</style>
