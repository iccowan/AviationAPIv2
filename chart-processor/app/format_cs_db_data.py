
def process_data(airac, files_path):
    logInfo("Beginning to process airport chart data for DynamoDB")
    try:
        file = open(files_path / "d-TPP_Metafile.xml")
    except FileNotFoundError:
        logError(f"No airport DB file d-TPP_Metafile.xml found in {files_path}")
    else:
        xml_document = ElementTree.iterparse(file, [START_EVENT, END_EVENT])
        airports = process_xml_db(xml_document, airac)

        logInfo(f"Finished processing data for {str(airports)} airports")
    finally:
        file.close()
