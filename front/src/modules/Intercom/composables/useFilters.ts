import { ref } from 'vue';
import {
  AbstractQueryParams,
  QueryString,
} from 'src/composables/useQueryString';

export type Filters = {
  geo_adress: string | null;
};

export function useServiceFilters() {
  const defaultFilterParams = (): Filters => ({
    geo_adress: null,
  });

  const filterParams = ref<Filters>(defaultFilterParams());

  const sanitizeQueryFilterParams = (): AbstractQueryParams => ({
    geo_adress: QueryString,
  });

  return {
    filterParams,
    defaultFilterParams,
    sanitizeQueryFilterParams,
  };
}
