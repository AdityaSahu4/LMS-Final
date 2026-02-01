"""
File Upload API Routes
Endpoints for file upload and management
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from typing import List

from app.modules.files.storage import FileStorageService

router = APIRouter()


@router.post("/upload/logo")
async def upload_logo(
    file: UploadFile = File(...),
    organization_id: str = None
):
    """
    Upload laboratory logo
    
    - **file**: Image file (JPG/PNG, max 1MB)
    - **organization_id**: Optional organization ID to prefix filename
    """
    try:
        file_url = await FileStorageService.save_logo(file, organization_id)
        return {
            "success": True,
            "file_url": file_url,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/upload/document")
async def upload_document(
    file: UploadFile = File(...),
    doc_type: str = "general",
    organization_id: str = None
):
    """
    Upload document file
    
    - **file**: PDF file (max 2MB)
    - **doc_type**: Type of document (general, compliance, policy, etc.)
    - **organization_id**: Optional organization ID to prefix filename
    """
    try:
        file_url = await FileStorageService.save_document(file, doc_type, organization_id)
        return {
            "success": True,
            "file_url": file_url,
            "filename": file.filename,
            "doc_type": doc_type
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/upload/multiple")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    doc_type: str = "general",
    organization_id: str = None
):
    """
    Upload multiple document files
    
    - **files**: List of PDF files (max 2MB each)
    - **doc_type**: Type of documents
    - **organization_id**: Optional organization ID to prefix filenames
    """
    try:
        uploaded_files = []
        
        for file in files:
            file_url = await FileStorageService.save_document(file, doc_type, organization_id)
            uploaded_files.append({
                "file_url": file_url,
                "filename": file.filename
            })
        
        return {
            "success": True,
            "files": uploaded_files,
            "count": len(uploaded_files)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/delete")
async def delete_file(file_url: str):
    """
    Delete a file
    
    - **file_url**: URL of the file to delete
    """
    success = FileStorageService.delete_file(file_url)
    
    if success:
        return {
            "success": True,
            "message": "File deleted successfully"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
