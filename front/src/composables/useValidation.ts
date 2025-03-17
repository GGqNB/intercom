/* eslint-disable class-methods-use-this */
import { values } from 'lodash';

import { parseRussianDate, toRussianDate } from 'src/utils/datetime';
import { isValidEmail, isValidRuMobilePhone, isValidSlug } from 'src/utils/validators';
import { toDate } from 'src/utils/date-rule';

export type ValidationRule = (value: any) => true | string;

/**
 * Форматируем строку для вывода в качестве ошибок валидации
 *
 * Метод заменяет все вхождения подстроки типа `{anyPlaceholder}`
 * на значение котрое находиться d _values_ под соответствующим ключом
 *
 * Например:
 *
 *     formatValidationMessage('Меньше чем {max}', { max: 0 }) => 'Меньше чем 0'
 *
 * @param {string} message
 * @param {(Record<string, number | string>)} [values]
 * @returns {string}
 */
const formatValidationMessage = (
  message: string,
  // eslint-disable-next-line @typescript-eslint/no-shadow
  values?: Record<string, number | string>
): string => {
  if (!values || Object.keys(values).length === 0) {
    return message;
  }

  let formatedString = message;
  Object.keys(values).forEach((placeholder) => {
    formatedString = message.replaceAll(`{${placeholder}}`, `${values[placeholder]}`);
  });
  return formatedString;
};

/**
 * Создаем правило для квазаровских элементов формы
 *
 * @param {string} [message='Поле обязательно для заполнения']
 * @returns
 */
const NotEmpty = (message = 'Поле обязательно для заполнения'): ValidationRule => {
  return (value: string | null): true | string => !!value || message;
};

/**
 * Меньше ли число заданного значения
 *
 * @param {number} max
 * @param {string} [message='Значение должно быть меньше {max}']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденной
 * если в качестве значения поступит null или не строка, или число
 * @returns {ValidationRule}
 */
const LessThen = (
  max: number,
  message = 'Значение должно быть меньше {max}',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { max });
  return (value: string | null): true | string => {
    if (value === null || !['string', 'number'].includes(typeof value)) {
      return !strict || formattedMessage;
    }

    return +value < max || formattedMessage;
  };
};

/**
 * Меньше либо равно ли число заданного значения
 *
 * @param {number} max
 * @param {string} [message='Значение должно быть меньше либо равно {max}']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденой
 * если в качестве значения  поступит null или не строка или число
 * @returns {ValidationRule}
 */
const LessThenOrEqual = (
  max: number,
  message = 'Значение должно быть меньше либо равно {max}',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { max });
  return (value: string | null): true | string => {
    if (value === null || !['string', 'number'].includes(typeof value)) {
      return !strict || formattedMessage;
    }

    return +value <= max || formattedMessage;
  };
};

/**
 * Больше ли число заданного значения
 *
 * @param {number} min
 * @param {string} [message='Значение должно быть больше {min}']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденой
 * если в качестве значения  поступит null или не строка, или число
 * @returns {ValidationRule}
 */
const GreaterThen = (
  min: number,
  message = 'Значение должно быть больше {min}',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { min });
  return (value: string | null): true | string => {
    if (value === null || !['string', 'number'].includes(typeof value)) {
      return !strict || formattedMessage;
    }

    return +value > min || formattedMessage;
  };
};

/**
 * Больше либо равно ли число заданного значения
 *
 * @param {number} min
 * @param {string} [message='Значение должно быть больше либо равно {min}']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденной
 * если в качестве значения поступит null или не строка, или число
 * @returns {ValidationRule}
 */
const GreaterThenOrEqual = (
  min: number,
  message = 'Значение должно быть больше либо равно {min}',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { min });
  return (value: string | null): true | string => {
    if (value === null || !['string', 'number'].includes(typeof value)) {
      return !strict || formattedMessage;
    }

    return +value >= min || formattedMessage;
  };
};

/**
 * Валидация длины значения
 *
 * @param {number} min
 * @param {string} [message='Длина значения должна быть больше или равна {min}']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденной
 * если в качестве значения поступит null или не массив, или строка
 * в общем то у чего "нет длинны"
 * @returns {ValidationRule}
 */
const MinLength = (
  min: number,
  message = 'Длина должна быть больше или равна {min}',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { min });
  return (value: Array<unknown> | string | null | unknown): true | string => {
    if (value === null || (!Array.isArray(value) && !(typeof value === 'string'))) {
      return !strict || formattedMessage;
    }

    return value.length >= min || formattedMessage;
  };
};

