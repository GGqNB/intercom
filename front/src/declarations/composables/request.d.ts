export interface MakeRequestOptions {
  useLoader: boolean;
  catchErrors: boolean;
  skipHttpCodes: Array<number>;
  dontAlert: boolean | Array<unknown>;
  reThrow: boolean;
  defaultMessage: string;
  startLoading?: () => Promise<void> | void;
  finishLoading?: () => Promise<void> | void;
}
