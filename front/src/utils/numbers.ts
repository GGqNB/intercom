import { isString } from './check';

/**
 * Округление числа до определенной точности
 *
 * @param num число
 * @param precision точность
 */
export const roundNumberToPrecision = (num: number, precision: number): number => {
  return +(Math.round(+(num + 'e+' + precision)) + 'e-' + precision);
};

/**
 * Сравнение двух чисел с округлением до определенного кол-ва знаков
 * @param a первое число
 * @param b второе число
 * @param precision точность
 */
export const isNumbersEqualsWithPrecision = (a: number, b: number, precision = 2): boolean => {
  return roundNumberToPrecision(a, precision) === roundNumberToPrecision(b, precision);
};

/**
 * Проверяет является ли `val` целым числом
 * @param val значение
 */
export const isPositiveNumber = (val: number): boolean => val > 0;

/**
 * Проверяет является ли `val` строкой с целым и положительным числом
 * @param val значение
 */
export const isPositiveIntegerString = (val: any): boolean =>
  isString(val) && /^[1-9]\d*$/.test(val);

/**
 * Приведение дробного числа к числу в локальном отображении
 * В РФ с запятой
 * @param num
 * @param fracDigits
 * @param useGrouping
 * @returns
 */
export const floatNumberToLocaleString = (
  num: any,
  fracDigits = 2,
  useGrouping = true,
  defaultVal = 'Н.д.'
): string | number => {
  if (typeof num === 'number') {
    const params = {
      minimumFractionDigits: fracDigits,
      maximumFractionDigits: fracDigits,
      useGrouping,
    };
    return Number(num).toLocaleString('ru-RU', params);
  }
  return num ?? defaultVal;
};

/**
 * Форматируем число пользуюясь правилами форматирования в РФ
 *
 * @param {number} value
 * @param {Intl.NumberFormatOptions} options
 * @returns {string}
 */
export const numberFormat = (value: number, options?: Intl.NumberFormatOptions): string =>
  Intl.NumberFormat('ru-RU', options).format(value);
