<template>
  <q-select
    v-model="localModel"
    use-input
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
    :option-value="optionValue"
    :label="label"
    :error="error"
    :error-message="errorMessage"
    @update:model-value="onUpdate"
    @virtual-scroll="onScroll"
    @filter="filterFn"
  >
    <template #default>
      <slot></slot>
    </template>
    <template #no-option>
      <q-item>
        <q-item-section class="text-italic text-grey">{{ noDataLabel }}</q-item-section>
        
      </q-item>
      <q-item v-if="noDataLabel != 'Объекты не найдены'" class="flex justify-center">
        <s-btn @click="$emit('add', search)">Создать</s-btn>
        <!-- <s-btn @click="console.log(search)">Создать</s-btn> -->
      </q-item>
    </template>
  </q-select>
</template>
<script lang="ts">
import { defineComponent, onMounted, ref, watch, toRef } from 'vue';

// const pageSize = 10;

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
    noDataLabel: {
      type : String,
      default: 'Объекты не найдены',
    },
    optionValue: {
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
      type: String,
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
    valueObject: {
      type: Boolean,
      default: false,
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

    const localModel = ref<number | string | null>(null);
    const options = ref<Record<string, string>[]>([]);
    const currentPage = ref(1);
    const loading = ref(false);
    const search = ref('');
    const lastPage = ref(0);

    async function updateLocalModel(modelValue?: string) {
      if (modelValue) {
        if (modelValue != localModel.value) {
          // await props.getter({ id: modelValue }).then(
          //   (r: any) => localModel.value = r.items[0]
          // );
        }
      } else {
        localModel.value = null;
      }
    }

    onMounted(async () => await updateLocalModel(props.modelValue));

    watch(toRef(props, 'modelValue'), async (modelValue) => {
      await updateLocalModel(modelValue);
    });

    const filterFn = async (value: string, update: () => void) => {
    console.log(value)
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
  // console.log(scrollData.to)

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
const onUpdate = (obj: OptionObject) => {
      if (props.valueObject) {
        emit('update:model-value', obj ? obj : null); 
      } else {
        emit('update:model-value', obj ? obj[props.optionValue] : null); 
      }
    };
return {
      classes,
      options,
      filterFn,
      onScroll,
      loading,
      localModel,
      onUpdate,
      search
    }
  },
})
</script>