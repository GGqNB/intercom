/* eslint-disable @typescript-eslint/ban-ts-comment */
import { cityPhonePattern, PHONE_NUMBER_PATTERN } from './patterns';

export const DISPLAY_DATE_REGEX_STR = '(0[1-9]|[12][0-9]|3[01])[\\.](0?[1-9]|1[012])[\\.]\\d{4}';

export const DISPLAY_DATE_REGEX = new RegExp(`^${DISPLAY_DATE_REGEX_STR}$`);

export const DISPLAY_DATE_RANGE_REGEX = new RegExp(
  `^(${DISPLAY_DATE_REGEX_STR})?[ ]*(-[ ]*${DISPLAY_DATE_REGEX_STR})?$`
);

/**
 * Переданное значение пустая строка или null
 * @param str
 * @returns
 */
export const isEmptyOrNullString = (str: string | null | number): boolean =>
  str === null || (typeof str === 'string' && !str.trim());

/**
 * Проверка, что в объекте имеются значения
 *
 * @param obj
 * @returns
 */
export const isEmptyObject = <T extends object>(obj: T) => Object.keys(obj).length === 0;

/**
 * Переданная строка длинее чем "length"
 *
 * @param str
 * @param length
 * @returns
 */
export const isStringLongerThan = (str: string, length: number): boolean =>
  typeof str === 'string' && str.length >= length;

/**
 * Переданная строка короче чем "length"
 *
 * @param str
 * @param length
 * @returns
 */
export const isStringLessThen = (str: string, length: number): boolean =>
  typeof str === 'string' && str.length < length;

/**
 * Проверка, что заполенен select
 *
 * @param val
 */
export const isSelectFilled = (
  val: number | null,
  defaultTextError = 'Пожалуйста, заполните данное поле'
): boolean | string => {
  if (isEmptyOrNullString(val)) {
    return defaultTextError;
  }
  return true;
};

/**
 * Проверка, что заполнен множественный select
 *
 * @param val
 */
export const isMuptipleSelectFilled = <T = unknown>(
  val: Array<T>,
  defaultTextError = 'Пожалуйста, заполните данное поле'
): boolean | string => {
  if (Array.isArray(val) && val.length === 0) {
    return defaultTextError;
  }
  return true;
};

/**
 * Проверка вводимого Email на корректность
 * @param val
 * @returns
 */
export const isValidEmail = (val: string): boolean => {
  const emailPattern =
    /^(?=[a-zA-Z0-9@._%+-]{6,254}$)[a-zA-Z0-9._%+-]{1,64}@(?:[a-zA-Z0-9-]{1,63}\.){1,8}[a-zA-Z]{2,63}$/;
  return emailPattern.test(val);
};

/**
 * Проверка URL на валидность
 *
 * @param val
 * @returns
 */
export const isValidUrl = (val: string): boolean => {
  const urlPattern =
    // eslint-disable-next-line
    /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/;
  return urlPattern.test(val);
};

/**
 * Проверка СНИЛС на валидность
 *
 * @param snils
 * @returns
 */
export const isValidSnils = (snils: string): boolean | string => {
  snils = snils.replace(/-|\s/g, '');
  let result = false;
  let message = '';

  if (/[^0-9]/.test(snils)) {
    message = 'СНИЛС может состоять только из цифр';
  } else if (snils.length !== 11) {
    message = 'СНИЛС может состоять только из цифр';
  } else {
    let sum = 0;
    for (let i = 0; i < 9; i++) {
      sum += parseInt(snils[i], 10) * (9 - i);
    }
    let checkDigit = 0;
    if (sum < 100) {
      checkDigit = sum;
    } else if (sum > 101) {
      // @ts-ignore
      checkDigit = parseInt(sum % 101, 10);
      if (checkDigit === 100) {
        checkDigit = 0;
      }
    }
    if (checkDigit === parseInt(snils.slice(-2), 10)) {
      result = true;
    } else {
      message = 'Неправильное контрольное число';
    }
  }
  return result;
};

