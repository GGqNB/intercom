import { useQuasar } from "quasar";
import { computed, ComputedRef } from "vue";

export function useDeviceSizes() {
  const $q = useQuasar();

  const isMobile: ComputedRef<boolean> = computed(() => $q.screen.lt.sm);

  const isLaptop: ComputedRef<boolean> = computed(() => $q.screen.lt.md);

  const isDesktop: ComputedRef<boolean> = computed(() => $q.screen.lt.lg);

  const isMoreDesktop: ComputedRef<boolean> = computed(() => $q.screen.lt.xl);

  return {
    isMobile,
    isLaptop,
    isMoreDesktop,
    isDesktop,
  }
}
