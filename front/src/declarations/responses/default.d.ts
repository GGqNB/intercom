

export namespace Default {
  export interface DefaultResponse {
     id: number,
     key: string,
  }
}

export interface ResponceObject<T>{
  data: T;
  succsess: boolean;
}