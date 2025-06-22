<script lang="ts">
	import AppSidebar from '$lib/components/sidebar/app-sidebar.svelte';
	import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';
	import LoadingOverlay from '$lib/components/loading-overlay/loading-overlay.svelte';
	import type { PageProps } from './$types';
	import type { Airport, Chart } from './types.ts';
	import { PUBLIC_API_URI } from '$env/static/public';

	let { data }: PageProps = $props();

	const airportName: string = data.airportName;
	let airport: Airport = $state();
	let currentChart: Chart = $state();

	let chartsLoaded: boolean = $state(false);
	let chartSupplementLoaded: boolean = $state(false);
	let isLoaded: boolean = $derived(chartsLoaded && chartSupplementLoaded);

	const unableToLoadCharts = () => {
		toast.error(`Unable to Load Charts for ${airportName}`, {
			description: `No charts were found for ${airportName}. Please try searching again`,
			duration: Infinity,
			action: {
				label: 'Search Again',
				onClick: () => goto('/')
			}
		});
	};

	onMount(async () => {
		fetch(`${PUBLIC_API_URI}/charts?airport=${airportName}`)
			.then((response) => {
				if (!response.ok) {
					unableToLoadCharts();
				}

				return response.json();
			})
			.then((data) => {
				airport = {
					...airport,
					data: data.airport_data,
					charts: data.charts
				};

				let currentChartData: Chart = airport.charts.general[0];
				if (airport.charts.airport_diagram.length > 0) {
					currentChartData = airport.charts.airport_diagram[0];
				}

				currentChart = {
					name: currentChartData.chart_name,
					section: 'General',
					pdfUrl: currentChartData.pdf_url
				};

				chartsLoaded = true;
			});

		fetch(`${PUBLIC_API_URI}/charts/chart-supplement?airport=${airportName}`)
			.then((response) => response.json())
			.then((data) => {
				airport = {
					...airport,
					chartSupplement: data.charts
				};

				chartSupplementLoaded = true;
			});
	});
</script>

<LoadingOverlay doShow={!isLoaded} />

<Sidebar.Provider>
	<AppSidebar
		charts={isLoaded ? airport.charts : []}
		chartSupplement={isLoaded ? airport.chartSupplement : []}
		{isLoaded}
		bind:currentChart
	/>
	<Sidebar.Inset>
		<header class="bg-background sticky top-0 flex h-16 shrink-0 items-center gap-2 border-b px-4">
			<Sidebar.Trigger class="-ml-1" />
			<Separator orientation="vertical" class="mr-2 h-4" />
			<Breadcrumb.Root>
				<Breadcrumb.List>
					<Breadcrumb.Item>
						<Breadcrumb.Page
							>{isLoaded ? airport.data.airport_name : ''} ({isLoaded
								? airport.data.icao_ident
								: ''})</Breadcrumb.Page
						>
					</Breadcrumb.Item>
					<Breadcrumb.Separator />
					<Breadcrumb.Item>
						<Breadcrumb.Page>{isLoaded ? currentChart.section : ''}</Breadcrumb.Page>
					</Breadcrumb.Item>
					<Breadcrumb.Separator />
					<Breadcrumb.Item>
						<Breadcrumb.Page>{isLoaded ? currentChart.name : ''}</Breadcrumb.Page>
					</Breadcrumb.Item>
				</Breadcrumb.List>
			</Breadcrumb.Root>
		</header>
		<div class="flex flex-1 flex-col gap-4 p-4">
			<iframe
				title={isLoaded ? currentChart.name : 'Chart Loading'}
				src={isLoaded ? currentChart.pdfUrl : ''}
				frameborder="0"
				style="width:100%; height:100%"
			></iframe>
		</div>
	</Sidebar.Inset>
</Sidebar.Provider>
