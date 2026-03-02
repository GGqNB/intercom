import { ref } from 'vue';
import {
  AbstractQueryParams,
  QueryString,
} from 'src/composables/useQueryString';

export type Filters = {
  name: string | null;
};

export function useServiceFilters() {
  const defaultFilterParams = (): Filters => ({
    name: null,
  });

  const filterParams = ref<Filters>(defaultFilterParams());

  const sanitizeQueryFilterParams = (): AbstractQueryParams => ({
    name: QueryString,
  });

  return {
    filterParams,
    defaultFilterParams,
    sanitizeQueryFilterParams,
  };
}
