<script lang="ts">
	import '../app.css';
	import type { Snippet } from 'svelte';
	import { ModeWatcher } from 'mode-watcher';
	import { Toaster } from '$lib/components/ui/sonner';

	interface Props {
		children: Snippet;
	}

	let { children }: Props = $props();
</script>

<svelte:head>
	<title>AviationAPI</title>
</svelte:head>

<Toaster richColors position="top-center" />
<ModeWatcher />

<div class="min-h-screen">
	{@render children()}
</div>
