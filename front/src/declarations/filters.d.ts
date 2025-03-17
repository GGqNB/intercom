import { NDataCatalogs } from 'src/declarations/data-catalogs';
import { MapTuple, SelectOptions } from 'src/declarations/general';
import { Nullable } from 'src/declarations/shared';

export namespace NFilters {
  export type Selects = 'multiselect' | 'select';

  export type Type = Selects | 'checkbox' | 'date' | 'text';

  export type ValueType = 'boolean' | 'array' | 'string' | 'date' | 'number';

  export type BaseFilter = {
    name: string;
    type: string;
    valueType: unknown;
    options?: SelectOptions | NDataCatalogs.Name;
  };

  // export interface FIlterItem<
  //   N extends string,
  //   T extends Type,
  //   VT,
  //   O extends null | SelectOptions | NDataCatalogs.Name = null
  // > extends BaseFilter {
  //   name: N;
  //   type: T;
  //   valueType: VT;
  //   options?: O extends null ? never : O;
  // }

  export interface FilterItem<N extends string, T extends Type, VT> extends BaseFilter {
    name: N;
    type: T;
    valueType: VT;
    options?: T extends Selects ? SelectOptions | NDataCatalogs.Name : never;
  }

  export type FilterDeclaration<T extends BaseFilter> = {
    [K in keyof T]: K extends 'valueType' ? ValueType : T[K];
  };

  export type FilterSet<T extends BaseFilter> = Array<FilterDeclaration<T>>;

  export type FilterValue<F extends BaseFilter> = Partial<
    Nullable<MapTuple<F, 'name', 'valueType'>>
  >;
}