/**
 * Валидация длины значения
 *
 * @param {number} max
 * @param {string} [message='Длина значения должна быть меньше или равна {max}']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденной
 * если в качестве значения поступит null или не массив, или строка
 * в общем то у чего "нет длинны"
 * @returns {ValidationRule}
 */
const MaxLength = (
  max: number,
  message = 'Длина должна быть меньше или равна {max}',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { max });
  return (value: Array<unknown> | string | null | unknown): true | string => {
    if (value === null || (!Array.isArray(value) && !(typeof value === 'string'))) {
      return !strict || formattedMessage;
    }

    return value.length <= max || formattedMessage;
  };
};

/**
 * Валидация значения как целого числа
 *
 * @param {string} [message='Значение должно быть целым числом']
 * @param {boolean} [strict=false]
 * @returns {ValidationRule}
 */
const IsInteger = (
  message = 'Значение должно быть целым числом',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message);
  return (value: number | null): true | string => {
    console.debug('Validating ', value);
    if (value === null) {
      return !strict || formattedMessage;
    }
    return Number.isInteger(value) || formattedMessage;
  };
};

/**
 * Дата формата - _dd.mm.YYYY_
 *
 * @param {boolean} strict
 * @returns {ValidationRule}
 * @constructor
 */
const RussianDate = (strict = false): ValidationRule => {
  const formattedMessage = 'Дата должна быть в формате "dd.mm.YYYY"';
  return (value: string | null): true | string => {
    if (value === null) {
      return !strict || formattedMessage;
    }
    if (!/\d{2}\.\d{2}\.\d{4}/.test(value)) {
      return formattedMessage;
    }
    const d = parseRussianDate(value);
    return !Number.isNaN(d.getTime()) || formattedMessage;
  };
};

/**
 * Раньше ли дата заданного значения
 *
 * @param {number} max
 * @param {string} [message='Значение должно быть раньше "{max}"']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденой
 * если в качестве значения  поступит null
 * @returns {ValidationRule}
 */
const EarlierThen = (
  max: string,
  message = 'Значение должно быть раньше чем "{max}"',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { max: toRussianDate(max) as string });
  return (value: string | null): true | string => {
    if (value === null) {
      return !strict || formattedMessage;
    }
    const [a, b] = [toDate(value), toDate(max)];
    return a < b || formattedMessage;
  };
};

/**
 * Раньше дата, либо равна заданному значению
 *
 * @param {string} max
 * @param {string} [message='Значение должно быть раньше либо равно "{max}"']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденой
 * если в качестве значения  поступит null
 * @returns {ValidationRule}
 */
const EarlierThenOrExact = (
  max: string,
  message = 'Значение должно быть раньше либо равно "{max}"',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { max: toRussianDate(max) as string });
  return (value: string | null): true | string => {
    if (value === null) {
      return !strict || formattedMessage;
    }

    const [a, b] = [toDate(value), toDate(max)];
    console.debug(value, max, a, b);
    return a <= b || formattedMessage;
  };
};

/**
 * Позже ли дата заданного значения
 *
 * @param {string} min
 * @param {string} [message='Значение должно быть позднее чем "{min}"']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденой
 * если в качестве значения  поступит null
 * @returns {ValidationRule}
 */
const LaterThen = (
  min: string,
  message = 'Значение должно быть позднее чем "{min}"',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { min });
  return (value: string | null): true | string => {
    if (value === null) {
      return !strict || formattedMessage;
    }

    const [a, b] = [toDate(value), toDate(min)];
    return a > b || formattedMessage;
  };
};

/**
 * Позже ли дата либо равна заданному значению
 *
 * @param {string} min
 * @param {string} [message='Значение должно быть позднее чем, либо равно "{min}"']
 * @param {boolean} [strict=false]
 * стоит ли считать валидацию не пройденой
 * если в качестве значения  поступит null
 * @returns {ValidationRule}
 */
const LaterThenOrExact = (
  min: string,
  message = 'Значение должно быть позднее чем, либо равно "{min}"',
  strict = false
): ValidationRule => {
  const formattedMessage = formatValidationMessage(message, { min });
  return (value: string | null): true | string => {
    if (value === null) {
      return !strict || formattedMessage;
    }

    const [a, b] = [toDate(value), toDate(min)];
    return a >= b || formattedMessage;
  };
};

/**
 * Проверка служебного поля на валидность.
 * Может состоять только из латинских букв в нижнем регистре, цифр и символа «_»
 *
 * correct: hello_korzhik
 * @param message
 * @param strict
 * @returns
 */
