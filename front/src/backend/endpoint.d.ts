export interface IEndpointData {
  method:
    | 'GET'
    | 'POST'
    | 'DELETE'
    | 'PUT'
    | 'get'
    | 'delete'
    | 'head'
    | 'HEAD'
    | 'options'
    | 'OPTIONS'
    | 'post'
    | 'put'
    | 'patch'
    | 'PATCH'
    | 'purge'
    | 'PURGE'
    | 'link'
    | 'LINK';
  url: string;
}

export interface CRUDEndpointCollection {
  LIST: IEndpointData;
  LIST_BRIEF?: IEndpointData;
  GET: (id: number) => IEndpointData;
  STORE: IEndpointData;
  UPDATE: (id: number) => IEndpointData;
  DELETE: (id: number) => IEndpointData;
}
