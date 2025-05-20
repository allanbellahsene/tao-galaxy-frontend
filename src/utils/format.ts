// Format numbers to K, M, B format
export const formatNumber = (num: number): string => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1);
  }
  return num.toString();
};

// Format large numbers with commas
export const formatWithCommas = (num: number): string => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};