const ValidSlug = (
  message = 'Данное поле может состоять только из латинских букв в нижнем регистре, цифр и симво «_»'
): ValidationRule => {
  return (value: string | null): true | string => {
    if (value === null) {
      return message;
    }

    return isValidSlug(value) || message;
  };
};

/**
 * Проверка значения на вхождение в список разрешенных
 *
 * @param {Array<string | number> | T} allowed
 * @param {string} message
 * @param {boolean} loose - использовать не строгое сравнение
 * при сравнении с разрешенными значениями
 * @param {boolean} strict
 * @returns {ValidationRule}
 * @constructor
 */
const In = <T extends Record<string, string | number>>(
  allowed: Array<string | number> | T,
  message = 'Значения нет в списке разрешенных.',
  loose = true,
  strict = false
): ValidationRule => {
  const formattedMessage = message;
  let allowedValues: Array<unknown>;
  if (Array.isArray(allowed)) {
    allowedValues = allowed;
  } else if (typeof allowed === 'object') {
    allowedValues = Object.values(allowed);
  }
  return (value: string | null): true | string => {
    if (value === null || !['string', 'number'].includes(typeof value)) {
      return !strict || formattedMessage;
    }
    let valid;
    if (loose) {
      // eslint-disable-next-line eqeqeq
      valid = allowedValues.some((v) => v == value);
    } else {
      valid = allowedValues.includes(value);
    }

    return valid || formattedMessage;
  };
};

/**
 * Валидатор для определения является ли значение
 * корректным регулярным выражением
 *
 * @param {boolean} strict
 * @returns {ValidationRule}
 * @constructor
 */
const ValidRegex = (strict = false): ValidationRule => {
  return (value): true | string => {
    if (!value && !strict) {
      return true;
    }
    try {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const r = new RegExp(value);
      return true;
    } catch {
      return 'Выражение не является корректным регулярным выражением';
    }
  };
};

/**
 * Correct: '5test_t', 'fd fd-fa'
 * Incorrect: '_qwe', ' asd', '1_fa -fa'
 *
 * @param str
 * @param allowEmpty
 * @returns
 */
export const isStringWithNumberInLowerCase = (
  str: string | null,
  allowEmpty = true
): boolean => {
  if (str) {
    const regexp = /^([\da-z]+[_\s-]?)+$/;
    return regexp.test(str);
  }
  return allowEmpty;
};

/**
 * Валидатор для проверки значения на удовлетворение регулярному выражению
 *
 * @param {string} pattern
 * @param {string} message
 * @param {boolean} strict
 * @returns {ValidationRule}
 * @constructor
 */
const CheckRegex = (
  pattern: string,
  message = 'Значение не соответствует регулярному выражению /{pattern}/',
  strict = false
): ValidationRule => {
  console.log(pattern);
  return (value: null | string): true | string => {
    console.log(value);
    if (!value && !strict) {
      return true;
    }
    const re = new RegExp(pattern);
    if (re.test(value as string)) {
      return true;
    }
    // const patternString = String(pattern);
    return formatValidationMessage(message, { pattern });
  };
};

/**
 *
 * @param {string} [message='Поле обязательно для заполнения']
 * @param strict
 * @returns
 */
const ValidEmail = (
  message = 'Необходимо корректно заполнить адрес электронной почты',
  strict = false
): ValidationRule => {
  return (value: string | null): true | string => {
    if (value === null) {
      return !strict || message;
    }
    return isValidEmail(value) || message;
  };
};

/**
 *
 * @param {string} [message='Необходимо коректно заполнить мобильный телефон']
 * @param strict
 * @returns
 */
const ValidMobilePhone = (
  message = 'Необходимо коректно заполнить мобильный телефон',
  strict = false
): ValidationRule => {
  return (value: string | null): true | string => {
    console.debug(value);
    if (value === null) {
      return !strict || message;
    }
    return isValidRuMobilePhone(value) || message;
  };
};

/**
 * Набор методов генерирующих правила валидации
 * для компонент формы фреймворка Quasar
 */
export default () => ({
  NotEmpty,
  LessThen,
  LessThenOrEqual,
  GreaterThen,
  GreaterThenOrEqual,
  MinLength,
  MaxLength,
  IsInteger,
  ValidEmail,
  CheckRegex,
  RussianDate,
  EarlierThen,
  EarlierThenOrExact,
  LaterThen,
  LaterThenOrExact,
  ValidSlug,
  In,
  ValidRegex,
  isStringWithNumberInLowerCase,
  ValidMobilePhone,
});
