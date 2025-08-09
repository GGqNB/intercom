import { Tables } from 'src/declarations/components/table';

export const ROWS_PER_PAGE = 3;

export const ROWS_PER_PAGE_LIST: Array<number> = [1, 25, 100];

export const NO_DATA_LABEL = 'Нет данных';

export const NO_RESULTS_LABEL = 'Совпадений не найдено';

export const ROWS_PER_PAGE_LABEL = 'Записей на странице:';

export const TABLE_SETTINGS: Tables.TTableSetting = {
  ROWS_PER_PAGE,
  ROWS_PER_PAGE_LIST,
  NO_DATA_LABEL,
  NO_RESULTS_LABEL,
  ROWS_PER_PAGE_LABEL,
};
