<template>
  <q-select
    v-model="localModel"
    multiple
    use-input
    use-chips
    outlined
    dense
    fill-input
    hide-selected
    :class="classes"
    :clearable="clearable"
    :disable="disable"
    :hide-bottom-space="hideBottomSpace"
    :options-dense="optionsDense"
    :loading="loading"
    :options="options"
    :option-label="optionLabel"
    popup-content-class="multi-select--popup"
    :label="label"
    :error="error"
    :error-message="errorMessage"
    @update:model-value="onUpdate"
    @virtual-scroll="onScroll"
    @filter="filterFn"
    @focus="onSelectFocus"
    @blur="onSelectBlur"
  >
    <template #default>
      <slot></slot>
    </template>
    <template #no-option>
      <q-item>
        <q-item-section class="text-italic text-grey">Объекты не найдены</q-item-section>
      </q-item>
    </template>
  </q-select>
  <!-- <div v-if="showWarning" class="text-orange">
      Пожалуйста, введите не менее 3 символов.
    </div> -->
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch, toRef, PropType } from 'vue';

type OptionObject = Record<string, string> & { id: number };

export default defineComponent({
  name: 'SSelectBackend',
  props: {
    getter: {
      type: Function,
      required: true,
    },
    optionLabel: {
      type: String,
      required: true,
    },
    error: {
      type: Boolean,
    },
    errorMessage: {
      type: String,
    },
    modelValue: {
      type: Array as PropType<number[]>,
      required: true,
    },
    clearable: {
      type: Boolean,
      default: false,
    },
    disable: {
      type: Boolean,
      default: false,
      required: false,
    },
    label: {
      type: String,
    },
    required: {
      type: Boolean,
      default: false,
      required: false,
    },
    hideBottomSpace: {
      type: Boolean,
      default: true,
    },
    optionsDense: {
      type: Boolean,
      default: true,
    },
    searchFilter: {
      type: String,
      default: 'filter'
    }
  },
  setup(props, { emit }) {
    const classesArray = ref([
      's-select',
      props.disable ? 's-select--disable' : '',
      props.required ? 'required' : '',
    ] as Array<string>);
    const classes = ref(classesArray.value.join(' ') as string);
    const localModel = ref<string[]>([]);
    const options = ref<Record<string, string>[]>([]);
    const currentPage = ref(1);
    const loading = ref(false);
    const search = ref('');
    const lastPage = ref(0);

    async function updateLocalModel(modelValue?: number[]) {
      // if (modelValue) {
      //   localModel.value = modelValue;
      // } else {
      //   localModel.value = [];
      // }
    }

    onMounted(async () => await updateLocalModel(props.modelValue));

    watch(toRef(props, 'modelValue'), async (modelValue) => {
      await updateLocalModel(modelValue);
    });
    const showWarning = ref(false);
    const filterFn = async (value: string, update: () => void) => {
   
        showWarning.value = false;
        search.value = value;
        loading.value = true;
        await props.getter({
          [props.searchFilter]: search.value,
          page: '1',
          size: '20',
        }).then(
          (r: any) => {
            options.value = r.items;
            lastPage.value = r.pages;
          }
        );
        currentPage.value = 1;
        loading.value = false;
        update();
      
    }

    const onScroll = async (scrollData: {
      to: number;
      ref: { refresh: () => void };
    }) => {
      const lastIndex = options.value.length - 1;
      if (
        loading.value == true &&
        currentPage.value < lastPage.value &&
        scrollData.to >= lastIndex
      ) {
        loading.value = true;
        currentPage.value++;
        await props.getter({
          search: search.value,
          page: `${currentPage.value}`,
          size: '20',
        }).then((r: any) => {
          options.value.push(...r.items);
        });
        loading.value = false;
      }
    };
    const onSelectFocus = () => {
      showWarning.value = true; // Показываем предупреждение при фокусировке
    };
    const onSelectBlur = () => {
      showWarning.value = false; // Скрываем предупреждение при потере фокуса
    };
    return {
      classes,
      options,
      filterFn,
      onScroll,
      loading,
      localModel,
      showWarning,
      onSelectFocus,
      onSelectBlur,
      onUpdate: (obj: OptionObject) => {
        const selectedValues = localModel.value.map((val) => val);
        emit('update:model-value', selectedValues);
      },
    }
  },
})
</script>
<style>
/* .multi-select--popup {
  width: 900px;
  min-width: 900px;
  margin-left: -275px !important;
} */
</style>