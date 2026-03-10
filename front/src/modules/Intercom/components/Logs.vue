<template>
<div class="mt-base-10" v-if="logsData">
    <div class=" ">
        <div class="flex justify-center">Логи</div>
        <div class="flex justify-center"><s-btn @click="init" label="Обновить"/></div>
        <div class="flex justify-center ">
          <div>
              <div
                class="setting-container"
                v-for="log in logsData"
                :key="log"
            >
                <q-card class="my-card mt-base-15" >
                    <q-card-section v-if="log.intercom">
                        <div class="text-h6">{{ log.intercom.id }}. {{ log.tech_name }}</div>
                        <div class="text-subtitle2">Вход: {{ log.intercom.entry.name }}</div>
                        <!-- Выкидывать еще из данных нормально дом -->
                        <div class="text-subtitle2">
                            Дом: {{ log.intercom.entry.house_id == 13 ? 'Объездная 57А': log.intercom.entry.house_id == 15 ? 'Объездная 57':'неизвестный дом'}}
                        </div>
                        <div class="text-subtitle2">Название: {{ log.intercom.name }}</div>
                        <div class="text-subtitle2">Температура: {{ log.battery_temp ? log.battery_temp : '' }}°C</div>
                        <div class="text-subtitle2">Заряд: {{ log.battery_level ? log.battery_level : '' }}%</div>
                    </q-card-section>
                     <q-card-section v-else>
                        <div class="text-h6">Слетел пресет</div>
                        <div class="text-subtitle2" color="orange">Нету информации про домофон</div>
                        <div class="text-subtitle2" color="orange">TECH-NAME:{{ log.tech_name }}</div>
                    </q-card-section>
                    <q-separator />
                    <q-card-section class="q-pt-none">
                        <div class="text-subtitle2">Время последнего сообщения:<br> {{ formatDate(log.last_update) }} - {{timeAgo(log.last_update)}}</div>
                    </q-card-section>
                    <q-card-section class="q-pt-none">
                        <div class="text-subtitle2">Время первого сообщения:<br> {{ formatDate(log.date_start) }} -  {{timeAgo(log.date_start)}}</div> 
                    </q-card-section>
                </q-card>
            </div>
          </div>
        </div>

    </div>
</div>
</template>

<script>
import {
    defineComponent,
    ref,
    onMounted,
    onBeforeUnmount,
    computed
} from 'vue';
import {
    makeRequest
} from 'src/composables/useRequest';
import LogsApi from 'src/backend/api/classes/LogsApiClass';
import { formatDate, timeAgo } from 'src/utils/datetime';
export default defineComponent({
    name: 'ServiceIntercom',
    components: {

    },
    setup() {
        const urlLocal = ref('');
        const lockIdLocal = ref(null);;
        const logsData = ref(null);
        const init = async () => {
             logsData.value = null;
            const response = await makeRequest(async () =>
                LogsApi.list());
            logsData.value = response.data;
        }
      
        onMounted(() => {
            init()
        })
        return {
            lockIdLocal,
            urlLocal,
            logsData,
            formatDate,
            init,
            timeAgo
        }
    },
});
</script>
