/* eslint-disable @typescript-eslint/ban-types */
import {
  NullableQueryNumber,
  QueryBoolean,
  QueryNumber,
  Sanitizer,
  QueryString,
} from 'src/composables/useQueryString';
import { PaginationParams, BasePagination, BasePaginated } from 'src/declarations/components/pagination';
import { ref } from 'vue';

// todo: добавить типы этому всему !!!!!!!!!!!
export const paginator = (extra: Record<string, Sanitizer> = {}) => ({
  page: QueryNumber,
  rowsPerPage: NullableQueryNumber,
  pages: QueryNumber,
  // size: NullableQueryNumber,
  sortBy: QueryString,
  descending: QueryBoolean,
  ...extra,
});

export const blankPaginator = <T extends Record<string, unknown>>(
  extra: T = {} as T
): PaginationParams<T> => ({
  page: 1,
  pages: 1,
  size: 10,
  rowsPerPage: 10,
  rowsNumber: 0,
  sortBy: 'id',
  descending: false,
  ...extra,
});

export function usePagination(extraPaginationParams: BasePagination | {} = {}) {
  const defaultPaginator = blankPaginator;

  const paginationParams = ref<BasePaginated>({ ...defaultPaginator(), ...extraPaginationParams });

  const sanitizeQueryPagination = paginator;

  const setPaginationFromData = (responseData) => {
    paginationParams.value.page = responseData.page ?? paginationParams.value.page;

    paginationParams.value.size =
    responseData.rowsPerPage ?? paginationParams.value.rowsPerPage;

    paginationParams.value.rowsPerPage =
      responseData.rowsPerPage ?? paginationParams.value.rowsPerPage;

    paginationParams.value.descending =
      responseData.descending ?? paginationParams.value.descending;

    paginationParams.value.sortBy = responseData.sortBy;

    paginationParams.value.pages =
      responseData.pages ?? paginationParams.value.pages;
  };

  /**
   * Сброс пагианции к заводским настройкам
   */
  function resetPagination() {
    paginationParams.value = <BasePaginated>defaultPaginator(extraPaginationParams);
  }

  return {
    paginationParams,
    sanitizeQueryPagination,
    setPaginationFromData,
    defaultPaginator,
    resetPagination,
  };
}
