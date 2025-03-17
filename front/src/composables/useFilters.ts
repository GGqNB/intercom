/* eslint-disable @typescript-eslint/ban-ts-comment */
import { cloneDeep, isEqual } from 'lodash';
import { NFilters } from 'src/declarations/filters';
import { computed, Ref, UnwrapRef } from 'vue';

/**
 * Метод "стерелизации" значений фильтрав
 *
 * Создан для того что бы приводить исключать "пустые" (которые пустые с точки зрения логики, но не пустые с технической точки зрения)
 * Например бинарный фильтр (_checkbox_):
 *
 * Логиего применения заключается в том что, когда он применен
 * то он должен присутствовать в наборе фильтров, а когда нет, то должен отсутствовать
 * но в реальном мире _checkbox_ работает, немног не так нужно.
 * И значение переменной из этого чекбокса будет либо истина либо ложь
 *
 * Как раз для этого (очищение набора фильтров от "пустых" значений), это функция и нужна.
 * Так же работвет в обратном порядке, когда нужно "пустые" значения скастить к реальным значения
 * компонент приложения
 *
 * Правила следующие:
 *  - `boolean`: `false` _=>_ `undefined`
 *  - `array`: `[]` _=>_ `undefined`
 *  - `number`: ` null | ''` _=>_ `undefined`
 *  - `date`: `null | ''` _=>_ `undefined`
 *  - `string`: `null | ''` _=>_ `undefined`
 *
 * @param {null | boolean | Array<number> | string | number} value
 * @param {NFilters.FilterDeclaration<NFilters.BaseFilter>} filterItem - декларация фильтра,
 * объект который содержит его "синтетический" тип
 * @param {boolean} reverse [default=false]
 * @returns
 */
export const sanitize = (
  value: null | boolean | Array<number> | string | number,
  filterItem: NFilters.FilterDeclaration<NFilters.BaseFilter>,
  reverse = false
): null | boolean | Array<number> | string | number | undefined => {
  if (filterItem.valueType === 'boolean') {
    if (reverse) {
      return typeof value === 'undefined' ? false : value;
    }
    return value === true ? value : undefined;
  }
  if (filterItem.valueType === 'array' && Array.isArray(value)) {
    if (reverse) {
      return typeof value === 'undefined' ? [] : value;
    }
    return value.length !== 0 ? value : undefined;
  }
  if (filterItem.valueType === 'number') {
    if (reverse) {
      return typeof value === 'undefined' ? null : value;
    }
    return ![null, ''].includes(value as string | null) ? value : undefined;
  }
  if (filterItem.valueType === 'date') {
    if (reverse) {
      return typeof value === 'undefined' ? null : value;
    }
    return ![null, ''].includes(value as string | null) ? value : undefined;
  }
  if (filterItem.valueType === 'string') {
    if (reverse) {
      return typeof value === 'undefined' ? null : value;
    }
    return ![null, ''].includes(value as string | null) ? value : undefined;
  }

  return undefined;
};
/**
 * Метод определяет какие из переданных значений
 * отличаются от значений по умолчанию
 *
 * Посредством перебирания значений текущего фильтра
 * и сравнением его со значением по-умолчанию
 *
 * В зависимости от _режима сравнения_ оно может быть строгим или нет
 *
 * @param {Record<string, unknown>} currentFilters
 * @param {Record<string, unknown>} defaultFilters
 * @param {boolean} strict [default=true] Использовать ли строгое сравнение значений
 * @returns
 */
export const countAppliedFilters = (
  currentFilters: Record<string, unknown>,
  defaultFilters: Record<string, unknown>,
  strict = true
): Array<string> => {
  const appliedFilters: Array<string> = [];
  Object.entries(currentFilters).forEach(([filterName, filterValue]) => {
    if (strict) {
      // if (filterValue !== defaultFilters[filterName]) {
      if (!isEqual(filterValue, defaultFilters[filterName])) {
        appliedFilters.push(filterName);
      }
      return;
    }
    // нестрогое сравнение здесь использовано
    // намеренно с полным пониманием всей опасности
    // eslint-disable-next-line eqeqeq
    if (filterValue != defaultFilters[filterName]) {
      appliedFilters.push(filterName);
    }
  });
  return appliedFilters;
};

/**
 *
 * @param {NFilters.FilterSet<F>} filters
 * @param {Array<keyof NFilters.FilterValue<F>>} excludeIfEmpty Список фильтров которые необходимо очищать при передаче
 * наружу компоненты и при получении из вне (смотри документацию функции `sanitize`) {@link sanitize}
 * @returns {{sanitizeSet: (value: NFilters.FilterValue<F>, reverse?: boolean) => NFilters.FilterValue<F>}}
 */
export default <F extends NFilters.BaseFilter>(
  filters: NFilters.FilterSet<F>,
  excludeIfEmpty: Array<keyof NFilters.FilterValue<F>> = []
) => {
  const filtersByName = Object.fromEntries(filters.map((f) => [f.name, f]));
  /**
   * Очищаем значение набора фильтров от "пустых",
   * либо проводим обратную операцию, что бы записать значение
   * фильтров из внешнего источника (бекэнд))
   *
   * (смотри документацию функции `sanitize`)
   *
   * {@link sanitize}
   *
   * @param value
   * @param reverse
   * @returns
   */
  const sanitizeValue = (
    value: NFilters.FilterValue<F>,
    reverse = false
  ): NFilters.FilterValue<F> => {
    const clone = cloneDeep(value);

    excludeIfEmpty.forEach((filterName) => {
      // SORRY: по другому быстро не получилось исправить
      // @ts-ignore
      clone[filterName] = sanitize(clone[filterName], filtersByName[filterName] as any, reverse);
    });
    return clone;
  };

  /**
   *
   * @param {Ref<UnwrapRef<NFilters.FilterValue<F>>>} filtersValue
   * @param {NFilters.FilterValue<F>} defaultFiltersValue
   * @returns {{appliedFilters: ComputedRef<Array<string>>, appliedFiltersCount: ComputedRef<number>}}
   */
  const watchApplied = (
    filtersValue: Ref<UnwrapRef<NFilters.FilterValue<F>>>,
    defaultFiltersValue: NFilters.FilterValue<F>
  ) => {
    /**
     *
     * @type {ComputedRef<Array<string>>}
     */
    const appliedFilters = computed(() =>
      countAppliedFilters(filtersValue.value as Record<string, unknown>, defaultFiltersValue, false)
    );

    /**
     *
     * @type {ComputedRef<number>}
     */
    const appliedFiltersCount = computed(() => appliedFilters.value.length);

    return {
      appliedFilters,
      appliedFiltersCount,
    };
  };

  return {
    sanitizeValue,
    watchApplied,
  };
};
