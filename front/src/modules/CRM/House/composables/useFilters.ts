import { ref } from 'vue';
import {
  AbstractQueryParams,
  QueryString,
} from 'src/composables/useQueryString';

export type Filters = {
  name: string | null;
  geo_adress: string | null;
};

export function useEntryFilters() {
  const defaultFilterParams = (): Filters => ({
    name: null,
    geo_adress: null,
  });

  const filterParams = ref<Filters>(defaultFilterParams());

  const sanitizeQueryFilterParams = (): AbstractQueryParams => ({
    name: QueryString,
    geo_adress: QueryString,
  });

  return {
    filterParams,
    defaultFilterParams,
    sanitizeQueryFilterParams,
  };
}
