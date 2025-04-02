import { ref, onBeforeUnmount } from 'vue';

export function useTimeout(callback, delay) {
  const timeoutId = ref(null);
  const isActive = ref(false);

  const start = () => {
    isActive.value = true;
    timeoutId.value = setTimeout(() => {
      callback();
      isActive.value = false; 
    }, delay);
  };

  const clear = () => {
    if (timeoutId.value) {
      clearTimeout(timeoutId.value);
      timeoutId.value = null;
      isActive.value = false;
    }
  };

  onBeforeUnmount(clear); 

  return { start, clear, isActive };
}