/**
 * Проверка ИНН на валидность
 *
 * @param value
 */
export const isValidINN = (value: string): boolean => {
  // преобразуем в строку
  value = `${value}`;
  if (!/^\d{10}$/.test(value) && !/^\d{12}$/.test(value)) {
    return false;
  }

  // преобразуем в массив
  const valueArr = value.split('').map(Number);

  // для ИНН в 10 знаков
  if (
    valueArr.length === 10 &&
    +valueArr[9] ===
      ((2 * valueArr[0] +
        4 * valueArr[1] +
        10 * valueArr[2] +
        3 * valueArr[3] +
        5 * valueArr[4] +
        9 * valueArr[5] +
        4 * valueArr[6] +
        6 * valueArr[7] +
        8 * valueArr[8]) %
        11) %
        10
  ) {
    return true;
  }

  // для ИНН в 12 знаков
  return (
    valueArr.length === 12 &&
    +valueArr[10] ===
      ((7 * valueArr[0] +
        2 * valueArr[1] +
        4 * valueArr[2] +
        10 * valueArr[3] +
        3 * valueArr[4] +
        5 * valueArr[5] +
        9 * valueArr[6] +
        4 * valueArr[7] +
        6 * valueArr[8] +
        8 * valueArr[9]) %
        11) %
        10 &&
    +valueArr[11] ===
      ((3 * valueArr[0] +
        7 * valueArr[1] +
        2 * valueArr[2] +
        4 * valueArr[3] +
        10 * valueArr[4] +
        3 * valueArr[5] +
        5 * valueArr[6] +
        9 * valueArr[7] +
        4 * valueArr[8] +
        6 * valueArr[9] +
        8 * valueArr[10]) %
        11) %
        10
  );
};

/**
 *  Проверка даты на валидность
 *  type - mature означает что пользователь созрел и ему есть 18 лет
 *  type - noMoreToday означает что выбрана дата не дальше сегодняшней
 *
 * @param inputDate
 * @param type
 */
export const isValidDate = (inputDate: string, type = 'noMoreToday'): boolean => {
  const [d, m, y] = inputDate.split('.');
  const correctInputDate = new Date(+y, +m - 1, +d);

  let dateForCheck;
  const currentDate = new Date();
  if (type === 'mature') {
    dateForCheck = new Date();
    dateForCheck.setFullYear(dateForCheck.getFullYear() - 18);
    return dateForCheck > correctInputDate;
  }
  if (type === 'noMoreToday') {
    return currentDate > correctInputDate;
  }
  return true;
};

/**
 * Correct: qwe_123,
 * @param str
 * @returns
 */
export const isValidSlug = (str: string): boolean => {
  // преобразуем в строку наверняка
  const value = `${str}`;
  // const regexp = /^[a-z]+[a-z0-9_]*/;

  // Исключаем два нижних подчеркивания
  const regexp = /^([a-z]+[a-z0-9]*)+(_{1}[a-z0-9]+)*$/;

  if (regexp.test(value)) {
    return true;
  }
  return false;
};

/**
 * Correct: test-t123,
 *
 * @param str
 * @returns
 */
export const isValidSlugWithDash = (str: string): boolean => {
  // преобразуем в строку наверняка
  const value = `${str}`;

  // Исключаем два нижних подчеркивания
  const regexp = /^[a-z]+(-{1}[a-z0-9]+)*$/;

  if (regexp.test(value)) {
    return true;
  }
  return false;
};

/**
 * Проверка, что строка в нижнем регистре
 * Correct: test_t,
 *
 * @param str
 * @returns
 */
export const isStringInLowerCase = (str: string): boolean => {
  // преобразуем в строку наверняка
  const value = `${str}`;
  const regexp = /^[a-z]+[a-z_]*$/;
  console.log(value, regexp.test(value));
  if (regexp.test(value)) {
    return true;
  }
  return false;
};

