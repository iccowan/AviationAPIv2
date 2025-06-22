<script lang="ts">
	import * as HoverCard from '$lib/components/ui/hover-card';
	import type { Component } from 'svelte';

	interface LinkWithPopupProps {
		text: string;
		href: string;
		Icon: Component;
	}

	let { text = '', href = '', Icon }: LinkWithPopupProps = $props();
</script>

<div class="mx-2">
	<HoverCard.Root>
		<HoverCard.Trigger {href} target="_blank">
			<Icon />
		</HoverCard.Trigger>
		<HoverCard.Content class="w-auto">
			<p class="text-muted-foreground text-center text-sm">
				{text}
			</p>
		</HoverCard.Content>
	</HoverCard.Root>
</div>
