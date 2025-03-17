import { useQuasar } from "quasar";


export function setScreenSizes(sm = 300, md = 500, lg = 750, xl = 1000) {
  const q = useQuasar();
  q.screen.setSizes({
    sm: sm,
    md: md,
    lg: lg,
    xl: xl,
  });

  return {
    q,
  }
}
