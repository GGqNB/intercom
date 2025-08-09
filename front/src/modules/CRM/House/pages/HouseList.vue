<template>
<s-page>
    <s-header
        title="Здания(Дома)"
        :create-btn="true"
        @clickBtn="visibleDialog = !visibleDialog"
    />
    <filters-house
      v-model="filterParams"
      @apply-filter="fetch"
      @clear="clearParameters"
      />

    <div>
        <div class="mt-base-15">
            <q-table
                class="s-table--wrapper bordered q-mt-xl"
                table-class=""
                dense
                flat
                :rows="list"
                :columns="TABLE_COLUMNS"
                :no-data-label="TABLE_SETTINGS.NO_DATA_LABEL"
                :no-results-label="TABLE_SETTINGS.NO_RESULTS_LABEL"
                :rows-per-page-options="TABLE_SETTINGS.ROWS_PER_PAGE_LIST"
                :rows-per-page-label="TABLE_SETTINGS.ROWS_PER_PAGE_LABEL"
                v-model:pagination="paginationParams"
                @request="onRequest"
            >

            </q-table>
        </div>
    </div>
    <div class="">

        <dialog-house v-model="visibleDialog" :create-service="createService" />
    </div>

    <div class="home_wrapper">

    </div>
    <div class="main_footer">
    </div>
</s-page>
</template>

<script lang="ts">
;
import {
    defineComponent,
    onMounted,
    ref,
} from 'vue';
import {
    useList
} from '../composables/useList';
import FiltersHouse from '../components/Filters.vue'
import DialogHouse from '../components/DialogHouse.vue';

export default defineComponent({
    name: 'EntryListPage',
    components: {
        DialogHouse,
        FiltersHouse
    },
    setup() {
        const {
            init,
            list,
            TABLE_SETTINGS,
            TABLE_COLUMNS,
            paginationParams,
            onRequest,
            visibleDialog,
            filterParams,
            fetch,
            clearParameters,
            currentUserId,
            title
        } = useList();

        const createService = (NewDataPromise) => {
            NewDataPromise.then((NewService) => {
                if (NewService == undefined) {
                    visibleDialog.value = true;
                } else {
                    list.value.push(NewService);
                    visibleDialog.value = !visibleDialog.value;
                }
            }).catch((error) => {
                console.error('Error while processing NewDataPromise:', error);
            });
        }

        onMounted(() => init())
        return {
            init,
            list,
            TABLE_SETTINGS,
            TABLE_COLUMNS,
            paginationParams,
            onRequest,
            visibleDialog,
            createService,
            filterParams,
            fetch,
            clearParameters,
            currentUserId,
            title
        };
    },
});
</script>
