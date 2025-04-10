import xml.etree.ElementTree as ElementTree
from app.lib.models.Airport import Airport
from app.lib.models.Chart import Chart

def main():
    with open("temp/data/DDTPPE_250417/d-TPP_Metafile.xml") as file:
        airac = '250417'
        START_EVENT = 'start'
        END_EVENT = 'end'
        document = ElementTree.iterparse(file, [START_EVENT, END_EVENT])

        current_airport = Airport(airac)
        current_chart = Chart()
        current_chart_section = ''
        skip_chart = False
        chart_change = False

        for event, element in document:
            tag = element.tag.strip()
            text = element.text.strip() if element.text is not None else ''

            if event == START_EVENT and tag == 'state_code':
                current_airport.airport_data.state = element.attrib['ID']
                current_airport.airport_data.state_full = element.attrib['state_fullname']
            if event == START_EVENT and tag == 'city_name':
                current_airport.airport_data.city = element.attrib['ID']
            if event == START_EVENT and tag == 'airport_name':
                current_airport.airport_data.airport_name = element.attrib['ID']
                current_airport.airport_data.faa_ident = element.attrib['apt_ident']
                current_airport.airport_data.icao_ident = element.attrib['icao_ident']
                current_airport.airport_data.is_military = element.attrib['military'] == 'M'
            if event == END_EVENT and tag == 'chartseq':
                current_chart.chart_sequence = text
            if event == END_EVENT and tag == 'chart_name':
                current_chart.chart_name = text
            if event == END_EVENT and tag == 'pdf_name':
                if '_C' in text:
                    skip_chart = True

                current_chart.pdf_name = text
                current_chart.pdf_url = f'https://charts-sandbox.aviationapi.com/{airac}/{text}'
            if event == END_EVENT and tag == 'cn_flg':
                chart_change = text == 'Y'
            if event == END_EVENT and tag == 'chart_code':
                match text:
                    case 'APD':
                        current_chart_section = Airport.CHART_SECTIONS['airport_diagram']
                    case 'DP' | 'DAU':
                        current_chart_section = Airport.CHART_SECTIONS['departure']
                    case 'STAR':
                        current_chart_section = Airport.CHART_SECTIONS['arrival']
                    case 'IAP' | 'CVFP':
                        current_chart_section = Airport.CHART_SECTIONS['approach']
                    case _:
                        current_chart_section = Airport.CHART_SECTIONS['general']

            if event == END_EVENT and tag == 'record':
                if chart_change:
                    current_chart.did_change = True
                    current_chart.change_pdf_name = current_chart.pdf_name[:-4] + '_CMP' + current_chart.pdf_name[-4:]
                    current_chart.change_pdf_url = current_chart.pdf_url[:-4] + '_CMP' + current_chart.pdf_url[-4:]

                if not skip_chart:
                    current_airport.insert_new_chart(current_chart_section, current_chart)

                skip_chart = False
                chart_change = False
                current_chart = Chart()

            if event == END_EVENT and tag =='airport_name':
                #process airport
                if current_airport.airport_data.icao_ident == 'KAVL':
                    print(current_airport)

                current_airport.reset_for_next_airport()

main()
