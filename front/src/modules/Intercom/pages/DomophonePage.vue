<template>
<q-page class="">
    <div class="intercom-container flex justify-center mt-base-10">
        <div class="left-area">
            <div class="video">
                <div class="block-video flex justify-center items-center">
                    <q-img
                        v-if="!isCalling"
                        src="icons/logo.svg"
                       width="260px"
                        height="350px"
                    />
                    <CallRoom
                        v-if="isCalling"
                        :hash-str="hashStr"
                        :is-intercom="true"
                    />
                </div>
            </div>
            <div class="button-group">
                <q-btn
                    v-if="isCalling"
                    icon="phone_disabled"
                    @click="abortCall(selectedNumbers)"
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
                        <div class="result-window-text">{{ selectedNumbers }}</div>

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
import CallRoom from 'src/modules/CallRoom/pages/CallRoom.vue';
import {
    API_SERVER
} from 'src/constants/common';
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
        const selectedNumbers = ref('');
        const selectButton = (number) => {
            selectedButton.value = number;
            if(selectedNumbers.value.length > 4){
                return
            }
            selectedNumbers.value = selectedNumbers.value + number
            console.log(`Выбрана квартира: ${number}`);
        }

        const socket = ref(null);
        const message = ref('');
        const userId = 'domophone1';
        const apartmentNumber = null;
        const role = 'domophone';
        const {
            accessToken
        } = useCurrentUser();
        const serverAddress = `wss://${API_SERVER}ws?key=${accessToken.value}&user_id=${userId}&role=${role}`;
        const isCalling = ref(false);
        const hashStr = ref('');
        const waitAnswer = ref(false);
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
                message.value = event.data;
                console.log('Сообщение от сервера:', event.data);
                if (event.data.includes('завершен') || event.data.includes('прерван')) {
                    isCalling.value = false;
                }
                // 
                const data = JSON.parse(event.data);
                if (data.type === 'call_started') {
                    console.log(`Звонок начался с кв. ${data.apartment}`);
                    isCalling.value = true;
                    waitAnswer.value = true;
                    console.log(waitAnswer.value)
                }
                if (data.type === 'call_answered') {
                    waitAnswer.value = false;
                }
                if (data.type === 'call_ended' || data.type === 'call_aborted') {
                    console.log(`Звонок закончился ${data.apartment}`);
                    selectedNumbers.value = '';
                    isCalling.value = false;
                    waitAnswer.value = false;

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
        };

        const callApartment = async (apartmentNumber, residentIds) => {
            hashStr.value = generateRandomString(7);
            isCalling.value = true;
            try {
                const response = await axios.get(`https://${API_SERVER}api/call/${apartmentNumber}/${hashStr.value}?resident_ids=${residentIds.join(',')}`);;
                const data = response.data;
                message.value = data.message;
                console.log(data.message);
            } catch (error) {
                console.error('Ошибка при вызове:', error);
                message.value = 'Ошибка при вызове.';
                isCalling.value = false;
            }
        };

        const abortCall = async (apartmentNumber) => {
            try {
                const response = await axios.get(`https://${API_SERVER}api/abort_call/${apartmentNumber}`);
                const data = response.data;
                message.value = data.message;
                console.log(data.message);
                isCalling.value = false;
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
        onMounted(() => {
            connectWebSocket();
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
            waitAnswer
        };
    },
});
</script>

<style scoped>
.intercom-container {}

.left-area {
    margin-right: 5px;
}

.right-area {
    display: flex;

    flex-direction: column;

    max-width: 1100px;
}

.block-video {
    width: 1135px;
    height: 851px;
    border-radius: 10px;
    background-color: gray;
}

.button-group {
    margin: 20px 0;
    display: flex;
    justify-content: space-between;
}

.call-end-btn {
    width: 100%;
    height: 151px;
    font-size: 60px;
    background: radial-gradient(ellipse farthest-corner at right bottom, #FEDB37 0%, #FDB931 8%, #9f7928 30%, #8A6E2F 40%, transparent 80%),
        radial-gradient(ellipse farthest-corner at left top, #FFFFFF 0%, #FFFFAC 8%, #D1B464 25%, #5d4a1f 62.5%, #5d4a1f 100%);
}

.call-start-btn {
    width: 49%;
    height: 151px;
    font-size: 80px;
}

.result-window {
    width: 837px;
    height: 284px;
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
    width: 157px;
    height: 270px;
    margin: 2px;
    font-size: 100px;
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
    height: 151px;
    font-size: 60px;
    /* Увеличение размера шрифта */
    background: radial-gradient(ellipse farthest-corner at right bottom, #FEDB37 0%, #FDB931 8%, #9f7928 30%, #8A6E2F 40%, transparent 80%),
        radial-gradient(ellipse farthest-corner at left top, #FFFFFF 0%, #FFFFAC 8%, #D1B464 25%, #5d4a1f 62.5%, #5d4a1f 100%);
}

.result-window-text {
    font-size: 4rem;
}
.wait-answer-text {
  font-size: 65px;
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


</style>
