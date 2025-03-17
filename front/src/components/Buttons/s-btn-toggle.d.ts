export namespace ButtonToggles {
  export type ToggleBtnVariants =
    | 'main';

  export type ToggleBtnOption = {
    attrs?: any;
    label?: string | undefined;
    icon?: string | undefined;
    value: any;
    slot?: string | undefined;
  }

  export type ToggleBtnStyles = {
    variant: string;
    toggleColor: string;
    color: string;
    textColor: string;
  }
}
