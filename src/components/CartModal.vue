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
const isMapOpen = ref(false)
const mapContainer = ref(null)
let ymapsInstance = null
let mapObject = null
let lastPlacemark = null

// Telefon raqamini faqat raqamlardan iborat qilish va 9 tadan oshirmaslik
const handlePhoneInput = (e) => {
  const value = e.target.value.replace(/\D/g, '')
  phone.value = value.slice(0, 9)
}

const isFormValid = computed(() => {
  return name.value.length >= 2 && phone.value.length === 9 && address.value.length >= 3
})

const openMap = () => {
  isMapOpen.value = true
  // Yandex Maps kutubxonasi yuklanganini tekshirish
  if (window.ymaps) {
    window.ymaps.ready(initMap)
  }
}

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

const closeMap = () => {
  isMapOpen.value = false
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
    total: props.total
  }
  
  emit('checkout', orderData)
}

// Modal yopilganda xaritani tozalash (ixtiyoriy)
watch(() => props.isOpen, (newVal) => {
  if (!newVal) {
    isMapOpen.value = false
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
        <h4>Ma'lumotlar:</h4>
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

        <div class="address-wrapper">
          <textarea v-model="address" placeholder="Yetkazib berish manzili"></textarea>
          <button class="map-btn" @click="openMap">
            📍 Xaritadan belgilash
          </button>
        </div>
        
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

    <!-- Yandex Map Fullscreen Modal -->
    <div v-if="isMapOpen" class="map-modal">
      <div class="map-header">
        <button class="back-btn" @click="closeMap">← Orqaga</button>
        <span>Joylashuvni belgilang</span>
        <button class="done-btn" @click="closeMap">Tayyor</button>
      </div>
      <div id="yandex-map" class="map-view"></div>
      <div class="map-hint">Markerni kerakli joyga suring</div>
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

.map-btn {
  background: #e3f2fd;
  color: #2196f3;
  border: none;
  padding: 10px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
}

.summary {
  display: flex;
  justify-content: space-between;
  font-size: 18px;
  padding: 10px 0;
  border-top: 1px solid #eee;
}

.submit-btn {
  background: #2196f3;
  color: white;
  border: none;
  padding: 16px;
  border-radius: 14px;
  font-weight: 600;
  font-size: 16px;
}

.submit-btn:disabled {
  background: #adb5bd;
}

/* Map Modal Styles */
.map-modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: white;
  z-index: 2000;
  display: flex;
  flex-direction: column;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  background: white;
}

.back-btn, .done-btn {
  background: none; border: none;
  font-weight: 600; font-size: 16px;
  color: #2196f3;
}

.map-view {
  flex: 1;
  width: 100%;
}

.map-hint {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  pointer-events: none;
}
</style>
