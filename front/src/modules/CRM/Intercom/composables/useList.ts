import { computed, ref} from 'vue';
import IntercomApi from 'src/backend/api/classes/IntercomClass';
import { Crm } from 'src/declarations/responses/crm';
import { makeRequest } from 'src/composables/useRequest';
import { Tables } from 'src/declarations/components/table';
import { TABLE_SETTINGS } from 'src/constants/table-settings';
import { usePagination } from 'src/composables/usePagination';
import { useQueryString } from 'src/composables/useQueryString';
import { BasePagination } from 'src/declarations/components/pagination';
import { Filters, useServiceFilters } from './useFilters';
import { useSelectBackend } from 'src/composables/useSelectBackend';

export function useList(){ 

 const users = ref([]);
 const TABLE_COLUMNS: Array<Tables.TableColumn> = [
  {
    name: 'id',
    label: '№',
    field: 'id',
    align: 'center',
    sortable: true
  },
  {
    name: 'name',
    label: 'Название',
    field: (row) => row.name ? String(row.name) : 'Отсутствует',
    align: 'center',
    sortable: false,
  },
  {
    name: 'entry',
    label: 'Вход',
    field: (row) => row.entry ? String(row.entry.name) : 'Отсутствует',
    align: 'center',
    sortable: false,
  },
  {
    name: 'flat_first',
    label: 'Начальная кв',
    field: (row) => row.entry ? String(row.entry.flat_first) : 'Отсутствует',
    align: 'center',
    sortable: false,
  },
  {
    name: 'flat_last',
    label: 'Конечная кв',
    field: (row) => row.entry ? String(row.entry.flat_last) : 'Отсутвует',
    align: 'center',
    sortable: false
  },
  {
    name: 'house',
    label: 'Дом',
    field: (row) => row.house ? String(row.house.name) : 'Отсутвует',
    align: 'center',
    sortable: false
  },
   {
    name: 'flat_count',
    label: 'Кол-во кв в доме',
    field: (row) => row.entry ? String(row.entry.house.flat_count) : 'Отсутвует',
    align: 'center',
    sortable: false
  },
];



const visibleDialog = ref(false);
const currentUserId = ref(0);
const list = ref([]);

const { filterParams, sanitizeQueryFilterParams, defaultFilterParams } = useServiceFilters();

const { paginationParams, sanitizeQueryPagination, setPaginationFromData, defaultPaginator } =
    usePagination();
const receive = async (response: Awaited<ReturnType<typeof  IntercomApi.list>>) => {
    list.value = response.items;
    setPaginationFromData(response);

    await setQueryParams(paginationParams.value);
    await setQueryParams(filterParams.value);
  };
  const combinedParametersSanitizers = {
    ...sanitizeQueryFilterParams(),
    ...sanitizeQueryPagination(),
  };
const combinedParameters = computed(() => ({ ...filterParams.value ,...paginationParams.value }));
const { getQueryParams, setQueryParams } = useQueryString(combinedParametersSanitizers, {
     ...filterParams.value,  
     ...paginationParams.value,
  });

    const fetch = async () =>
      makeRequest(async () =>
      receive(
        await  IntercomApi.list(combinedParameters.value)
      )
    );
    const onRequest = async ({ pagination: tablePagination }: { pagination: BasePagination }) => {
    setPaginationFromData(tablePagination);

    await fetch();
  };
const init = async () => {
  fetch();
  const queryParams = getQueryParams();
  setPaginationFromData(queryParams);
};

const clearParameters = async () => {
  paginationParams.value = defaultPaginator();
  filterParams.value = defaultFilterParams();

  await fetch();
};
const title = ref('Заявка OKTMO');

  return {
    init,
    list,
    TABLE_SETTINGS, 
    TABLE_COLUMNS,
    users,
    paginationParams, 
    onRequest,
    visibleDialog,
    filterParams,
    fetch,
    clearParameters,
    currentUserId,
    title
  };
}