/**
 * Correct: '5test_t', 'fd fd-fa'
 * Incorrect: '_qwe', ' asd', '1_fa -fa'
 *
 * @param str
 * @param allowEmpty
 * @returns
 */
export const isStringWithNumberInLowerCase = (str: string | null, allowEmpty = true): boolean => {
  if (str) {
    const regexp = /^([\da-z]+[_\s-]?)+$/;
    return regexp.test(str);
  }
  return allowEmpty;
};

/**
 * Проверка IP адреса v4 на корректность
 *
 * @param str
 * @returns
 */
export const isValidIPv4 = (str: string): boolean => {
  const value = `${str}`;
  const regexp =
    /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/;
  if (regexp.test(value)) {
    return true;
  }
  return false;
};

/**
 * Проверка IP адреса v6 на корректность
 * @param str
 * @returns
 */
export const isValidIPv6 = (str: string): boolean => {
  const value = `${str}`;
  const regexp =
    /^s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:)))(%.+)?s*/;
  if (regexp.test(value)) {
    return true;
  }
  return false;
};

/**
 * Проверка доменного имени
 * @param str
 * @returns
 */
export const isValidDomainName = (str: string): boolean => {
  const value = `${str}`;
  const regexp =
    // eslint-disable-next-line
    /^(?:(?:(?:[a-zA-z\-]+)\:\/{1,3})?(?:[a-zA-Z0-9])(?:[a-zA-Z0-9\-\.]){1,61}(?:\.[a-zA-Z]{2,})+|\[(?:(?:(?:[a-fA-F0-9]){1,4})(?::(?:[a-fA-F0-9]){1,4}){7}|::1|::)\]|(?:(?:[0-9]{1,3})(?:\.[0-9]{1,3}){3}))(?:\:[0-9]{1,5})?$/;
  if (regexp.test(value)) {
    return true;
  }
  return false;
};

/**
 * Проверка UUID на соответствие 4-й версии
 * @param str
 * @returns
 */
export const isUUID4 = (str: string): boolean => {
  const value = `${str}`;
  const regexp = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/;
  if (regexp.test(value)) {
    return true;
  }
  return false;
};

/**
 * Проверка сотового телефона в русском сегменте на корректность
 * #TODO
 */
export const isValidRuMobilePhone = (str: string): boolean => {
  const regexp = new RegExp(cityPhonePattern);
  if (regexp.test(str)) {
    return true;
  }

  return false;
};

/**
 * Проверка рабочего телефона на корректность
 * то есть с учётом добавочного
 * #TODO
 */
export const isValidWorkPhone = (str: string): boolean => {
  return true;
};

/**
 * Проверка на целое число
 * @param val
 * @returns
 */
export const isInteger = () => {
  return (value: number | null): boolean => {
    return Number.isInteger(value);
  };
};

export const dateRule = (v: string) => {
  if (v) return DISPLAY_DATE_REGEX.test(v) || 'Некорректный формат даты';
  return true;
};

export const dateRangeRule = (v: string) => {
  if (v) return DISPLAY_DATE_RANGE_REGEX.test(v) || 'Некорректный формат даты';
  return true;
};

export const toDate = (dateLikeValue: string | Date | null | undefined): Date => {
  if (dateLikeValue instanceof Date) {
    return dateLikeValue;
  }
  if (typeof dateLikeValue === 'string' && dateLikeValue) {
    if (DISPLAY_DATE_REGEX.test(dateLikeValue)) {
      const [d, m, y] = dateLikeValue.split('.');
      return new Date(+y, +m - 1, +d);
    }
    const dateObject = new Date(dateLikeValue);
    if (dateObject.toString() !== 'Invalid Date') {
      return dateObject;
    }
  }

  throw new Error('It is not date-like value!');
};

export const containsUppercase = (value: string): boolean => {
  return /[A-Z]/.test(value);
};

export const containsLowercase = (value: string): boolean => {
  return /[A-Z]/.test(value);
};

export const containsNumber = (value: string): boolean => {
  return /[0-9]/.test(value);
};

