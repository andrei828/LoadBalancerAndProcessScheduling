export function groupBy<T, K extends keyof any>(arr: T[], getKey: (item: T) => K) {
  return arr.reduce((previous, currentItem) => {
    const group = getKey(currentItem);
    if (!previous[group]) {
      previous[group] = [];
    }
    previous[group].push(currentItem);
    return previous;
  }, {} as Record<K, T[]>);
};

export function getMaxScrollTop(element: HTMLInputElement) {
  return element.scrollHeight - element.clientHeight;
}