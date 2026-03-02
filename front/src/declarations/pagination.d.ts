/* eslint-disable @typescript-eslint/ban-types */

// Обязательная передача числа (для пагинации)
export type NumberedRowsPerPage = number;

// При передаче null пагинация игнорируется и берутся все записи
export type AllRowsPerPage = null;

export type MixedRowsPerPage = NumberedRowsPerPage | AllRowsPerPage;

/**
 * Типы для пагинации при запросе значений
 *
 * @type PaginationParams
 */
export type PaginationParams<
 T extends Record<string | number, any> = {},
 R extends MixedRowsPerPage = MixedRowsPerPage
> = {
 page: number;
 rowsPerPage: R; // null - получение всех записей
 rowsNumber?: number;
 showDeleted?: boolean;
 sortBy?: string;
 descending?: boolean;
} & T;

export interface QueryParamsMapper {
  [key: string]: (value: string) => any;
}

interface Link {
  url: null | string;
  label: string;
  active: boolean;
}

export interface PaginationResponse {
  current_page: number;
  first_page_url: null | string;
  from: number;
  last_page: number;
  last_page_url: null | string;
  links: Link[];
  next_page_url: null | string;
  path: null | string;
  per_page: number;
  prev_page_url: null | string;
  to: number;
  total: number;
}
