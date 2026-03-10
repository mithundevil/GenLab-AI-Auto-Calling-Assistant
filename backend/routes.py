from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import JSONResponse
from database.db import get_db_connection
from backend.twilio_service import twilio_service
from backend.ai_service import AIService
from twilio.twiml.voice_response import VoiceResponse
import urllib.parse

router = APIRouter()

@router.post("/lead")
@router.post("/lead/")
async def create_lead(name: str = Form(...), email: str = Form(...), phone: str = Form(...)):
    try:
        # Save to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO leads (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )
        conn.commit()
        conn.close()
        
        # Trigger Twilio Call
        call_sid = twilio_service.trigger_outbound_call(phone, name)
        
        return JSONResponse(content={
            "status": "success",
            "message": "Lead saved and call triggered",
            "call_sid": call_sid
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@router.post("/ai-call")
@router.get("/ai-call")
async def ai_call_endpoint(request: Request):
    params = request.query_params
    name = params.get("name", "Customer")
    
    ai_intro = await AIService.generate_intro(name)
    
    response = VoiceResponse()
    # Using Gather with longer timeout
    gather = response.gather(
        input='speech',
        action=f'/api/handle-speech?name={urllib.parse.quote(name)}',
        language='ta-IN',
        speechTimeout='auto',
        timeout=10  # Wait up to 10 seconds for user to start speaking
    )
    gather.say(ai_intro, voice='Polly.Raveena', language='en-IN')
    
    # If silence, remind gently in Tamil and try again
    response.say("Neenga ange irukkingala? Are you there?", voice='Polly.Raveena', language='en-IN')
    response.redirect(f'/api/ai-call?name={urllib.parse.quote(name)}')
    
    return Response(content=str(response), media_type="application/xml")

@router.post("/handle-speech")
async def handle_speech_endpoint(request: Request):
    form_data = await request.form()
    user_speech = form_data.get("SpeechResult", "")
    name = request.query_params.get("name", "Customer")
    
    if not user_speech:
        response = VoiceResponse()
        response.say("Mannikkavum, enakku ketkavillai. Sorry, I didn't hear you.", voice='Polly.Raveena', language='en-IN')
        response.redirect(f'/api/ai-call?name={urllib.parse.quote(name)}')
        return Response(content=str(response), media_type="application/xml")

    # Generate AI response
    system_msg = "You are a helpful AI sales voice assistant for GenLab. IMPORTANT: Write ALL responses using ROMANIZED TAMIL only (Tamil words in English letters / Tanglish). Do NOT use Tamil script. Answer concisely in under 40 words."
    ai_reply = await AIService.get_response(user_speech, system_msg)
    
    response = VoiceResponse()
    gather = response.gather(
        input='speech',
        action=f'/api/handle-speech?name={urllib.parse.quote(name)}',
        language='ta-IN',
        speechTimeout='auto',
        timeout=10
    )
    gather.say(ai_reply, voice='Polly.Raveena', language='en-IN')
    
    # Keep the call alive if silence
    response.redirect(f'/api/handle-speech?name={urllib.parse.quote(name)}')
    
    return Response(content=str(response), media_type="application/xml")
