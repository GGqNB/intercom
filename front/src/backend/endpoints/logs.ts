import { IEndpointData } from 'src/backend/endpoint';
import { API_SERVER } from 'src/constants/common';

const url = `${API_SERVER}api/logs`;


export const LOGS = {
  LIST: {
    method: 'GET',
    url: `${url}/redis-intercom`,
  } as IEndpointData,
  CLEAR: {
    method: 'GET',
    url: `${url}/redis-intercom`,
  } as IEndpointData,
}