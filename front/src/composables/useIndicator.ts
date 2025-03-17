/* eslint-disable no-undef */
/* eslint-disable @typescript-eslint/no-unused-vars */
import { computed, Ref, ref } from 'vue';
import { useIndicatorStore } from 'stores/indicator.store';
import { UserInfo } from 'AdminDir/declarations/access';

export function useIndicator() {
  const indicatorStore = useIndicatorStore();

  const indicatorDataSet = {
    setActivePhone(val : boolean) {
      indicatorStore.setActivePhone(val);
    },
    setActiveWifi(val : boolean) {
      indicatorStore.setActiveWifi(val);
    },
    setCurrentNetwork(val : string) {
      indicatorStore.setCurrentNetwork(val);
    },
    setPastNetworks(val : string) {
      indicatorStore.setPastNetworks(val);
    },
    getActivePhone() {
     return indicatorStore.watchActivePhone;
    },
    getActiveWifi() {
      return indicatorStore.watchActiveWifi;
     },
     getCurrentNetwork() {
      return indicatorStore.watchCurrentNetwork;
     },
     getPastNetwork() {
      return indicatorStore.watchPastNetworks;
     },
  };

  return {
    indicatorDataSet
  };
}
