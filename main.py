from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from transformers import pipeline

import shutil
import os
import re


app = FastAPI(
    title="MeetIQ AI",
    description="Intelligent Meeting Insights Platform",
    version="1.0.0"
)


# =========================================================
# LOAD AI MODELS
# =========================================================

print("Loading MeetIQ AI models... Please wait.")


# Speech-to-Text
asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny"
)


# Meeting Summarization
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)


# =========================================================
# REQUEST MODEL
# =========================================================

class ActionItemRequest(BaseModel):
    text: str


# =========================================================
# HOME PAGE
# =========================================================

@app.get("/")
def read_index():

    return FileResponse("index.html")


# =========================================================
# FORMAT SUMMARY AS BULLET POINTS
# =========================================================

def format_as_bullets(text):

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    bullet_points = []

    for sentence in sentences:

        sentence = sentence.strip()

        if sentence:

            bullet_points.append(
                f"• {sentence}"
            )

    return "\n".join(bullet_points)


# =========================================================
# PROCESS AUDIO
# =========================================================

@app.post("/process-audio")
async def process_audio(
    file: UploadFile = File(...)
):

    temp_filename = (
        f"temp_{file.filename}"
    )


    try:

        # Save uploaded audio temporarily
        with open(
            temp_filename,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        # -----------------------------------------
        # STEP 1: TRANSCRIBE AUDIO
        # -----------------------------------------

        print("Transcribing meeting audio...")


        transcription_result = (
            asr_pipeline(
                temp_filename
            )
        )


        transcription = (
            transcription_result["text"]
            .strip()
        )


        if not transcription:

            raise HTTPException(
                status_code=400,
                detail="No speech was detected in the audio."
            )


        # -----------------------------------------
        # STEP 2: SUMMARIZE MEETING
        # -----------------------------------------

        print("Generating meeting summary...")


        summary_result = summarizer(

            transcription,

            max_length=150,

            min_length=30,

            do_sample=False

        )


        raw_summary = (
            summary_result[0][
                "summary_text"
            ]
        )


        # -----------------------------------------
        # STEP 3: FORMAT SUMMARY
        # -----------------------------------------

        formatted_summary = (
            format_as_bullets(
                raw_summary
            )
        )


        # -----------------------------------------
        # RESPONSE
        # -----------------------------------------

        return {

            "message":
                formatted_summary,

            "original_text":
                transcription

        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "Audio processing error:",
            str(e)
        )


        raise HTTPException(

            status_code=500,

            detail=
                f"Unable to process audio: {str(e)}"

        )


    finally:

        # Delete temporary audio file

        if os.path.exists(
            temp_filename
        ):

            os.remove(
                temp_filename
            )


# =========================================================
# ACTION ITEM HELPERS
# =========================================================

def detect_owner(sentence):

    """
    Basic owner detection.

    Example:
    John will update the API documentation.
    """

    patterns = [

        r"^([A-Z][a-z]+)\s+will\b",

        r"^([A-Z][a-z]+)\s+should\b",

        r"^([A-Z][a-z]+)\s+needs?\s+to\b",

        r"^([A-Z][a-z]+)\s+must\b"

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            sentence
        )


        if match:

            return match.group(1)


    return "Unassigned"


def detect_due_date(sentence):

    """
    Detect simple due-date phrases.
    """

    patterns = [

        r"\bby\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",

        r"\bby\s+(tomorrow|today|next week|next month)\b",

        r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",

        r"\b(tomorrow|today|next week|next month)\b",

        r"\bby\s+([A-Z][a-z]+\s+\d{1,2})\b"

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            sentence,
            re.IGNORECASE
        )


        if match:

            return match.group(1)


    return "Not specified"


def detect_priority(sentence):

    """
    Detect priority from keywords.
    """

    text = sentence.lower()


    high_priority_words = [

        "urgent",
        "critical",
        "immediately",
        "asap",
        "high priority"

    ]


    low_priority_words = [

        "low priority",
        "when possible",
        "optional"

    ]


    for word in high_priority_words:

        if word in text:

            return "High"


    for word in low_priority_words:

        if word in text:

            return "Low"


    return "Medium"


def is_action_item(sentence):

    """
    Determine whether a sentence
    appears to contain an action.
    """

    action_words = [

        "will",
        "should",
        "need to",
        "needs to",
        "must",
        "follow up",
        "update",
        "fix",
        "complete",
        "review",
        "send",
        "prepare",
        "schedule",
        "deploy",
        "create",
        "contact",
        "implement",
        "test",
        "investigate"

    ]


    text = sentence.lower()


    return any(
        word in text
        for word in action_words
    )


def clean_task(sentence):

    """
    Clean sentence before displaying
    it as an action item.
    """

    sentence = sentence.strip()


    sentence = re.sub(
        r"^[•\-\*]\s*",
        "",
        sentence
    )


    return sentence


# =========================================================
# GENERATE ACTION ITEMS
# =========================================================

@app.post("/action-items")
async def generate_action_items(
    request: ActionItemRequest
):

    try:

        text = request.text.strip()


        if not text:

            raise HTTPException(

                status_code=400,

                detail=
                    "Meeting summary is required."

            )


        # Split summary into sentences

        sentences = re.split(

            r'(?<=[.!?])\s+|\n+',

            text

        )


        action_items = []


        for sentence in sentences:

            sentence = clean_task(
                sentence
            )


            if (
                sentence and
                is_action_item(sentence)
            ):

                action_items.append({

                    "task":
                        sentence,

                    "owner":
                        detect_owner(
                            sentence
                        ),

                    "due_date":
                        detect_due_date(
                            sentence
                        ),

                    "priority":
                        detect_priority(
                            sentence
                        )

                })


        return {

            "action_items":
                action_items

        }


    except HTTPException:

        raise


    except Exception as e:

        print(
            "Action item error:",
            str(e)
        )


        raise HTTPException(

            status_code=500,

            detail=
                "Unable to generate action items."

        )