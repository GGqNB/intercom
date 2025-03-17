/* eslint-disable @typescript-eslint/ban-types */
export type BasePagination = {
  pages: number,
  page: number;
  sortBy: string;
  rowsPerPage: null | number;
  descending: boolean;
};
export type BasePaginated = BasePagination & { rowsNumber: number } & { size : number};

export type PaginationParams<T extends object> = T & BasePagination;

/**
 * Тип ответа на постраничный зарос элементов
 */
export type Paginated<DataType, Extra extends object = {}> = Required<BasePaginated> &
  Extra & {
    data: Array<DataType>;
  };

// Обязательная передача числа (для пагинации)
export type NumberedRowsPerPage = number;

// При передаче null пагинация игнорируется и берутся все записи
export type AllRowsPerPage = null;

export type MixedRowsPerPage = NumberedRowsPerPage | AllRowsPerPage;

export interface OffsetParams {
  limit: number;
  offset: number;
  sortBy: string;
  showDeleted: boolean;
  descending: boolean;
}

export interface Limited<T> extends OffsetParams {
  data: Array<T>;
}
