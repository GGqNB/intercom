export function offset(el: Window & typeof globalThis) {
  if (el === window) {
    return { top: 0, left: 0 };
  }
  // @ts-ignore
  const { top, left } = el.getBoundingClientRect();
  return { top, left };
}

export function style(el: Element, property: string) {
  // @ts-ignore
  return window.getComputedStyle(el).getPropertyValue(property);
}

export function height(el: Window & typeof globalThis) {
  // @ts-ignore
  return el === window ? window.innerHeight : el.getBoundingClientRect().height;
}

export function width(el: Window & typeof globalThis) {
  // @ts-ignore
  return el === window ? window.innerWidth : el.getBoundingClientRect().width;
}

export function goUrl(url: string) {
  window.location.href = url;
}
