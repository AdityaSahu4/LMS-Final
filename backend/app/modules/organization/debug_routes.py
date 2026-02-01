"""
Debug endpoint to see exactly what data is being sent
"""
from fastapi import APIRouter, Request

router = APIRouter()

@router.put("/debug/compliance")
async def debug_compliance(request: Request):
    """Debug endpoint to see raw request data"""
    body = await request.json()
    print("=" * 80)
    print("RAW REQUEST BODY:")
    print(body)
    print("=" * 80)
    
    if "compliance_documents" in body and len(body["compliance_documents"]) > 0:
        first_doc = body["compliance_documents"][0]
        print("\nFIRST DOCUMENT:")
        for key, value in first_doc.items():
            print(f"  {key}: {value!r} (type: {type(value).__name__})")
    
    return {"status": "ok", "received": body}
