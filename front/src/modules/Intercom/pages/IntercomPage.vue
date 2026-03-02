<template>
<q-page class="">
    <ServiceIntercom v-if="serviceView" @back="closeSettings" />
    <div class="intercom-container flex justify-center mt-base-10" v-else>
        <div class="left-area">
            <div class="video">
                <div class="block-video flex justify-center items-center">
                    <div v-if="!isCallingVideo">
                        <video autoplay muted playsinline loop class="videosize">
                            <source src="video/video.mp4" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                    </div>
                    <div v-else>

                        <iframe class="test22" :src="VIDEO_SERVER + hashStr" allow="camera;microphone;fullscreen;display-capture;screen-wake-lock">
                        </iframe>
                    </div>

                </div>
            </div>
            <div class="button-group">
                <q-btn
                    v-if="isCalling"
                    icon="phone_disabled"
                    :disabled="!isCallingVideo"
                    @click="abortCall"
                    label="Сброс"
                    class="call-end-btn"
                />
                <q-btn
                    v-else
                    class="call-end-btn"
                    @click="selectedNumbers = selectedNumbers.slice(0, -1)"
                    icon="backspace"
                    label="Удалить"
                    :disabled="!selectedNumbers.length > 0"
                />
            </div>
        </div>
        <div class="right-area flex flex-col">
            <div class="result">
                <div class="result-window flex justify-center items-center">
                    <div v-if="!waitAnswer" class="flex">
                        <div class="result-window-text" v-if="selectedNumbers.length <= 3">{{ selectedNumbers }}</div>
                        <div class="result-window-text" v-else>
                            {{ '*'.repeat(selectedNumbers.length) }}
                        </div>

                    </div>
                    <div v-if="waitAnswer" class=" wait-answer-text">
                        Идет звонок...
                    </div>
                </div>
            </div>
            <div class="number-pad">
                <div
                    class="number-row"
                    v-for="(row, rowIndex) in numberPadRows"
                    :key="rowIndex"
                >
                    <q-btn
                        v-for="number in row"
                        :key="number"
                        :label="number"
                        class="number-button"
                        :class="{ 'active-button': selectedButton === number }"
                        @click="selectButton(number)"
                        :disabled="isCalling"
                    />
                </div>
            </div>
            <div class="entry">
                <q-btn
                    v-if="selectedNumbers.length > 3"
                    icon="logout"
                    label="ВОЙТИ"
                    class="entry-btn"
                    @click="serviceOrEntry"
                />
                <q-btn
                    v-else
                    :disabled="isCalling || !selectedNumbers.length > 0"
                    @click="callApartment(selectedNumbers, ['user999'])"
                    icon="phone"
                    label="Вызов"
                    class="entry-btn"
                />
            </div>
        </div>
    </div>
    <q-btn @click="connectWebSocket">КОН</q-btn>
    <!-- <div v-if="techData"> {{ techData }}</div> -->
</q-page>
</template>

<script>
import {
    defineComponent,
    ref,
    onMounted,
    onBeforeUnmount,
    computed
} from 'vue';
import axios from 'axios';
// import CallRoom from 'src/modules/CallRoom/pages/CallRoom.vue';
import ServiceIntercom from '../components/ServiceIntercom.vue';
import {
    API_SERVER,
    WSS_SERVER
} from 'src/constants/common';
import {
    useCurrentUser
} from 'src/composables/useCurrentUser';
import {
    useTimeout
} from 'src/composables/useTimeout';
import {
    useNotifications
} from 'src/composables/useNotifications';
import {
    useList
} from '../composables/useMegaKostil';
import {
    VIDEO_SERVER
} from 'src/constants/common';
import {
    useAppStore
} from 'src/stores/app.store';
import IntercomCallApi from 'src/backend/api/classes/IntercomCallClass';
import {
    makeRequest
} from 'src/composables/useRequest';

