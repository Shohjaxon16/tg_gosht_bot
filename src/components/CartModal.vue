<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  cart: Array,
  total: Number,
  isOpen: Boolean
})

const emit = defineEmits(['close', 'update-quantity', 'checkout'])

const name = ref('')
const phone = ref('') // Faqat 9 ta raqam uchun
const address = ref('')
const mapContainer = ref(null)
let ymapsInstance = null
let mapObject = null
let lastPlacemark = null
const DELIVERY_FEE = 15000

// Telefon raqamini faqat raqamlardan iborat qilib, 9 xonagacha ishlash
const handlePhoneInput = (e) => {
  const value = e.target.value.replace(/\D/g, '')
  phone.value = value.slice(0, 9)
}

const isFormValid = computed(() => {
  return name.value.length >= 2 && phone.value.length === 9 && address.value.length >= 3
})

const initMap = () => {
  if (mapObject) return

  // Toshkent koordinatalari default sifatida
  const defaultCoords = [41.311081, 69.240562]

  mapObject = new window.ymaps.Map("yandex-map", {
    center: defaultCoords,
    zoom: 12,
    controls: ['zoomControl', 'geolocationControl']
  })

  // Marker qo'shish
  lastPlacemark = new window.ymaps.Placemark(defaultCoords, {}, {
    preset: 'islands#redDotIconWithCaption',
    draggable: true
  })

  mapObject.geoObjects.add(lastPlacemark)

  // Markerni surish tugatilganda manzilni olish
  lastPlacemark.events.add('dragend', function () {
    getAddress(lastPlacemark.geometry.getCoordinates())
  })

  // Xarita bosilganda markerni o'sha yerga ko'chirish
  mapObject.events.add('click', function (e) {
    const coords = e.get('coords')
    lastPlacemark.geometry.setCoordinates(coords)
    getAddress(coords)
  })

  // Geolokatsiyani aniqlash (agar ruxsat berilsa)
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const coords = [position.coords.latitude, position.coords.longitude]
      mapObject.setCenter(coords, 16)
      lastPlacemark.geometry.setCoordinates(coords)
      getAddress(coords)
    })
  }
}

const getAddress = (coords) => {
  window.ymaps.geocode(coords).then(function (res) {
    const firstGeoObject = res.geoObjects.get(0)
    address.value = firstGeoObject.getAddressLine()
  })
}

const submitOrder = () => {
  if (!isFormValid.value) return
  
  const orderData = {
    user: {
      name: name.value,
      phone: '+998' + phone.value,
      address: address.value,
      coords: lastPlacemark ? lastPlacemark.geometry.getCoordinates() : null
    },
    items: props.cart,
    total: props.total + DELIVERY_FEE
  }
  
  emit('checkout', orderData)
}

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    // Modal ochilganda xaritani darxol ishga tushiramiz
    setTimeout(() => {
      if (window.ymaps) {
        window.ymaps.ready(initMap)
      }
    }, 100)
  }
})
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
        
        <!-- Xarita to'g'ridan to'g'ri forma ichida -->
        <div class="inline-map-wrapper">
          <div id="yandex-map" class="inline-map"></div>
        </div>

        <div class="address-wrapper">
          <span class="field-label">Manzil *</span>
          <textarea v-model="address" placeholder="Yetkazib berish manzili avtomatik yoziladi..."></textarea>
        </div>

        <span class="field-label">Ma'lumotlar</span>
        <input v-model="name" type="text" placeholder="Ismingiz" />
        
        <div class="phone-input-wrapper">
          <span class="prefix">+998</span>
          <input 
            type="tel" 
            :value="phone" 
            @input="handlePhoneInput"
            placeholder="XX YYY ZZ ZZ"
            maxlength="9"
          />
        </div>
        
        <div class="summary-box">
          <div class="summary-line">
            <span>Mahsulotlar</span>
            <span>{{ total.toLocaleString() }} so'm</span>
          </div>
          <div class="summary-line">
            <span>Yetkazib berish</span>
            <span>{{ DELIVERY_FEE.toLocaleString() }} so'm</span>
          </div>
          <div class="summary-line total-line">
            <span>Jami</span>
            <span>{{ (total + DELIVERY_FEE).toLocaleString() }} so'm</span>
          </div>
        </div>
        
        <div class="bottom-checkout">
          <div class="bottom-total">{{ (total + DELIVERY_FEE).toLocaleString() }} so'm</div>
          <button 
            class="submit-btn" 
            :disabled="!isFormValid"
            @click="submitOrder"
          >
            Rasmiylashtirish
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
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
  max-height: 90vh;
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

.close-btn {
  background: #f1f3f5;
  border: none;
  width: 32px; height: 32px;
  border-radius: 50%;
  font-size: 20px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f1f3f5;
}

.cart-item img {
  width: 50px; height: 50px;
  border-radius: 10px;
  object-fit: cover;
}

.item-details { flex: 1; }
.item-details h4 { margin: 0; font-size: 14px; }
.item-details p { margin: 2px 0; color: #ff5722; font-weight: 700; }

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #f8f9fa;
  padding: 5px 10px;
  border-radius: 20px;
}

.quantity-controls button {
  border: none; background: none;
  font-weight: bold; font-size: 18px;
}

.checkout-form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.phone-input-wrapper {
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 0 12px;
  border: 1px solid #e9ecef;
}

.prefix {
  font-weight: 600;
  color: #495057;
  margin-right: 8px;
}

.checkout-form input, .checkout-form textarea {
  width: 100%;
  padding: 12px;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  background: #f8f9fa;
  font-size: 16px;
}

.phone-input-wrapper input {
  border: none;
  padding-left: 0;
}

.address-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.inline-map-wrapper {
  width: 100%;
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 15px;
}

.inline-map {
  width: 100%;
  height: 100%;
}

.field-label {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-color);
  margin-bottom: -5px;
}

.summary-box {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.summary-line {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #495057;
}

.total-line {
  margin-top: 5px;
  padding-top: 10px;
  border-top: 1px solid #e9ecef;
  font-weight: 700;
  font-size: 16px;
  color: var(--text-color);
}

.bottom-checkout {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 20px;
  gap: 15px;
}

.bottom-total {
  font-size: 18px;
  font-weight: bold;
}

.submit-btn {
  background: #eb4034; /* tugmalarni qizilga moslash */
  color: white;
  border: none;
  padding: 14px 24px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 16px;
  flex: 1;
}

.submit-btn:disabled {
  background: #adb5bd;
}
</style>
