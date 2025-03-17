/**
 *
 */
export type Diff<T, U> = T extends U ? never : T;

/**
 *
 */
export type Nullable<T, K extends keyof T = keyof T> = {
  [P in keyof T]: P extends K ? T[P] | null : T[P];
};

/**
 *
 */
export type Optional<T, K extends keyof T = keyof T> = {
  [P in Diff<keyof T, K>]: T[P];
} & {
  [P in K]?: T[P] | undefined;
};

/**
 *
 */
export type NotNull<T, K extends keyof T = keyof T> = {
  [P in keyof T]: P extends K ? Diff<T[P], null> : T[P];
};

export type Scalars = string | number | boolean | null;

/**
 *
 */
// @ts-ignore
export type Json = Record<string, Json | Array<unknown>>;
// export type Json = { [key: string]:  Scalars | Json[] | Json | Array<Scalars> } | Array<Json>;

/**
 *
 */
export interface ForeignKey<T, R = number> extends R {
  isForeignKey?: true;
  relation?: T;
}

/**
 *
 */
export type IdLiteral = 'id';

/**
 *
 */
export type ForeignKeys<T> = {
  [P in keyof Required<T>]: T[P] extends ForeignKey<infer R> ? P : never;
}[keyof T];

/**
 *
 */
export type RelationNames<
  T,
  I = IdLiteral
> = ForeignKeys<T> extends `${infer N}${Capitalize<IdLiteral>}` ? N : never;

/**
 *
 */
export type Relations<T, K extends RelationNames<T> = RelationNames<T>, I = IdLiteral> = {
  [P in K]: T[`${P}${Capitalize<I>}`] extends ForeignKey<infer R> ? R : never;
};

/**
 *
 */
export type WithRelations<T, K extends RelationNames<T> = RelationNames<T>> = T &
  Pick<Relations<T>, K>;

/**
 *
 */
export type QueryParamsMapper = {
  [key: string]: (value: string) => any;
};

/**
 *
 */
export type New<T> = Nullable<T, 'id' | ForeignKeys<T>>;

/**
 *
 */
export type Core<T> = Optional<T, 'id'>;

/**
 *
 */
export type AnyObject = Record<string | number, any>;

/**
 *
 */
export type StatusMessage = {
  status: 'ok';
  warning: string;
  // eslint-disable-next-line camelcase
  warning_info: Array<AnyObject>;
};

/**
 *
 */
export type FileResponse = string;

export type ID = 'id';

// export type HasId<F extends ID = 'id', T = number> = Record<F, T>;
export interface HasId<F extends ID = 'id', T = number> {
  F: T;
}

export type FilterKeys<T, V> = Exclude<
  {
    [K in keyof T]: T[K] extends V ? K : never;
  }[keyof T],
  undefined
>;

export type ScalarKeys<T> = FilterKeys<T, string | number | symbol>;

export interface IEndpointData {
  method:
    | 'GET'
    | 'POST'
    | 'DELETE'
    | 'PUT'
    | 'get'
    | 'delete'
    | 'head'
    | 'HEAD'
    | 'options'
    | 'OPTIONS'
    | 'post'
    | 'put'
    | 'patch'
    | 'PATCH'
    | 'purge'
    | 'PURGE'
    | 'link'
    | 'LINK';
  url: string;
}

export interface CRUDEndpointCollection {
  LIST: IEndpointData;
  LIST_BRIEF?: IEndpointData;
  GET: (id: number) => IEndpointData;
  STORE: IEndpointData;
  UPDATE: (id: number) => IEndpointData;
  DELETE: (id: number) => IEndpointData;
}

export interface WafError {
  id: string;
  content: string;
  url: string;
}

// Рекомендуется как минимум один из объекта
export type RequireAtLeastOne<T, Keys extends keyof T = keyof T> = Pick<T, Exclude<keyof T, Keys>> &
  {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Pick<T, Exclude<Keys, K>>>;
  }[Keys];

// Только одно из объекта рекомендуется
export type RequireOnlyOne<T, Keys extends keyof T = keyof T> = Pick<T, Exclude<keyof T, Keys>> &
  {
    [K in Keys]-?: Required<Pick<T, K>> & Partial<Record<Exclude<Keys, K>, undefined>>;
  }[Keys];

export type QuasarTableColumn<T extends object = any> = {
  name: string;
  label: string;
  field?: keyof T | ((val: T) => unknown);
  format?: (val: T, row: number) => unknown;
  align?: string;
  required?: boolean;
  sortable?: boolean;
  style?: string;
};

export type QuasarTableColumnList<T extends object = any> = Array<QuasarTableColumn<T>>;
