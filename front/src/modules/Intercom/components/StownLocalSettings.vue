<template>
<div class="mt-base-10">
    <div class=" ">
        <div class="flex justify-center">192.168.0.1</div>
        <div class=" flex justify-center ">

            <div class="flex">
                <q-btn
                    flat
                    round
                    color="primary"
                    icon="content_copy"
                    @click="copyText"
                />
                <div class="text-toogle">Нажмите чтобы скопировать текст выше</div>
            </div>
        </div>
        <div class="flex justify-center ">
            <div class="setting-container">
                <s-input
                    class="mt-base-15"
                    label="URL для запроса к лок. устройствам"
                    v-model="urlLocal"
                />
                <div class="flex justify-center mt-base-15">
                    <s-btn
                        :disable="!urlLocal"
                        class="full-width"
                        @click="saveUrl"
                    >Запомнить URL</s-btn>
                </div>
            </div>
        </div>
        <div class="flex justify-center mt-base-15">
            <s-select
                v-model="lockIdLocal"
                :options="[1,2,3,4,5, 6, 7, 8]"
                option-label="label"
                option-value="value"
                label="Выберите ID устройства"
                @update:model-value="saveLockId"
                map-options
                class="setting-container"
            />
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
export default defineComponent({
    name: 'ServiceIntercom',
    components: {

    },
    setup() {
        const appStore = useAppStore();
        const $notify = useNotifications();
        const urlLocal = ref('');
        const lockIdLocal = ref(null);
        const {
            localUrlControlBoard,
            localIdLock
        } = storeToRefs(appStore);

        const saveUrl = () => {
            appStore.setlocalUrlControlBoard(urlLocal.value)
            $notify.success('URL запомнил')

        }
        const saveLockId = () => {
            appStore.setLocalIdLock(lockIdLocal.value)
            $notify.success('ID изменен')

        }
        onMounted(() => {
            urlLocal.value = localUrlControlBoard.value;
            lockIdLocal.value = localIdLock.value;
        })
        return {
            saveUrl,
            lockIdLocal,
            urlLocal,
            saveLockId
        }
    },
});
</script>
