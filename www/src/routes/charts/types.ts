export interface AirportData {
	icao_ident: string;
	airport_name: string;
}

export interface Charts {
	airport_diagram: [Chart];
	general: [Chart];
	departure: [Chart];
	arrival: [Chart];
	approach: [Chart];
}

export interface Chart {
	chart_name: string;
	pdf_name: string;
	pdf_url: string;
	did_change: boolean;
	change_pdf_name: string;
	change_pdf_url: string;
	section: string;
}

export interface Airport {
	data: AirportData;
	charts: Charts;
	chartSupplement: [Chart];
}
