import os
import uuid
from fastapi import UploadFile
from supabase import create_client, Client
from app.core.config import settings
from typing import Optional

# Initialize Supabase client globally if configured
supabase: Optional[Client] = None
if settings.SUPABASE_URL and settings.SUPABASE_KEY:
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")

async def upload_file_to_supabase(file: UploadFile, bucket_name: str = "club-media") -> Optional[str]:
    """
    Uploads a file to Supabase Storage and returns the public URL.
    Falls back to local storage if Supabase is not configured.
    """
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    if supabase:
        try:
            # Read file content
            contents = await file.read()
            # Reset file pointer if needed again
            await file.seek(0)
            
            # Upload to Supabase bucket
            res = supabase.storage.from_(bucket_name).upload(
                file=contents,
                path=unique_filename,
                file_options={"content-type": file.content_type}
            )
            
            # Get public URL
            public_url = supabase.storage.from_(bucket_name).get_public_url(unique_filename)
            return public_url
        except Exception as e:
            print(f"Supabase upload failed: {e}")
            await file.seek(0)
    
    # Fallback to local storage
    os.makedirs("uploads", exist_ok=True)
    local_path = os.path.join("uploads", unique_filename)
    with open(local_path, "wb") as buffer:
        buffer.write(await file.read())
    return f"/static/uploads/{unique_filename}"
