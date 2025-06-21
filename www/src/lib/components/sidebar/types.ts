import type { Chart, Charts } from '$app/routes/charts/types.ts';

export interface Section {
	name: string;
	charts: [Chart];
}

export interface Props {
	charts: Charts;
	chartSupplement: [Chart];
	isLoaded: boolean;
	currentChart: Chart;
}
