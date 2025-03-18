<template>
  <q-page class="flex flex-center">
    <div class="intercom-container">
      <h2>Домофон</h2>
      <div class="button-group">
        <q-btn 
          v-for="number in buttons" 
          :key="number" 
          :label="number"
          class="" 
          :class="{ 'active-button': selectedButton === number }" 
          @click="selectButton(number)" 
          :disabled="isCalling"
       
        />
      </div>
      <q-btn
        label="Сбросить звонок"
        color="red"
        @click="abortCall(selectedButton)"
        :disabled="!isCalling"
    
      />
      <q-btn label="Вызов" color="primary" @click="callApartment(selectedButton, ['user999'])" :disabled="isCalling" />
      {{ data }}
    </div>
    <CallRoom v-if="isCalling" :hash-str="hashStr"/>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';
import CallRoom from 'src/modules/CallRoom/pages/CallRoom.vue';
import { API_SERVER } from 'src/constants/common';
import {
    useCurrentUser
} from 'src/composables/useCurrentUser';
  export default defineComponent({
    name: 'SettingDevicePage',
    components: {
      CallRoom
    },
    setup() {
      const selectedButton = ref(null);
     const  selectButton = (number) => {
      selectedButton.value = number;
      console.log(`Выбрана квартира: ${number}`);
    }
 

    const socket = ref(null);
    const message = ref('');
    const userId = 'domophone1'; // Уникальный ID домофона
    const apartmentNumber = null; // Домофону не нужен номер квартиры
    const role = 'domophone';
    const {
      accessToken
        } = useCurrentUser();
    const serverAddress = `wss://${API_SERVER}ws?key=${accessToken.value}&user_id=${userId}&role=${role}`;
    const isCalling = ref(false);
    const hashStr = ref('');
    const connectWebSocket = () => {
      console.log(accessToken.value)
      console.log(serverAddress)
      socket.value = new WebSocket(serverAddress);

      socket.value.onopen = () => {
        console.log('Подключено к WebSocket серверу');
        socket.value.send('Клиент подключен');
      };

      socket.value.onmessage = (event) => {
        message.value = event.data;
        console.log('Сообщение от сервера:', event.data);
        if (event.data.includes('завершен') || event.data.includes('прерван')) {
          isCalling.value = false; // Сброс статуса при завершении или прерывании звонка
        }
        // 
        const data = JSON.parse(event.data);
                if (data.type === 'call_started') {
                  console.log(`Звонок начался с кв. ${data.apartment}`);
                  isCalling.value = true;
                  console.log(isCalling.value)
                } 
                if (data.type === 'call_ended' || data.type === 'call_aborted') {
                  console.log(`Звонок начался с кв. ${data.apartment}`);
                  isCalling.value = false;
                } 
      };

      socket.value.onclose = () => {
        console.log('Соединение с WebSocket сервером закрыто');
      };

      socket.value.onerror = (error) => {
        console.error('Ошибка WebSocket:', error);
      };
    };

    const disconnectWebSocket = () => {
      if (socket.value) {
        socket.value.close();
      }
    };

    const callApartment = async (apartmentNumber, residentIds) => {
      hashStr.value = generateRandomString(7);
      isCalling.value = true; // Устанавливаем статус звонка
      try {
        const response = await axios.get(`https://${API_SERVER}call/${apartmentNumber}/${hashStr.value}?resident_ids=${residentIds.join(',')}`);;
        const data = response.data;
        message.value = data.message;
        console.log(data.message);
      } catch (error) {
        console.error('Ошибка при вызове:', error);
        message.value = 'Ошибка при вызове.';
        isCalling.value = false; // Сброс статуса при ошибке
      }
    };

    const abortCall = async (apartmentNumber) => {
      try {
        const response = await axios.get(`https://${API_SERVER}abort_call/${apartmentNumber}`);
        const data = response.data;
        message.value = data.message;
        console.log(data.message);
        isCalling.value = false; // Сброс статуса после сброса звонка
      } catch (error) {
        console.error('Ошибка при сбросе:', error);
        message.value = 'Ошибка при сбросе.';
      }
    };

    const generateRandomString = (length)  => {
    const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';

    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters[randomIndex];
    }

    return result;
}

    onMounted(() => {
      console.log(API_SERVER)
      connectWebSocket();
    });

    onBeforeUnmount(() => {
      disconnectWebSocket();
      
    });

      return {
      buttons: [1, 2, 3, 5, 6, 7, 8, 9, 10],
      selectButton,
      selectedButton,
      callApartment,
      abortCall,
      isCalling,
      hashStr
      };
    },
  });
</script>

<style scoped>
.intercom-container {
  text-align: center;
}

.button-group {
  margin: 20px 0;
}

.button-group q-btn {
  margin: 5px;
}

/* Стили для активной кнопки */
.active-button {
  background-color: #1976D2; /* Цвет фона для активной кнопки */
  color: white; /* Цвет текста для активной кнопки */
  border: 2px solid white; /* Обводка для активной кнопки */
}
</style>
