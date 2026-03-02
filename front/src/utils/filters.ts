import { toRussianLocaleDateFromIso, toRussianLocaleDateTimeTzFromIso } from './datetime';

/*
  Vue фильтра
*/

const isNumber = (value: any) => !Number.isNaN(Number(value));

export const toFloatNumber = (num: any, fracDigits = 4): string | number => {
  if (isNumber(num)) {
    return Number(num).toFixed(fracDigits);
  }
  return num;
};

export const humanDateTime = (date: string): string =>
  toRussianLocaleDateFromIso(date, {
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
  });

export const humanDateTimeTz = (date: string): string =>
  toRussianLocaleDateTimeTzFromIso(date, {
    hour: 'numeric',
    minute: 'numeric',
    second: 'numeric',
  });
