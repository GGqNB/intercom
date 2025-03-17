/* eslint-disable @typescript-eslint/ban-types */
import { ref } from "vue";

export function useTimer(){
    const touchTimer = ref(null);
    const longTouch = (nextFunc: Function, nfcData) => {
        touchTimer.value = setTimeout(() => {
            nextFunc(nfcData);
        }, 600); // Задержка в миллисекундах (в данном случае 600 мс)
        };
        const endLongTouch = () => {
            clearTimeout(touchTimer);
        }

       return{
        longTouch,
        endLongTouch
       } 
}