// import formatISO from 'date-fns/formatISO';
// import addHours from 'date-fns/addHours';
// import startOfHour from 'date-fns/startOfHour';

export const MILLISECONDS_IN_DAY = 86400000;
export const MILLISECONDS_IN_HOUR = 3600000;
export const MILLISECONDS_IN_MINUTE = 60000;
export const SECONDS_IN_MINUTE = 60;
export const SECONDS_IN_HOUR = 3600;

// Маска для времени
export const timeMask = '##:##';

// Маска для даты
export const dateMask = '##.##.####';

// Формат iso
export const maskFormatIso = 'YYYY-MM-DD';

// Параметры по умолчанию дляя компоненты QDateTimeInput
export const dateTimeInputProps = {
  readonly: false,
  outlined: true,
  dense: true,
  'hide-bottom-space': true,
  required: true,
  maskDate: dateMask,
  maskTime: timeMask,
  dateRules: [
    (val: string) => !!val || 'Необходимо указать дату!',
    (val: string) => val.length === dateMask.length || 'Необходимо указать корректную дату',
  ],
  timeRules: [
    (val: string) => !!val || 'Необходимо указать время!',
    (val: string) => val.length === timeMask.length || 'Необходимо указать корректное время',
  ],
};

/**
 * Проверка на то больше ли первая дата чем вторая
 *
 * @param firstDate
 * @param secondDate
 * @returns
 */
export const isFirstDateMoreThenSecond = (firstDate: Date, secondDate: Date): boolean =>
  +firstDate > +secondDate;

/**
 * Переводим из строки времени UTC (ISO) вида 2021-05-25T06:51:56.567000
 * В локальное время с добавлением соответствующей временной зоны
 *
 * @param date
 * @returns
 */
export const convertUTCToLocal = (date: string | Date): Date => {
  if (typeof date === 'string') {
    const utcDate = new Date(date);
    const newDate = new Date(utcDate.getTime() - utcDate.getTimezoneOffset() * 60 * 1000);
    return newDate;
  }
  const utcDate = date;
  const localDate = new Date(utcDate);
  return localDate;
};

/**
 * Преобразовать объект типа Date (UTC) в формат ISO с сохранением временной зоны
 * Также обрезается временная зона
 *
 * @param date
 * @returns
 */
export const convertToIsoLocal = (date: Date): string =>
  new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().replace('Z', '');

/**
 * Количество минут между двумя датами
 * @param a
 * @param b
 * @returns
 */
export const minutesBetweeenDates = (a: Date, b: Date): number =>
  Math.round((a.getTime() - b.getTime()) / 60000);

/**
 * Перевод даты из iso8601 в отечественный формат даты
 *
 * @param d
 * @param options
 * @returns
 */
export const toRussianLocaleDateFromIso = (
  d: string,
  options: Intl.DateTimeFormatOptions = {}
): string => {
  const russianDate = new Date(d).toLocaleString('ru', {
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    ...options,
  });
  return russianDate;
};

/**
 * Перевод даты из iso8601 в локальный формат даты и времени
 *
 * @param d
 * @param options
 * @returns
 */
export const toRussianLocaleDateTimeFromIso = (
  d: string,
  options: Intl.DateTimeFormatOptions = {}
): string => {
  const russianDate = new Date(d).toLocaleString('ru', {
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    ...options,
  });
  return russianDate;
};

/**
 * Перевод даты из iso8601 в локальный формат даты и времени
 * c выставлением временной зоны
 *
 * @param d
 * @param options
 * @returns
 */
export const toRussianLocaleDateTimeTzFromIso = (
  d: string,
  options: Intl.DateTimeFormatOptions = {}
): string => {
  const russianDate = convertUTCToLocal(d).toLocaleString('ru', {
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    ...options,
  });
  return russianDate;
};

// export const formatToIsoDate = (d: Date | string): string => {
//   const newDate = new Date(d);
//   return formatISO(newDate, { representation: 'date' });
// };

/**
 * Добавляем к текущей дате определенное количество часов
 * округляем до заданной даты
 *
 * @param hour
 * @returns
 */
// export const generateDatetimeFromCurrent = (hour = 2): Date => {
//   const date = startOfHour(addHours(new Date(), hour));
//   return date;
// };

/**
 * Метод меняет формат даты `DD.MM.YYYY` <=> `YYYY-MM-DD`
 *
 * @param dateIn
 * @param currentFormat
 * @returns
 */
export const dateFormatSwitcher = (
  dateIn: string,
  currentFormat: 'DD.MM.YYYY' | 'YYYY-MM-DD'
): string => {
  const err = new TypeError(
    'Неопознанные формат даты, принимается либо "YYYY-MM-DD", либо "DD.MM.YYYY"'
  );
  if (dateIn.length !== 10) {
    throw err;
  }
  let original: string;
  let replacer: string;
  if (currentFormat === 'DD.MM.YYYY') {
    original = '.';
    replacer = '-';
  } else {
    original = '-';
    replacer = '.';
  }

  const parts = dateIn.split(original);

  if (parts.length !== 3) {
    throw err;
  }

  return parts.reverse().join(replacer);
};

/**
 * Смещаем дату в другую временную зону.
 * По умолчанию используется зона смещаемой даты,
 * так же можно указать смещение в минутах.
 *
 * @param {Date} date
 * @param {number} offset
 * @returns {Date}
 */
export const castDateToLocalTimezone = (date: Date, offset?: number): Date => {
  if (!offset) {
    // eslint-disable-next-line no-param-reassign
    offset = date.getTimezoneOffset();
  }
  const copy = new Date(date.getTime() - offset * 60 * 1000);
  return copy;
};

export const getOnlyDate = (date: string | Date | null): string => {
  if (typeof date === 'string') {
    // eslint-disable-next-line no-param-reassign
    date = new Date(date);
  }
  if (date instanceof Date) {
    const [y, m, d] = [date.getFullYear(), date.getMonth() + 1, date.getDate()];
    const leadingZero = m > 9 ? '' : '0';
    return `${y}-${leadingZero}${m}-${d}`;
  }
  return '';
};

/**
 * Формирует нативный объект Date
 * из строки с русским форматом даты - `dd.mm.YYYY`
 *
 * @param {string} value
 * @returns {Date}
 */
export const parseRussianDate = (value: string): Date => {
  const [day, month, year] = value.split('.');
  return new Date(+year, +month, +day);
};

export const toRussianDate = (value: null | string | Date) => {
  if (!value) {
    return null;
  }
  const date = value instanceof Date ? value : new Date(value);
  return date.toLocaleDateString();
};
