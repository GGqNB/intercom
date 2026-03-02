import { IEndpointData } from 'src/backend/endpoint';
import { API_SERVER } from 'src/constants/common';

const url = `${API_SERVER}api`;


export const INTERCOM_CALL = {
  CALL: {
    method: 'POST',
    url: `${url}/call`,
  } as IEndpointData,
  ANSWER_CALL(apartment_number: number): IEndpointData {
      return {
        method: 'GET',
        url: `${url}/answer_call/${apartment_number}`,
      };
    },
  ABORT_CALL(apartment_number: number): IEndpointData {
      return {
        method: 'GET',
        url: `${url}/abort_call/${apartment_number}`,
      };
    },
    OPEN(lock_id: number, code: string, local_url_base: string): IEndpointData {
        return {
          method: 'GET',
          url: `${url}/stown/open/${lock_id}/${code}/${local_url_base}`,
        };
      },
  ACTIVE_CALLS: {
      method: 'GET',
      url: `${url}/active_calls`,
    } as IEndpointData,
};


