/* eslint-disable @typescript-eslint/ban-types */
export type BasePagination = {
  pages?: number;
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

export interface PaginatedList<T>{
  items: T[];
  page: number;
  size: number;
  total: number;
}

// Тип "({ pagination: tablePagination }: { pagination: BasePagination; }) => Promise<void>"
//  не может быть назначен для типа "(requestProp: { pagination: { sortBy: string; descending: 
// boolean; page: number; rowsPerPage: number; }; filter?: any; getCellValue: (col: any, row: any) => any; }) => void".
//   Типы параметров "__0" и "requestProp" несовместимы.
//     Тип "{ pagination: { sortBy: string; descending: boolean; 
// page: number; rowsPerPage: number; };
//  filter?: any; getCellValue: (col: any, row: any) => any; }" не может быть назначен для типа "{ pagination: BasePagination; }".
//       Типы свойства "pagination" несовместимы.
//         Свойство "pages" 
// отсутствует в типе "{ sortBy: string; descending: boolean; page: number; rowsPerPage: number; }" 
// и является обязательным в типе "BasePagination".