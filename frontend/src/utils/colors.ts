// Category color mapping
const categoryColors: Record<string, string> = {
  'ai-&-machine-learning': 'rgb(99, 102, 241)', // indigo
  'core-infrastructure': 'rgb(168, 85, 247)', // purple
  'data-services': 'rgb(14, 165, 233)', // sky
  'defi-&-trading': 'rgb(239, 68, 68)', // red
  'scientific-computing': 'rgb(16, 185, 129)', // emerald
  'uncategorized': 'rgb(234, 179, 8)', // yellow
  'security-&-trust': 'rgb(249, 115, 22)', // orange
  'default': 'rgb(99, 102, 241)' // fallback
};

export const getCategoryColor = (categoryId: string): string => {
  return categoryColors[categoryId] || categoryColors.default;
};