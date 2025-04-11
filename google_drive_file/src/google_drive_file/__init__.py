import io
import re
from googleapiclient import discovery
from googleapiclient import http
from google.oauth2.service_account import Credentials

from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.data_types import DataType

class GoogleDriveFile(
    LunarComponent,
    component_name="Google Drive File",
    component_description="This component replaces the xlsx file in Google Drive.",
    input_types={"file_link": DataType.TEXT, "credentials_json": DataType.TEXT},
    output_type=DataType.TEXT,
    component_group=ComponentGroup.DATA_EXTRACTION,
):

    def __init__(self, **kwargs):
        super().__init__(configuration=kwargs)

    def extract_file_id(self, file_link: str) -> str:
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', file_link)
        if not match:
            raise ValueError("Invalid Google Drive link")
        return match.group(1)

    def run(self, file_link: str, credentials_json: str) -> str:
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(str(credentials_json), scopes=SCOPES)

        service = discovery.build("drive", "v3", credentials=creds)

        file_id = self.extract_file_id(file_link)
        file_metadata = service.files().get(fileId=file_id).execute()
        file_name = file_metadata['name']

        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = http.MediaIoBaseDownload(file, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        file.seek(0)
        output_file_path = f"/tmp/{file_name}"
        with open(output_file_path, "wb") as f:
            f.write(file.read())

        return output_file_path