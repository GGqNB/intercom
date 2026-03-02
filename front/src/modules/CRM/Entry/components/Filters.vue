<!-- eslint-disable vue/multi-word-component-names -->
<template>
<s-base-filters :applied-filters-count="appliedFiltersCount">
    <template #default>

        <div class=" col-12 col-sm-6 col-md-4 s-filter--elem">
            <s-input
                v-model="filterParams.name"
                label="Поиск по названию"
                clearable
                debounce="600"
                class="col-12"
                @update:model-value="$emit('apply-filter')"
            >
            </s-input>

        </div>
        <div class="col-12 col-sm-6 col-md-4 s-filter--elem">
            <s-input
                v-model="filterParams.geo_address"
                label="Поиск по адресу дома"
                clearable
                debounce="600"
                class="col-12"
                @update:model-value="$emit('apply-filter')"
            >
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
import {
    computed,
    defineComponent,
    PropType
} from 'vue';
import {
    useSelectBackend
} from 'src/composables/useSelectBackend';
import SBaseFilters from 'src/components/Filters/BaseFilters.vue';
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
    components:{
    SBaseFilters
    },
    emit: ['update:model-value', 'apply-filters', 'clear'],
    setup(props, {
        emit
    }) {

        const filterParams = computed({
            get: () => props.modelValue,
            set: (val) => emit('update:model-value', val),
        });

        const {
            getIntercom
        } = useSelectBackend();

        return {
            filterParams,
            getIntercom,
        };
    },
})
</script>
