import os
from typing import Any, Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .controller import Controller, ControllerException
from .config import settings

MAX_UPLOAD_SIZE = 1024 * 1024

# Create storage folder
os.makedirs('storage', exist_ok=True)

app = FastAPI(
    docs_url='/storage-docs', openapi_url="/storage-docs/openapi.json")
controller = Controller('storage', 'sqlite:///storage/file_storage.db')
app.mount('/storage', StaticFiles(directory='storage'), name='static')
#
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.post('/upload')
def upload_file(
    file: UploadFile = File(...)
) -> Dict[str, Any]:
    file_chunks = []  # type: List[bytes]

    real_file_size = 0
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f'Too large file. Maximum allowed file: {MAX_UPLOAD_SIZE} bytes',
            )
        file_chunks.append(chunk)

    try:
        file_uid = controller.save_file(
            b''.join(file_chunks), file.filename, file.content_type
        )
    except ControllerException:
        return {'status': 'error', 'reason': 'problems with server'}

    model_file = controller.get_file_by_uid(file_uid)
    path = os.path.join(
        settings.SERVER_HOST,
        controller.get_file_path_in_storage(model_file.file_path))
    return {'status': 'ok', 'file_uid': file_uid, 'path': path}


@app.get('/download/{file_uid}')
def download_file(file_uid: str) -> FileResponse:
    try:
        file = controller.get_file_by_uid(file_uid)
    except ControllerException:
        file = None

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='you are not allowed to get this file',
        )

    return FileResponse(
        path=controller.get_file_path_in_storage(file.file_path),
        filename=file.file_original_name,
        media_type=file.file_media_type,
    )


@app.get('/download/link/{file_uid}')
def download_link(file_uid: str) -> Dict[str, str]:
    try:
        file = controller.get_file_by_uid(file_uid)
    except ControllerException:
        file = None

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='you are not allowed to get this file',
        )

    path = os.path.join(
        settings.SERVER_HOST,
        controller.get_file_path_in_storage(file.file_path))
    return {'path': path}
