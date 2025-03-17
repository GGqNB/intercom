/* eslint-disable @typescript-eslint/no-explicit-any */
export namespace Tables {
  export type TableColumn = {
    name: string;
    label: string;
    field: string | ((row: any) => any);
    required?: boolean;
    align?: 'left' | 'right' | 'center';
    sortable?: boolean;
    sort?: (a: any, b: any, rowA: any, rowB: any) => number;
    sortOrder?: 'ad' | 'da';
    format?: (val: any, row: any) => any;
    style?: string | ((row: any) => string);
    classes?: string | ((row: any) => string);
    headerStyle?: string;
    headerClasses?: string;
  };

  export type TTableSetting = {
    ROWS_PER_PAGE: number;
    ROWS_PER_PAGE_LIST: Array<number>;
    NO_DATA_LABEL: string;
    NO_RESULTS_LABEL: string;
    ROWS_PER_PAGE_LABEL: string;
  };
}

