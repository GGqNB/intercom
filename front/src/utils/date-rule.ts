import { date } from 'quasar';

export const DISPLAY_DATE_REGEX_STR = '(0[1-9]|[12][0-9]|3[01])[\\.](0?[1-9]|1[012])[\\.]\\d{4}';

export const DISPLAY_DATE_REGEX = new RegExp(`^${DISPLAY_DATE_REGEX_STR}$`);

export const DISPLAY_DATE_RANGE_REGEX = new RegExp(
  `^(${DISPLAY_DATE_REGEX_STR})?[ ]*(-[ ]*${DISPLAY_DATE_REGEX_STR})?$`
);

export const dateRule = (v: string) => {
  if (v) return DISPLAY_DATE_REGEX.test(v) || 'Некорректный формат даты';
  return true;
};

export const dateRangeRule = (v: string) => {
  if (v) return DISPLAY_DATE_RANGE_REGEX.test(v) || 'Некорректный формат даты';
  return true;
};

export function dateDisplayToInternal(displayValue: string | null): string | null {
  if (displayValue && DISPLAY_DATE_REGEX.test(displayValue)) {
    return date.formatDate(date.extractDate(displayValue, 'DD.MM.YYYY'), 'YYYY-MM-DD');
  }
  return null;
}

export function dateInternalToDisplay(internalValue: string | null): string | null {
  if (internalValue) {
    return date.formatDate(date.extractDate(internalValue, 'YYYY-MM-DD'), 'DD.MM.YYYY');
  }
  return null;
}

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
