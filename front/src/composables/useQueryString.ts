/* eslint-disable @typescript-eslint/no-explicit-any */
import { mapValues, pick } from 'lodash';
import { useSettingsStore } from 'src/stores/settings.store';
import { isRef, Ref, toValue } from 'vue';
import { LocationQueryValue, useRoute, useRouter } from 'vue-router';

/**
 *
 * @param value
 */
const decoded = (value: LocationQueryValue[] | LocationQueryValue): null | string | string[] => {
  if (typeof value === 'undefined' || value === null) {
    return null;
  }
  if (Array.isArray(value)) {
    return value.filter((v) => v !== null).map((v) => decodeURI(<string>v));
  }
  return decodeURI(value);
};

export const QueryNumber = <T = number>(
  queryStringValue: LocationQueryValue[] | LocationQueryValue
): T => +(queryStringValue ?? 0) as unknown as T;

export const NullableQueryNumber = (
  queryStringValue: LocationQueryValue[] | LocationQueryValue
): number | null =>
  typeof queryStringValue !== 'undefined' && queryStringValue !== null ? +queryStringValue : null;

/**
 * Маппер для преобразования значения из строки запроса в строку
 */
export const QueryString = (queryStringValue: LocationQueryValue): string | null =>
  decodeURI(queryStringValue ?? '');

/**
 * Маппер для преобразования значения из строки запроса в булево значение
 */
export const QueryBoolean = (
  queryStringValue: LocationQueryValue[] | LocationQueryValue
): boolean => queryStringValue === 'true';

/**
 * Маппер для преобразования значения из строки запроса в массив строк
 */
export const QueryArray = (
  queryStringValue: LocationQueryValue | LocationQueryValue[]
): Array<string> => queryStringValue as string[];
// decoded((String(queryStringValue) ?? '').split(',')) as string[];

/**
 * Маппер для преобразования значения из строки запроса в массив из чисел
 */
export const QueryNumberArray = (queryStringValue: string[] | string) => {
  if (!queryStringValue) {
    return null;
  }
  if (!Array.isArray(queryStringValue)) {
    queryStringValue = [queryStringValue];
  }
  return queryStringValue.map((s) => (s !== '' ? +s : null)).filter((s) => s !== null);
};

/**
 *
 */
export type Sanitizer<T = unknown> = (rawValue: any) => T;

/**
 *
 */
export type AbstractQueryParams = { [Key: string]: (...any) => any };
// export type QueryParams<T extends object> = { [Key: keyof T]: (...any) => any };

/**
 *
 */
export type ParamsSet<T extends AbstractQueryParams> = { [K in keyof T]: ReturnType<T[K]> };

interface QueryStringUsageOptions {
  /**
   * Необходимо ли сохранять параметры строки запроса
   * на пользовательском устройстве, и восстанавливать их в дальнейшем
   *
   * Доступные значения:
   * - false - параметры строки запроса, не сохраняются в стору (localStorage)
   * - true - параметры строки запроса сохраняются в стору (ключ - '`${router.path}_query-params`')
   * - '[любая строка]' - параметры строки запроса сохраняются в стору (ключ - переданная строка)
   * - () => '[любая строка]' - параметры строки запроса сохраняются в стору (ключ - сгенерированная  строка)
   */
  saveInStore: boolean | string | (() => string);
}

const defaultOptions: Partial<QueryStringUsageOptions> = {
  saveInStore: true,
};
/**
 * Компоузабл метод, возвращающий методы
 * чтения и установки параметров строки запроса
 *
 * @param parameters
 * @param defaultParams
 * @param options {Partial<QueryStringUsageOptions>} [{saveInStore: true}]
 * @returns {
 *   getQueryParams: () => ParamsSet<T>,
 *   setQueryParams: (value: ParamsSet<T>) => Promise<void>,
 * }
 */
