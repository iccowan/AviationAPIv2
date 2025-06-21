<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { ArrowBigLeft } from '@lucide/svelte';
</script>

<img class="hidden p-5 dark:block" src="/logos/aviationapi-dark.svg" alt="#" />
<img class="block p-5 dark:hidden" src="/logos/aviationapi.svg" alt="#" />

<Button href="/"><ArrowBigLeft />New Search</Button>
