<template>
<div class="mt-base-10">
    <div>
        <q-tabs
            v-model="currentTab"
            align="left"
            class="text-primary"
        >
            <q-tab name="general" label="Основные" />
            <q-tab name="stown-local" label="STOWN local" />
            <q-tab name="stown" label="STOWN" />
            <q-tab name="logs" label="Логи" />
            <q-btn
                label="Назад"
                icon="arrow_back"
                @click="$emit('back')"
            />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="currentTab" animated>
            <q-tab-panel name="general">
                 <GeneralSettings/>
            </q-tab-panel>

            <q-tab-panel name="stown-local">
                <StownLocalSettings/>
            </q-tab-panel>

             <q-tab-panel name="stown">
                <StownSettings/>
            </q-tab-panel>
             <q-tab-panel name="logs">
                <Logs/>
            </q-tab-panel>
        </q-tab-panels>

    
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
import GeneralSettings from 'src/modules/Intercom/components/GeneralSettings.vue'
import StownLocalSettings from 'src/modules/Intercom/components/StownLocalSettings.vue'
import StownSettings from 'src/modules/Intercom/components/StownSettings.vue'
import Logs from 'src/modules/Intercom/components/Logs.vue'
 
export default defineComponent({
    name: 'ServiceIntercom',
    components: {
        GeneralSettings,
        StownLocalSettings,
        StownSettings,
        Logs
    },
    setup() {
        const currentTab = ref('general');
        return {
            
            currentTab
        };
    },
});
</script>
