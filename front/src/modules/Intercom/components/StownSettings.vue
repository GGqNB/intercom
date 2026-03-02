<template>
<div class="mt-base-10">
    <div>
        <div class="flex justify-center mt-base-15">
            <s-select-backend
                v-model="deviceStownData"
                :getter="getStownDevices"
                option-label="name"
                value-object
                label="Выберите устройство STOWN"
                class="setting-container"
                search-filter="name"
            />

        </div>
        <div class="mt-base-15">
            <!-- <div v-if="currentIntercom" class="mt-base-15"> -->

        </div>

        <div class="flex justify-center mt-base-15 ">
            <s-btn :disable="!deviceStownData" class="setting-container" @click="onSubmit">Запомнить устройство</s-btn>
        </div>

        <div class="flex justify-center">
            <div v-if="deviceStownData" class="mt-base-15 setting-container">
            Сейчас есть устройство:<br>
            {{ deviceStownData   }}
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
    useNotifications
} from 'src/composables/useNotifications';
import {
    useAppStore
} from 'stores/app.store';
import {
    storeToRefs
} from 'pinia';
import {
    useSelectBackend
} from 'src/composables/useSelectBackend';
import SSelectBackend from 'src/components/backend/SSelectBackend.vue';
export default defineComponent({
    name: 'ServiceIntercom',
    components: {
        SSelectBackend
    },
    setup() {
        const appStore = useAppStore();
        const $notify = useNotifications();
        const deviceStownData = ref(null);
        const {
            getStownDevices
        } = useSelectBackend();
        const {
            stownDevice,
        } = storeToRefs(appStore);

        const onSubmit = () => {
            appStore.setStownDevice(deviceStownData.value)
            $notify.success('STOWN устройство сохранено')

        }
        onMounted(() => {
            deviceStownData.value = stownDevice.value;
        })
        return {
            onSubmit,
            getStownDevices,
            deviceStownData

        }
    },
});
</script>
