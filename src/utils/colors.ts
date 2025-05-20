// Category color mapping
const categoryColors: Record<string, string> = {
  'genai': 'rgb(99, 102, 241)', // indigo
  'training': 'rgb(16, 185, 129)', // emerald
  'modeldev': 'rgb(14, 165, 233)', // sky
  'predictions': 'rgb(249, 115, 22)', // orange
  'infra': 'rgb(168, 85, 247)', // purple
  'defi': 'rgb(239, 68, 68)', // red
  'aitool': 'rgb(234, 179, 8)', // yellow
  'default': 'rgb(99, 102, 241)' // default to indigo
};

export const getCategoryColor = (categoryId: string): string => {
  return categoryColors[categoryId] || categoryColors.default;
};