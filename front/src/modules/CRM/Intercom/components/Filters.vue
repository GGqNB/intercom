<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <s-base-filters :applied-filters-count="appliedFiltersCount" >
    <template #default>


      <div class="full-width s-filter--elem">
        <!-- <s-select-backend
            v-model="filterParams.oktmo_group_index"
            :getter="getPhones"
            option-label="name"
            option-value="id"
            label="Поиск по имени"
            class=" "
            search-filter="fio" 
            @update:model-value="$emit('apply-filter')"

        /> -->
      </div>
            <div class="full-width s-filter--elem">
              <s-input
                        v-model="filterParams.name"
                        label="Поиск по названию"
                        clearable
                        debounce="600"
                        class="col-12"
                        @update:model-value="$emit('apply-filter')"
            
                    >
                        <template v-slot:prepend>
                            <q-icon name="email" />
                        </template>
                    </s-input>
      
      </div>
      <!-- <div class=" full-width  s-filter--elem">
        <s-select
            v-model="filterParams.status"
            :options="optionStatusTicket"
            option-label="label"
            option-value="value"
            label="Выберите справочник:"
            emit-value
            @update:model-value="$emit('apply-filter')"
            map-options
        />
      </div> -->
      
    </template>
  </s-base-filters>
</template>
<script lang="ts">
import { computed, defineComponent, PropType } from 'vue';
import { useSelectBackend } from 'src/composables/useSelectBackend';
export default defineComponent({
  props: {
    modelValue: {
      type: Object,
      required: true,
    },
    appliedFiltersCount: {
      type: Number,
      default: 0,
    },

  },
  emit: ['update:model-value', 'apply-filters', 'clear'],
  setup(props, { emit }) {

    const filterParams = computed({
      get: () => props.modelValue,
      set: (val) => emit('update:model-value', val),
    });

    const { getIntercom } = useSelectBackend();


    return {
      filterParams,
      getIntercom,
    };
  },
})
</script>
