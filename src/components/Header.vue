<template>
  <header class="header">
    <div class="logo-container">
      <div class="logo">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
          <polyline points="9 22 9 12 15 12 15 22" />
        </svg>
      </div>
      <div class="shop-info">
        <h1>MUXLISA FOOD</h1>
        <p>Onlayn buyurtma</p>
      </div>
    </div>
    <div class="lang-selector">
      <span>🌐 UZ</span>
    </div>
  </header>
  <div class="search-bar">
    <div class="search-input">
      <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
      <input type="text" placeholder="Qidiruv..." />
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: var(--secondary-color);
  border-bottom: 1px solid #eee;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 40px;
  height: 40px;
  background-color: var(--primary-color);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.logo svg {
  width: 24px;
  height: 24px;
}

.shop-info h1 {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  color: var(--primary-color);
}

.shop-info p {
  margin: 0;
  font-size: 12px;
  color: var(--text-secondary);
}

.lang-selector {
  font-size: 14px;
  font-weight: 500;
  color: var(--primary-color);
  background: #f0f7ff;
  padding: 4px 8px;
  border-radius: 20px;
}

.search-bar {
  padding: 12px 16px;
  background-color: var(--secondary-color);
}

.search-input {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  width: 18px;
  height: 18px;
  color: var(--text-secondary);
}

.search-input input {
  width: 100%;
  padding: 10px 10px 10px 40px;
  border: none;
  background-color: #f1f3f5;
  border-radius: 10px;
  font-size: 14px;
  outline: none;
}

.search-input input:focus {
  background-color: #e9ecef;
}
</style>
