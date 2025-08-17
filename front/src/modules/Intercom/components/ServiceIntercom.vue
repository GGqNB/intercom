<template>
<div class="intercom-container flex justify-center mt-base-10">
    <div>
        <div>
            <q-btn color="blue" icon="arrow_back"></q-btn>
        </div>
        <div>
            Введите учетные данные для админ-панели<br>(Пока не используется)
        </div>
        <div>
            <s-input
                class="mt-base-15"
                label="Логин"
                disable
            />
            <s-input
                class="mt-base-15"
                label="Пароль"
                disable
            />

        </div>
        <div class="flex justify-center mt-base-15">
            <s-btn disable>Вход</s-btn>
        </div>
        <div>
            <div class="mt-base-15">Идентификация домофона</div>
            <div>
                <s-select-backend
                    v-model="currentHome"
                    :getter="getHouse"
                    option-label="geo_adress"
                    option-value="id"
                    label="Выбор дома"
                    class=" "
                    search-filter="geo_adress"
                />
            </div>

             <div class="mt-base-15" v-if="currentHome">
                <s-select-backend
                    :disable="!currentHome"
                    v-model="currentEntry"
                    :getter="getEntry"
                    option-label="name"
                    option-value="id"
                    label="Выберите подъезд/вход"
                    class=" "
                    search-filter="name"
                    :params="{house_id : currentHome}"
                />
            </div>

              <div class="mt-base-15" v-if="currentEntry">
                <s-select-backend
                    :disable="!currentEntry"
                    v-model="currentIntercom"
                    :getter="getIntercom"
                    option-label="name"
                    value-object
                    label="Выберите домофон"
                    class=" "
                    search-filter="name"
                    :params="{entry_id : currentEntry}"
                />
                
            </div>
            <div v-if="currentIntercom" class="mt-base-15">
                <div>Выбран: {{ currentIntercom.name }}</div>
                <div>С кв: {{ currentIntercom.entry.flat_first }}</div>
                <div>С кв: {{ currentIntercom.entry.flat_last }}</div>
            </div>
            <div class="flex justify-center mt-base-15">
                  <s-btn :disable="currentIntercom" @click="$emit('apply', currentIntercom )">Запомнить на этом устройстве</s-btn>
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
    useCurrentUser
} from 'src/composables/useCurrentUser';
import {
    useSelectBackend
} from 'src/composables/useSelectBackend';
import SSelectBackend from 'src/components/backend/SSelectBackend.vue';
import {
    useServiceFilters
} from '../composables/useFilters';
export default defineComponent({
    name: 'ServiceIntercom',
    components: {
        SSelectBackend
    },
    setup() {
        const {
            getIntercom,
            getHouse, 
            getEntry
        } = useSelectBackend();
        const {
            filterParams,
            sanitizeQueryFilterParams,
            defaultFilterParams
        } = useServiceFilters();
        const currentHome = ref(null);
        const currentEntry = ref(null);
        const currentIntercom = ref(null);
        return {
            getHouse,
            getIntercom,
            filterParams,
            currentHome,
            currentIntercom,
            currentEntry,
            getEntry
        };
    },
});
</script>