export default defineComponent({
    name: 'IntercomPage',
    components: {
        // CallRoom
        ServiceIntercom
    },
    setup() {
        const {
            openLock
        } = useList();
        const selectedButton = ref(null);
        const selectedNumbers = ref('');
        const $notify = useNotifications();
        const $app = useAppStore();
        const techData = computed(() => $app.getIntercomData);
        // const router = useRouter();

        const selectButton = (number) => {
            selectedButton.value = number;
            if (selectedNumbers.value.length > 4) {
                return
            }
            selectedNumbers.value = selectedNumbers.value + number
        }
        const flat_id = ref(null);
        const socket = ref(null);
        const message = ref('');
        const role = 'intercom';
        const {
            accessToken
        } = useCurrentUser();
        const serverAddress = `${WSS_SERVER}?key=${accessToken.value}&user_id=${techData.value ? techData.value.tech_name : 'None'}&role=${role}`;
        const isCalling = ref(false);
        const isCallingVideo = ref(false);
        const hashStr = ref('');
        const waitAnswer = ref(false);
        const reconnectInterval = 3000;
        let reconnectTimer = null;

        // PING interval
        let pingInterval = null;

        const connectWebSocket = () => {
            console.log(serverAddress)
            socket.value = new WebSocket(serverAddress);

            if (techData.value) {
                socket.value.onopen = () => {
                    console.log('Подключено к WebSocket серверу');
                    socket.value.send('Клиент подключен');
                    clearInterval(reconnectTimer);

                    // Start PING interval after successful connection
                    pingInterval = setInterval(() => {
                        if (socket.value && socket.value.readyState === WebSocket.OPEN) {
                              socket.value.send(JSON.stringify({
                                'type':'ping', 
                                'battery_level': '100',
                                'battery_temp': '28'
                            }))
                            // socket.value.send('ping')
                            // console.log('Отправлен PING');
                        } else {
                            console.log('WebSocket не готов, PING не отправлен');
                            clearInterval(pingInterval);
                        }
                    }, 4000);
                };
            } else {
                $notify.error('Произведите настройку')
            }

            socket.value.onmessage = (event) => {
                message.value = event.data;
                // console.log('Сообщение от сервера:', event.data);
                if (event.data.includes('завершен') || event.data.includes('прерван')) {
                    start();
                    isCallingVideo.value = false;
                }
                // 
                const data = JSON.parse(event.data);
                if (data.type === 'call_started') {
                    console.log(`Звонок начался с кв. ${data.apartment} c id - ${data.flat_id}`);
                    flat_id.value = data.flat_id;
                    isCalling.value = true;
                    isCallingVideo.value = true;
                    waitAnswer.value = true;
                    console.log(waitAnswer.value)
                }
                if (data.type === 'call_answered') {
                    waitAnswer.value = false;
                }
                if (data.type === 'call_ended' || data.type === 'call_aborted') {
                    console.log(`Звонок закончился ${data.apartment}`);
                    selectedNumbers.value = '';
                    start(); // Задержка на клаву
                    isCallingVideo.value = false;
                    waitAnswer.value = false;

                }
            };

            socket.value.onclose = () => {
                console.log('Соединение с WebSocket сервером закрыто');
                clearInterval(pingInterval); // Stop PING interval on close
                reconnect();
            };

            socket.value.onerror = (error) => {
                console.error('Ошибка WebSocket:', error);
                clearInterval(pingInterval);
                reconnect();
            };
        };
        const reconnect = () => {
            if (reconnectTimer) {
                clearInterval(reconnectTimer);
                reconnectTimer = null;
            }

            reconnectTimer = setTimeout(() => {
                console.log('Попытка переподключения к WebSocket серверу...');
                connectWebSocket();
                reconnectTimer = null;
            }, reconnectInterval);
        };
        const disconnectWebSocket = () => {
            if (socket.value) {
                socket.value.close();
            }
            clearInterval(reconnectTimer);
            clearInterval(pingInterval); // Stop PING interval on manual disconnect
        };

        const callApartment = async (apartmentNumber, residentIds) => {

            console.log(techData.value.entry.flat_first)
            console.log(Number(apartmentNumber))
            if (Number(apartmentNumber) < techData.value.entry.flat_first || Number(apartmentNumber) > techData.value.entry.flat_last) {
                $notify.warning('Значение кв не входит в диапозон');
                return
            }

            hashStr.value = generateRandomString(7);
            isCalling.value = true;
            isCallingVideo.value = true;

            const callData = ref({
                apartment_number: Number(apartmentNumber),
                hash_room: hashStr.value,
                indentifier: techData.value ? techData.value.tech_name : 'None',
                blockDevice: computed(() => $app.getStownDevice),
                house_id: 13,
            })

            try {

                const response = await makeRequest(async () =>
                    IntercomCallApi.call(callData.value));

                const data = response;

                message.value = data.message;
                console.log(data.message);
            } catch (error) {
                if (error.response ?.status == 418) $notify.error(error.response.data.detail);
                console.error('Ошибка при вызове:', error);
                disconnectWebSocket();
                reconnect();
                start(); // Задержка на клаву
                isCallingVideo.value = false;
            }
        };

        const abortCall = async () => {
            try {
                const response = await axios.get(`${API_SERVER}api/abort_call/${flat_id.value}`);
                const data = response.data;
                message.value = data.message;
                console.log(data.message);
                isCallingVideo.value = false;
                start(); //Задержка на клаву
            } catch (error) {
                console.error('Ошибка при сбросе:', error);
                message.value = 'Ошибка при сбросе.';
            }
        };

        const generateRandomString = (length) => {
            const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
            let result = '';

            for (let i = 0; i < length; i++) {
                const randomIndex = Math.floor(Math.random() * characters.length);
                result += characters[randomIndex];
            }

            return result;
        }
        const numberPadRows = computed(() => {
            const rows = [];
            rows.push(buttons.value.slice(0, 5));
            rows.push(buttons.value.slice(5, 10));
            return rows;
        });
        const deleteLast = () => {
            selectedNumbers.value = selectedNumbers.value.slice(0, -1)
            console.log(selectedNumbers.value)
        }
        const buttons = ref(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']);

        const {
            start
        } = useTimeout(() => {
            isCalling.value = false;
        }, 2500);

        const serviceView = ref(false);
        const serviceOrEntry = () => {
            if (selectedNumbers.value == '9698') {
                serviceView.value = !serviceView.value
            } else {
                openLock(selectedNumbers.value)
                selectedNumbers.value = ''
            }

        }
        const closeSettings = () => {
            serviceView.value = !serviceView.value;
            selectedNumbers.value = ''
        }
        onMounted(() => {
        // connectWebSocket();
        });

        onBeforeUnmount(() => {
            disconnectWebSocket();
        });

        return {
            buttons,
            selectButton,
            selectedButton,
            callApartment,
            abortCall,
            isCalling,
            hashStr,
            numberPadRows,
            selectedNumbers,
            deleteLast,
            disconnectWebSocket,
            connectWebSocket,
            waitAnswer,
            isCallingVideo,
            VIDEO_SERVER,
            serviceOrEntry,
            serviceView,
            techData,
            closeSettings
        };
    },
});
</script>

<style scoped>
.test22 {
    width: 750px !important;
    height: 500px !important;
    border-radius: 15px;
}

.intercom-container {}

.left-area {
    margin-right: 5px;
}

.right-area {
    display: flex;

    flex-direction: column;

    max-width: 600px;
}

.block-video {
    width: 750px;
    height: 500px;
    border-radius: 10px;
    background-color: gray;
}

.button-group {
    margin-top: 5px;
    display: flex;
    justify-content: space-between;
}

.call-end-btn {
    width: 100%;
    /* height: 101px; */
    font-size: 35px;
    background: radial-gradient(ellipse farthest-corner at right bottom, #FEDB37 0%, #FDB931 8%, #9f7928 30%, #8A6E2F 40%, transparent 80%),
        radial-gradient(ellipse farthest-corner at left top, #FFFFFF 0%, #FFFFAC 8%, #D1B464 25%, #5d4a1f 62.5%, #5d4a1f 100%);
}

.call-start-btn {
    width: 49%;
    height: 151px;
    font-size: 35px;
}

.result-window {
    width: 421px;
    height: 155px;
    border: 2px solid #D6B06F;
    border-radius: 10px;
    font-size: 1.2rem;
}

.number-pad {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.number-row {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.number-button {
    width: 75px;
    height: 75px;
    margin: 1px;
    font-size: 60px;
    padding: 10px;
    border-radius: 5px;
    min-width: auto;
    margin-right: 10px;
    background: radial-gradient(ellipse farthest-corner at right bottom, #FEDB37 0%, #FDB931 8%, #9f7928 30%, #8A6E2F 40%, transparent 80%),
        radial-gradient(ellipse farthest-corner at left top, #FFFFFF 0%, #FFFFAC 8%, #D1B464 25%, #5d4a1f 62.5%, #5d4a1f 100%);
}

.active-button {
    background-color: #1976D2;
    color: white;
    border: 2px solid white;
}

.entry {}

.entry-btn {
    width: 100%;
    /* height: 151px; */
    font-size: 35px;
    /* Увеличение размера шрифта */
    background: radial-gradient(ellipse farthest-corner at right bottom, #FEDB37 0%, #FDB931 8%, #9f7928 30%, #8A6E2F 40%, transparent 80%),
        radial-gradient(ellipse farthest-corner at left top, #FFFFFF 0%, #FFFFAC 8%, #D1B464 25%, #5d4a1f 62.5%, #5d4a1f 100%);
}

.result-window-text {
    font-size: 4rem;
}

.wait-answer-text {
    font-size: 35px;
    background: linear-gradient(90deg, #cab01b, #dbce10, #c6b38e, #c2ab28);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: goldShine 5s linear infinite;
    font-weight: bold;
}

@keyframes goldShine {
    0% {
        background-position: 0% 50%;
    }

    100% {
        background-position: 100% 50%;
    }
}

video {
    width: 100%;
    /*  Заполняет контейнер по ширине */
    height: auto;
    /*  Высота автоматически масштабируется, сохраняя пропорции */
    object-fit: cover;
    /* или contain, см. объяснение ниже */

}

.videosize {
    border-radius: 10px;

    width: 100%;
    height: 500px;
}

.qwerrty {
    width: 750px !important;
    height: 500px !important;
}
</style>
