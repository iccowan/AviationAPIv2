<script lang="ts">
	import * as Card from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Github } from '@lucide/svelte';
	import { MessageCircle } from '@lucide/svelte';
	import { FileText } from '@lucide/svelte';
	import { HandCoins } from '@lucide/svelte';
	import { LinkWithPopup } from '$lib/components/link-with-popup';
	import { goto } from '$app/navigation';

	let airport: string = $state('');

	const submitAirport = (event: HTMLFormElement) => {
		event.preventDefault();
		goto(`/charts?airport=${airport}`);
	};
</script>

<div class="flex min-h-screen min-w-screen flex-col items-center justify-center align-middle">
	<img
		class="mb-4 hidden w-70 object-contain dark:block"
		src="/logos/aviationapi-dark.svg"
		alt="#"
	/>
	<img class="mb-4 block w-70 object-contain dark:hidden" src="/logos/aviationapi.svg" alt="#" />
	<Card.Root class="mx-4 w-3/4 text-center md:w-1/2 lg:w-1/3">
		<Card.Header>
			<Card.Title>Search for Charts</Card.Title>
		</Card.Header>
		<Card.Content>
			<form onsubmit={submitAirport}>
				<div class="mb-5 flex justify-center">
					<Input
						bind:value={airport}
						placeholder="Airport ICAO (i.e. KATL)"
						class="w-1/2 text-center"
					/>
				</div>
				<Button type="submit" class="cursor-pointer">Search</Button>
			</form>
		</Card.Content>
		<Card.Footer class="text-muted-foreground justify-center text-sm">
			<LinkWithPopup
				text="Open Source on GitHub"
				href="https://github.com/iccowan/AviationAPIv2"
				Icon={Github}
			/>
			&bull;
			<LinkWithPopup
				text="Join the Conversation on Discord"
				href="https://discord.gg/CWRGN4DStU"
				Icon={MessageCircle}
			/>
			&bull;
			<LinkWithPopup
				text="API Documentation for Developers"
				href="https://api-v2.aviationapi.com/v2/docs"
				Icon={FileText}
			/>
			&bull;
			<LinkWithPopup
				text="Donate to Support AviationAPI"
				href="https://www.aviationapi.com/donate"
				Icon={HandCoins}
			/>
		</Card.Footer>
	</Card.Root>
	<div class="w-3/4 text-center md:w-1/2 lg:w-1/3">
		<p class="text-muted-foreground mt-2 text-sm italic">
			Use with caution. AviationAPI is not responsible for any misuse of outdated charts or other
			information as it is intended for flight simulation use. Please confirm the cycle dates prior
			to use of any data.
		</p>
	</div>
</div>
