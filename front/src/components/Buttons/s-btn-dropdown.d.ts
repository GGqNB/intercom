export namespace BtnDropdown {
  export interface Items {
    index: number;
    label: string;
    event: string;
  }

  export type BtnSizes =
    | 'base'
    | 'base-small'
    | 'base-medium'
    | 'base-large'
    | 'base-xl'
    | 'base-xxl'
    | 'base-xxxl'
    | 'small'
    | 'medium'
    | 'large';
}
