<template>
<q-page class="flex flex-center">
    <div class="intercom-container">
      <transition
      enter-active-class="shake-enter-active"
      leave-active-class="fade-leave-active"
    >
      <q-card
        class="my-card shake"
        :style="blockStyle"
        v-if="isCalling"
      >
        <q-card-section>
          Звонок!!!
        </q-card-section>
      </q-card>
    </transition>
        <h2>Клиент</h2>
        <div class="button-group">
           
        </div>
        <q-btn
            label="Сбросить звонок"
            color="red"
            @click="abortCall"
            :disabled="!isCalling"
        />
        <q-btn
            label="Ответ"
            color="primary"
            @click="answerCall"
            :disabled="!isAnswer"

        />
        {{ data }}
    </div>
    <CallRoom v-if="videoFlag" :hash-str="hashStr"/>
</q-page>
</template>

<script>
import {
    defineComponent,
    ref,
    onMounted,
    onBeforeUnmount
} from 'vue';
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
        const selectButton = (number) => {
            selectedButton.value = number;
            callApartment(number)
            console.log(`Выбрана квартира: ${number}`);
        }
        const callButton = () => {
            if (selectedButton.value) {
                console.log(`Вызов на квартиру: ${selectedButton.value}`);
                alert(`Вызов на квартиру: ${selectedButton.value}`);
            } else {  
                alert('Пожалуйста, выберите квартиру перед вызовом.');
            }
        }

        const socket = ref(null);
        const message = ref('');
        const userId = '002';
        const apartmentNumber = ref(2);
        const role = 'resident';
        const {
      accessToken
        } = useCurrentUser();
        const serverAddress = `ws://${API_SERVER}/ws?key=${accessToken.value}&user_id=${userId}&apartment_number=${apartmentNumber.value}&role=${role}`;
        
        const isCalling = ref(false);
        const isAnswer = ref(false);
        const videoFlag = ref(false);
        const hashStr = ref('');
        const connectWebSocket = () => {

            socket.value = new WebSocket(serverAddress);

            socket.value.onopen = () => {
                console.log('Подключено к WebSocket серверу');
                socket.value.send('Клиент подключен');
            };

            socket.value.onmessage = (event) => {
              console.log(isCalling.value)

                message.value = event.data;
                const data = JSON.parse(event.data);
                if (data.type === 'incoming_call') {
                  console.log(`Входящий звонок в квартиру ${data.apartment} от домофона!`);
                  isCalling.value = true;
                  isAnswer.value = true;
                  hashStr.value = data.hash_room;
                  console.log(hashStr.value)
                } 
                
                if (data.type === 'abort_call' || data.type ===  'call_aborted') {
                  console.log(`Сброс звонока${data.apartment} от домофона!`);
                  isCalling.value = false;
                  isAnswer.value = false;
                  videoFlag.value = false;
                  console.log(isCalling.value)
                } 

                if (data.type === 'call_ended') {
                  console.log(` не ответ${data.apartment} от домофона!`);
                  isCalling.value = false;
                  isAnswer.value = false;
                  videoFlag.value = false;

                  console.log(isCalling.value)
                } 

                if (event.data.includes('завершен') || event.data.includes('прерван')) {
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

        const callApartment = async (apartmentNumber) => {
            isCalling.value = true; // Устанавливаем статус звонка
            try {
                const response = await axios.get(`https://${API_SERVER}call/${apartmentNumber}`);;
                const data = response.data;
                message.value = data.message;
                console.log(data.message);
            } catch (error) {
                console.error('Ошибка при вызове:', error);
                message.value = 'Ошибка при вызове.';
                isCalling.value = false; // Сброс статуса при ошибке
            }
        };

        const abortCall = async () => {
            try {
                const response = await axios.get(`https://${API_SERVER}abort_call/${apartmentNumber.value}`);
                const data = response.data;
                message.value = data.message;
                console.log(data.message);
                isCalling.value = false; // Сброс статуса после сброса звонка
            } catch (error) {
                console.error('Ошибка при сбросе:', error);
                message.value = 'Ошибка при сбросе.';
            }
        };

        const answerCall = async () => {
      try {
        const response = await axios.get(`https://${API_SERVER}answer_call/${apartmentNumber.value}`);
        const data = response.data;
        message.value = data.message;
        console.log(data.message);
        isCalling.value = true;
        isAnswer.value = false;
        videoFlag.value = true;

      } catch (error) {
        console.error('Ошибка при ответе:');
        message.value = 'Ошибка при ответе.';
      }
    };


        onMounted(() => {
            connectWebSocket();

        });

        onBeforeUnmount(() => {
            disconnectWebSocket();

        });

        return {
            buttons: [1, 2, 3, 5, 6, 7, 8, 9, 10],
            selectButton,
            callButton,
            selectedButton,
            callApartment,
            abortCall,
            isCalling,
            answerCall,
            isAnswer,
            videoFlag,
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
    background-color: #1976D2;
    /* Цвет фона для активной кнопки */
    color: white;
    /* Цвет текста для активной кнопки */
    border: 2px solid white;
    /* Обводка для активной кнопки */
}
</style>
<style scoped lang="scss">
/* Дополнительные стили для карточки */
.my-card {
  width: 300px;
  margin: 20px auto;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

/* Анимация тряски */
@keyframes shakeX {
  0% {
    transform: translateX(0);
  }
  10%, 30%, 50%, 70%, 90% {
    transform: translateX(-10px);
  }
  20%, 40%, 60%, 80% {
    transform: translateX(10px);
  }
  100% {
    transform: translateX(0);
  }
}

/* Анимация исчезновения */
@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}


/* Классы для transition */
.shake-enter-active {
  animation: shakeX 1s;
}

.fade-leave-active {
  animation: fadeOut 0.5s forwards;
}

.shake {
      animation: shakeX 1s linear infinite; // infinite для постоянной анимации
    }
</style>