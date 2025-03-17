<template>
  <q-table
    :class="classes"
    :table-class="tableClasses"
    dense
    flat
    :no-data-label="TABLE_SETTINGS.NO_DATA_LABEL"
    :no-results-label="TABLE_SETTINGS.NO_RESULTS_LABEL"
    :rows-per-page-options="TABLE_SETTINGS.ROWS_PER_PAGE_LIST"
    :rows-per-page-label="TABLE_SETTINGS.ROWS_PER_PAGE_LABEL"
  >
    <!-- <template #default>
      <slot></slot>
    </template> -->
    <template #body-cell="props">
      <q-td
        :props="props"
        :class="{ 's-table--row-deleted': props.row.deletedAt }"
      >
        {{ props.value }}
      </q-td>
    </template>
    <template v-for="(_, name) in $slots" v-slot:[name]="slotData">
      <slot :name="name" v-bind="slotData" />
    </template>
    <!-- Slot по умолчанию для загрузки -->
    <template #loading>
      <q-spinner-dots />
    </template>
  </q-table>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { TABLE_SETTINGS } from 'src/constants/table-settings';

export default defineComponent({
  name: 'STable',
  setup(props, { slots, emit }) {
    const classes = 's-table';

    const tableClasses = '';
    return {
      classes,
      tableClasses,
      slots,
      TABLE_SETTINGS,
      emit,
    };
  },
});
</script>
