<template>
<div class="mt-base-10">
    <div>

       <div class="flex justify-center">
         <div class="setting-container">
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
                <s-btn :disable="currentIntercom" @click="onSubmit">Запомнить на этом устройстве</s-btn>
            </div>

        </div>
       </div>
        <div class="flex justify-center">
            <div class="flex mt-base-15">
            <q-toggle
                v-model="adminSideBarFlag"
                color="primary"
                keep-color
                @update:model-value="saveAdminSidebarFlag"
            />
            <div class="text-toogle">Разрешить исп. боковой панели</div>
        </div>
        </div>
    </div>
 <!-- <div class="flex justify-center">
            <div v-if="currentIntercom" class="mt-base-15 setting-container">
            Сейчас есть устройство:<br>
            {{ currentIntercom   }}
        </div>
        </div> -->
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
    useNotifications
} from 'src/composables/useNotifications';
import {
    useAppStore
} from 'stores/app.store';
import {
    useSelectBackend
} from 'src/composables/useSelectBackend';
import SSelectBackend from 'src/components/backend/SSelectBackend.vue';
import {
    useServiceFilters
} from '../composables/useFilters';
import {
    storeToRefs
} from 'pinia';

export default defineComponent({
    name: 'ServiceIntercom',
    components: {
        SSelectBackend,
    },
    setup() {
        const {
            getIntercom,
            getHouse,
            getEntry,
        } = useSelectBackend();
        const {
            filterParams,
        } = useServiceFilters();

        const appStore = useAppStore();
        const $notify = useNotifications();
        const adminSideBarFlag = computed(() => appStore.getAdminBar)
        const collapseSideBarFlag = computed(() => appStore.getCollapseSidebar)
        const currentHome = ref(null);
        const currentEntry = ref(null);
        const currentIntercom = ref(null);

        const saveAdminSidebarFlag = () => {
            if (collapseSideBarFlag.value == true && collapseSideBarFlag.value == true) {
                appStore.setCollapseSidebar(false)
            }
            appStore.setAdminBar(!adminSideBarFlag.value)
        }
        const onSubmit = () => {
            appStore.setIntercomData(currentIntercom.value);
            window.location.reload();
        }
         const {
            intercomData,
        } = storeToRefs(appStore)
        onMounted(() => {
            currentIntercom.value = intercomData.value;
        })
        return {
            onSubmit,
            saveAdminSidebarFlag,
            adminSideBarFlag,
            getHouse,
            getIntercom,
            filterParams,
            currentHome,
            currentIntercom,
            currentEntry,
            getEntry,
            appStore,
        };
    },
});
</script>
