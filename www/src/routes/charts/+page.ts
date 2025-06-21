import type { PageLoad } from './$types';

export const load: PageLoad = ({ _params, url }) => {
	const airportName: string = url.searchParams.get('airport');
	return { airportName };
};
