export namespace Network {
  export interface NetworkBrief {
    connected: boolean,
    ssid: string,
    signal: number,
    security: string,
  }

  export interface NetworkActiveBrief {
    name: boolean,
    type: string,
  }

  export interface NetworkBare {
    ssid: string;
    password: string;

  }

  export interface NetworkConnections{
    name: string,
    type: string,
  }

}