export const useQueryString = <T extends AbstractQueryParams>(
  parameters: T,
  defaultParams: Partial<ParamsSet<T>> = {},
  options: Partial<QueryStringUsageOptions> = defaultOptions
) => {
  const route = useRoute();
  const router = useRouter();
  const availableParams = Object.keys(parameters);
  const blankParams = Object.fromEntries(availableParams.map((key) => [key, null]));

  const opt = { ...defaultOptions, ...options };
  const settingsStore = useSettingsStore();

  function resolveStoreKey(): string | false {
    if (typeof opt.saveInStore === 'string') {
      return opt.saveInStore;
    }
    if (opt.saveInStore === true) {
      return `${route.path}_query-params`;
    }
    if (typeof opt.saveInStore === 'function') {
      return opt.saveInStore();
    }

    if (opt.saveInStore === false) {
      return false;
    }
    throw new Error('Неизвестный тип параметра для настроек строки запроса');
  }

  /**
   * Сохраняем переданный объект в стору с сохраненными настройками
   *
   * _**Если при использовании `useQueryString` соответствующая настройка не была включена то ничего не произойдет**_
   *
   * @param {Record<string | number | symbol, unknown>} params
   */
  function storeQueryParams(params: Record<string | number | symbol, unknown>) {
    const key = resolveStoreKey();
    if (key !== false) {
      // console.debug(`Storing query params for key "${key}"`, params);
      settingsStore.save(key, params);
    }
  }

  /**
   * Извлекаем параметры строки запроса из хранилища настроек
   *
   * _**Если при использовании `useQueryString` соответствующая настройка не была включена то ничего не произойдет**_
   *
   * @returns {Partial<ParamsSet<T>>}
   */
  function restoreQueryParams(): Partial<ParamsSet<T>> {
    const key = resolveStoreKey();
    if (key !== false) {
      const restored = settingsStore.settings[key];
      // console.debug(`Restoring query params for key "${key}"`, restored);
      return typeof restored === 'object' && restored ? restored : {};
    }
    return {};
  }

  /**
   * Метод читает параметры командной строки
   */
  const getQueryParams = (): ParamsSet<T> => {
    const fit = Object.entries(route.query).filter(
      ([key, value]) => availableParams.includes(key) && value !== null
    );
    const sanitizedEntries = fit.map(([key, value]) => {
      const resolve = parameters[key];
      const decodedValue = decoded(value);
      const resolvedValue = resolve(decodedValue);
      return [key, resolvedValue];
    });
    const realParams = Object.fromEntries(sanitizedEntries);
    const fromStore = restoreQueryParams();
    return {
      // Сначала все "зарегистрированные" параметры с пустыми значениями, просто что бы они были все
      ...blankParams,
      // Затем затираем параметрами по умолчанию, на случай если какой-либо параметр не пустой
      ...defaultParams,
      // Если мы используем сохранение параметров строки запроса, то достаем все что сохранено
      ...fromStore,
      // И только после этого добираемся до реальных на данный момент параметров строки запроса.
      // Если пользователь пришел по прямой ссылке
      ...realParams,
    };
  };

  /**
   * Метод устанавливает параметры строки запроса
   * @param value
   */
  // const setQueryParams = async (value: ParamsSet<T>) => {

  const setQueryParams = async (value) => {
    const onlyAvailable = pick(value, availableParams);
    // console.debug(value, onlyAvailable);
    storeQueryParams(onlyAvailable);
    // В данном случае необходимо приводить нулловые значения к undefined потому что роутер считает нулл
    // не совсем пустым и все равно пихает ключ со значением нулл в строку запроса без значения
    const notEmpty = mapValues(onlyAvailable, (v) => (v !== null ? v : undefined));
    const params = { ...route.query, ...notEmpty };
    await router.replace({ query: params });
  };

  /**
   * Метод наполняет переданные объекты значениями из строки запроса
   *
   * @param {(Ref<Record<string, unknown>> | Record<string, unknown>)[] | [(Ref<Record<string, unknown>> | Record<string, unknown>)[]]} args
   */
  const fillFromQueryString = (
    ...args:
      | (Ref<Record<string, unknown>> | Record<string, unknown>)[]
      | [(Ref<Record<string, unknown>> | Record<string, unknown>)[]]
  ) => {
    if (args.length === 0) return;
    let targets: (Ref<Record<string, unknown>> | Record<string, unknown>)[];
    if (Array.isArray(args[0])) {
      [targets] = args as (Ref<Record<string, unknown>> | Record<string, unknown>)[][];
    } else {
      targets = args as (Ref<Record<string, unknown>> | Record<string, unknown>)[];
    }

    const values = getQueryParams();

    targets.forEach((target) => {
      const keys = Object.keys(toValue(target));
      const updatedValues = pick(values, keys);
      if (isRef(target)) {
        target.value = { ...target.value, ...updatedValues };
      } else {
        target = { ...target, ...updatedValues };
        keys.forEach((key) => {
          if (typeof updatedValues !== 'undefined') {
            target[key] = updatedValues[key];
          }
        });
      }
    });
  };

  const fillFromQueryStringSsr = (
    ssrValue,
    ...args:
      | (Ref<Record<string, unknown>> | Record<string, unknown>)[]
      | [(Ref<Record<string, unknown>> | Record<string, unknown>)[]]
  ) => {
    if (args.length === 0) return;
    let targets: (Ref<Record<string, unknown>> | Record<string, unknown>)[];
    if (Array.isArray(args[0])) {
      [targets] = args as (Ref<Record<string, unknown>> | Record<string, unknown>)[][];
    } else {
      targets = args as (Ref<Record<string, unknown>> | Record<string, unknown>)[];
    }
    const values = ssrValue;
    targets.forEach((target) => {
      const keys = Object.keys(toValue(target));
      const updatedValues = pick(values, keys);
      if (isRef(target)) {
        target.value = { ...target.value, ...updatedValues };
      } else {
        target = { ...target, ...updatedValues };
        keys.forEach((key) => {
          if (typeof updatedValues !== 'undefined') {
            target[key] = updatedValues[key];
          }
        });
      }
    });
  };
  return {
    getQueryParams,
    setQueryParams,
    fillFromQueryString,
    fillFromQueryStringSsr,
    storeQueryParams,
    restoreQueryParams,
  };
};
