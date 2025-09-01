// eslint-disable-next-line @typescript-eslint/no-unused-vars
import * as dotenv from 'dotenv';
//for deploy
export const URL_SERVER = String(process.env.SERVER_URL);

export const API_SERVER = String('https://'+process.env.SERVER_URL);

export const WSS_SERVER = String('ws    s://' + process.env.SERVER_URL + 'ws');

export const VIDEO_SERVER = String(process.env.VIDEO_SERVER);

export const API_KEY = String(process.env.KEY);
export const WEBRTC_KEY = String(process.env.WEBRTC_KEY);

