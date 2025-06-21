<script lang="ts">
	import Header from './sidebar-header.svelte';
	import * as Collapsible from '$lib/components/ui/collapsible/index.js';
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import ChevronRightIcon from '@lucide/svelte/icons/chevron-right';
	import type { ComponentProps } from 'svelte';
	import type { Section, Props } from './types.ts';

	let {
		ref = $bindable(null),
		charts,
		chartSupplement,
		isLoaded,
		currentChart = $bindable(),
		...restProps
	}: ComponentProps<typeof Sidebar.Root> & Props = $props();

	let sections: [Section] = $derived.by(() => {
		if (isLoaded) {
			return [
				{
					name: 'General',
					charts: [
						...charts.airport_diagram,
						...charts.general,
						{ chart_name: 'CHART SUPPLEMENT', ...chartSupplement[0] }
					]
				},
				{ name: 'Departure Procedures', charts: charts.departure },
				{ name: 'Arrival Procedures', charts: charts.arrival },
				{ name: 'Approach Procedures', charts: charts.approach }
			];
		}

		return [
			{ name: 'General', charts: [] },
			{ name: 'Departure Procedures', charts: [] },
			{ name: 'Arrival Procedures', charts: [] },
			{ name: 'Approach Procedures', charts: [] }
		];
	});

	const updateCurrentChart = (chart: Chart, sectionName: string) => {
		currentChart = {
			name: chart.chart_name,
			section: sectionName,
			pdfUrl: chart.pdf_url
		};
	};
</script>

<Sidebar.Root bind:ref {...restProps}>
	<Sidebar.Header>
		<Header />
	</Sidebar.Header>
	<Sidebar.Content class="gap-0">
		{#each sections as section (section.name)}
			{#if section.charts.length > 0}
				<Collapsible.Root
					title={section.name}
					open={section.name == 'General'}
					class="group/collapsible"
				>
					<Sidebar.Group>
						<Sidebar.GroupLabel
							class="group/label text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground cursor-pointer text-sm"
						>
							{#snippet child({ props })}
								<Collapsible.Trigger {...props}>
									{section.name}
									<ChevronRightIcon
										class="ml-auto transition-transform group-data-[state=open]/collapsible:rotate-90"
									/>
								</Collapsible.Trigger>
							{/snippet}
						</Sidebar.GroupLabel>
						<Collapsible.Content>
							<Sidebar.GroupContent>
								<Sidebar.Menu>
									{#each section.charts as chart (chart.chart_name)}
										<Sidebar.MenuItem>
											<Sidebar.MenuButton
												isActive={currentChart.name == chart.chart_name}
												onclick={() => updateCurrentChart(chart, section.name)}
												class="cursor-pointer"
											>
												{#snippet child({ props })}
													<p href="" {...props}>{chart.chart_name}</p>
												{/snippet}
											</Sidebar.MenuButton>
										</Sidebar.MenuItem>
									{/each}
								</Sidebar.Menu>
							</Sidebar.GroupContent>
						</Collapsible.Content>
					</Sidebar.Group>
				</Collapsible.Root>
			{/if}
		{/each}
	</Sidebar.Content>
	<Sidebar.Rail />
</Sidebar.Root>
