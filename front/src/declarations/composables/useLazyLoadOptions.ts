// import { computed, Ref, ref, useAttrs, watch } from 'vue';
// import { QSelect, QVirtualScroll } from 'quasar';
// import { blankPaginator } from 'SharedDir/common/composables/usePagination';
// import { makeRequest } from 'SharedDir/common/composables/useRequests';
// import { BasePaginated } from 'SharedDir/declarations/pagination';

// export const useLazyLoadOptions = (
//   attrs: ReturnType<typeof useAttrs>,
//   props,
//   select: Ref<QSelect>
// ) => {
//   const objectList = ref<Array<object>>([]);
//   const objectFilter = ref('');
//   const objectPagination = ref(<BasePaginated>blankPaginator({ rowsPerPage: 50 }));
//   const virtualScrollHasMore = ref(true);
//   const innerLoading = ref(false);
//   const requestOptions = {
//     startLoading() {
//       innerLoading.value = true;
//     },
//     finishLoading() {
//       innerLoading.value = false;
//     },
//   };

//   const smartOptions = computed(() => (props.lazy ? objectList.value : props.options));
//   const smartLoading = computed(() => (props.lazy ? innerLoading.value : attrs.loading));
//   const smartUseInput = computed(() => (props.lazy ? true : attrs.useInput));

//   const refreshObjectList = async (filter: string) => {
//     if (objectFilter.value !== filter || props.filterTreshold === 0) {
//       objectPagination.value.page = 1;
//       objectList.value = [];
//     }
//     if (!props.factory) return;
//     const data = await props.factory({ ...objectPagination.value, filter });
//     console.debug(`Got ${data.length} records.`);
//     virtualScrollHasMore.value = data.length === (objectPagination.value.rowsPerPage as number);
//     objectList.value = objectList.value.concat(data);
//     objectFilter.value = filter;
//   };

//   /**
//    *
//    * @param {string} val
//    * @param {Function} update
//    * @param {Function} abort
//    * @returns {Promise<void>}
//    */
//   const filterObjects = async (val: string, update: CallableFunction, abort: CallableFunction) => {
//     if (val.length < props.filterTreshold) {
//       abort();
//       objectList.value = [];
//       virtualScrollHasMore.value = true;
//       return;
//     }
//     if (val === objectFilter.value && props.filterTreshold > 0) {
//       update();
//       return;
//     }
//     objectPagination.value.page = 1;
//     try {
//       await makeRequest(() => refreshObjectList(val), requestOptions);
//       update();
//     } catch (e) {
//       abort();
//       throw e;
//     }
//   };

//   /**
//    *
//    * @param {number} to
//    * @param {QVirtualScroll} virtualScroll
//    * @param {string} direction
//    * @returns {Promise<void>}
//    */
//   const askForMoreObjects = async ({
//     to,
//     ref: virtualScroll,
//     direction,
//   }: {
//     to: number;
//     direction: string;
//     ref: QVirtualScroll;
//   }) => {
//     if (direction === 'decrease') return;

//     if (!innerLoading.value && virtualScrollHasMore.value && to === objectList.value.length - 1) {
//       console.debug('Asking for more options ...');
//       objectPagination.value.page += 1;
//       await makeRequest(() => refreshObjectList(objectFilter.value), requestOptions);
//       virtualScroll.refresh();
//     }
//   };

//   const clearFilterOnBlur = () => {
//     select.value.updateInputValue('', true);
//   };

//   const smartFilter = computed(() => (props.lazy ? filterObjects : attrs.filter));
//   const smartVirtualScroll = computed(() => (props.lazy ? askForMoreObjects : attrs.filter));
//   const smartBlur = computed(() => (props.lazy ? clearFilterOnBlur : attrs.blur));

//   const lazyResolver = async (newValue) => {
//     if (newValue === null || (Array.isArray(newValue) && newValue.length === 0)) {
//       objectList.value = [];
//     }
//     if (objectList.value.length !== 0) return;
//     objectList.value = await makeRequest(() => props.resolveValue(newValue), requestOptions);
//   };

//   if (props.lazy && props.resolveValue) {
//     watch(() => attrs.modelValue, lazyResolver);
//   }

//   const lazyHint = computed(() => {
//     if (!props.lazy || attrs.readonly || attrs.disable) {
//       return undefined;
//     }
//     let text = 'Пожалуйста введите поисковую фразу';
//     if (props.filterTreshold > 1) {
//       text += ` (мин ${props.filterTreshold} символа)`;
//     }
//     return text;
//   });

//   return {
//     smartOptions,
//     smartUseInput,
//     smartLoading,
//     smartFilter,
//     smartVirtualScroll,
//     smartBlur,
//     lazyHint,
//     lazyResolver,
//   };
// };
