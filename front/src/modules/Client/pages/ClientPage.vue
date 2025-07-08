<template>
<q-page class="flex flex-center">
    <div class="intercom-container">
        <h3>2я кв</h3>

        <q-btn @click="disconnectWebSocket">123</q-btn>
        <transition enter-active-class="shake-enter-active" leave-active-class="fade-leave-active">
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
        <!-- <CallRoom
            v-if="videoFlag"
            :hash-str="hashStr"
            :is-intercom="true"
        /> -->
        <div v-if="videoFlag">
            <iframe class="qwerrty" :src="'https://intercom-stown.edgelive.ru/call/?roomId=serv1'+hashStr" allow="camera;microphone;fullscreen;display-capture;screen-wake-lock">
            </iframe>
        </div>
    </div>
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
// import CallRoom from 'src/modules/CallRoom/pages/CallRoom.vue';
import {
    API_SERVER
} from 'src/constants/common';

import {
    useCurrentUser
} from 'src/composables/useCurrentUser';
export default defineComponent({
    name: 'SettingDevicePage',
    components: {
        // CallRoom
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
        const serverAddress = `wss://${API_SERVER}ws?key=${accessToken.value}&user_id=${userId}&apartment_number=${apartmentNumber.value}&role=${role}`;

        const isCalling = ref(false);
        const isAnswer = ref(false);
        const videoFlag = ref(false);
        const hashStr = ref('');
        const reconnectInterval = 3000;
        let reconnectTimer = null;
        const connectWebSocket = () => {

            socket.value = new WebSocket(serverAddress);

            socket.value.onopen = () => {
                console.log('Подключено к WebSocket серверу');
                socket.value.send('Клиент подключен');
                clearInterval(reconnectTimer);
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

                if (data.type === 'abort_call' || data.type === 'call_aborted') {
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
                reconnect();
            };

            socket.value.onerror = (error) => {
                console.error('Ошибка WebSocket:', error);
                reconnect();
            };
        };

        const callApartment = async (apartmentNumber) => {
            isCalling.value = true;
            try {
                const response = await axios.get(`https://${API_SERVER}api/call/${apartmentNumber}`);;
                const data = response.data;
                message.value = data.message;
                console.log(data.message);
            } catch (error) {
                console.error('Ошибка при вызове:', error);
                message.value = 'Ошибка при вызове.';
                isCalling.value = false;
            }
        };

        const abortCall = async () => {
            try {
                const response = await axios.get(`https://${API_SERVER}api/abort_call/${apartmentNumber.value}`);
                const data = response.data;
                message.value = data.message;
                console.log(data.message);
                isCalling.value = false;
            } catch (error) {
                console.error('Ошибка при сбросе:', error);
                message.value = 'Ошибка при сбросе.';
            }
        };

        const answerCall = async () => {
            try {
                const response = await axios.get(`https://${API_SERVER}api/answer_call/${apartmentNumber.value}`);
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
        const reconnect = () => {
            if (reconnectTimer) {
                clearInterval(reconnectTimer); // Предотвращаем множественные таймеры
                reconnectTimer = null; // Сбрасываем, чтобы можно было запустить снова
            }

            reconnectTimer = setTimeout(() => {
                console.log('Попытка переподключения к WebSocket серверу...');
                connectWebSocket();
                reconnectTimer = null; // Сбрасываем после попытки подключения
            }, reconnectInterval);
        };
        const disconnectWebSocket = () => {
            if (socket.value) {
                socket.value.close();
            }
            clearInterval(reconnectTimer);
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
            hashStr,
            disconnectWebSocket
        };
    },
});
</script>

<style scoped>
.intercom-container {
    text-align: center;
    max-width: 600px;
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
</style><style lang="scss" scoped>
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

    10%,
    30%,
    50%,
    70%,
    90% {
        transform: translateX(-10px);
    }

    20%,
    40%,
    60%,
    80% {
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
.qwerrty{
    width: 750px !important;
    height: 500px !important;
}
</style>
