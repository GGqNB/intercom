import 'jest-extended';

export type SelectOptions = Array<{ value: number | string; label: string }>;

export type RemoveNonStrings<T extends Record<string, unknown>> = {
  [K in keyof T]: T[K] extends string ? T[K] : never;
};

type MapTuple<T extends Record<string, unknown>, N extends string, V extends string> = {
  [K in T as RemoveNonStrings<K>[N]]: RemoveNonStrings<K>[N] extends string ? K[V] : never;
};

export type CopyFormType = {
  id: number;
  name: string;
};
