import mapValues from 'lodash/mapValues';
import keyBy from 'lodash/keyBy';

// простой фильтр-словарь
export const lookInDictionary = (key: string | number, dictionary: unknown, options: any) => {
  const o = {
    key: 'id',
    value: 'name',
    ...options,
  };
  const properDictionary = mapValues(keyBy(dictionary, o.key), o.value);
  // eslint-disable-next-line no-prototype-builtins
  return properDictionary.hasOwnProperty(key) ? properDictionary[key] : key;
};

/**
 * Функция-помощник, которая ищет в словаре (catalog) по ключу (keySearch) и значению (valueSearch)
 * И возвращает значения поля (fieldValue).
 *
 * @param keySearch
 * @param fieldValue
 * @param valueSearch
 * @param catalog
 * @param emptyDefault
 * @returns
 */
export const getFieldValueByFieldIdentifier = (
  keySearch = 'id',
  fieldValue = 'name',
  valueSearch: unknown,
  catalog: Array<unknown>,
  emptyDefault = ''
): unknown => {
  const item = catalog.find((item) => item[keySearch] === valueSearch);
  if (item) {
    return item[fieldValue] ?? emptyDefault;
  }
  return emptyDefault;
};

/**
 * Возвращает наименование правильного склонения к числительному
 * 1 услуга
 * 2 услуги
 * 100 услуг
 *
 * @example n = 12, titles = ['услуга', 'услуги', 'услуг'], return 'услуг'
 * @param n числительное
 * @param titles наименования соответствующие числительному
 */
export const titlePluralForm = (n: number, titles: Array<string>) => {
  return titles[
    n % 10 === 1 && n % 100 !== 11
      ? 0
      : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)
      ? 1
      : 2
  ];
};

/**
 * Перевести строку в булево значение
 *
 * @param val
 * @returns
 */
export const stringToBoolean = (val: string | boolean | null): boolean | null => {
  if (typeof val === 'boolean') {
    return val;
  }

  if (typeof val === 'string' && val.toLowerCase() === 'true') {
    return true;
  }

  if (typeof val === 'string' && val.toLowerCase() === 'false') {
    return false;
  }

  return null;
};

export function asyncTimeout<T>(timeout: number, value?: T) {
  return new Promise<T>((resolve) => {
    setTimeout(resolve, timeout, value);
  });
}

/**
 * Копирование в буфер обмена
 *
 * @param text
 * @returns
 */
export const copyTextToClipboard = async (text: string) => {
  if (!navigator.clipboard) {
    return false;
  }
  return navigator.clipboard
    .writeText(text)
    .then(() => true)
    .catch(() => false);
};


export const stringNumberWithoutSymbols = (number) => {
  return number.replace(/\D/g, '');
};
