Alright — if we want free / free-trial AI verification and don’t want to create a separate microservice API for it, we can:

Use OpenAI Vision API — free tier available if you have new credits (good for hackathon MVP).

Or Hugging Face Inference API — free tier, can call waste-detection models without training.

Or Roboflow Hosted Models — free plan (200 free credits/month) with YOLO models.

We’ll structure prompts so you can swap between them easily.
Here’s the updated, final prompt sequence for your Django MVP.

Prompt 1 — Project bootstrap
Ask:

Act as a senior Django dev. Create commands and a minimal README to bootstrap a new Django project called cityconnect_mvp and an app called issues. Include:

recommended pip install commands (django, djangorestframework, pillow, exifread, geopy, requests, python-dotenv, plus openai or huggingface_hub depending on AI choice),

settings.py additions for MEDIA and REST_FRAMEWORK,

.env variables (SECRET_KEY, OPENAI_API_KEY or HF_API_KEY, optional GOOGLE_MAPS_API_KEY),

exact command sequence to run migrations and startserver.

Prompt 2 — Models
Ask:

Create Django models for issues app:

user (optional FK to AUTH_USER_MODEL),

title (char),

description (text),

image (ImageField),

reported_latitude & reported_longitude (decimal),

exif_latitude & exif_longitude (nullable decimal),

is_verified (nullable boolean),

verification_method (char choices: 'openai', 'huggingface', 'roboflow', 'manual'),

verification_score (float, null),

verification_details (JSONField or TextField),

timestamps.

Add model method extract_exif_and_save() to read EXIF GPS using Pillow or exifread. Provide migrations.

Prompt 3 — Report form (camera + GPS capture)
Ask:

Generate report_create.html template and Django view:

Form fields: title, description, camera file input (accept="image/*" capture="environment"), hidden lat/lon inputs.

JavaScript: get GPS coords before submit, fill hidden inputs, submit.

View: save form, call extract_exif_and_save() after save.

Fallback UI if GPS denied.

Prompt 4 — EXIF & location compare
Ask:

Create utils/location_tools.py:

extract_gps_from_image(image_path) → (lat, lon) or None

haversine_distance(lat1, lon1, lat2, lon2) → meters

verify_location_against_exif(reported_lat, reported_lon, exif_lat, exif_lon) → dict with match True/False, distance.

Prompt 5 — AI image verification (OpenAI + free alternative)
Ask:

Create verifier/image_verifier.py with:

verify_with_openai(image_path, prompt="Does this image show a civic issue like garbage or pothole?") — returns dict {yes_no, confidence, explanation}

verify_with_huggingface(image_path, model_id="mohammadamireshraghi/garbage-detection") — calls Hugging Face Inference API (free tier) for object detection, checks if garbage/pothole found.

Both functions should update IssueReport with is_verified, verification_method, verification_score, verification_details.

Prompt 6 — Verification pipeline
Ask:

Create Django function run_verification(issue_id) that:

Extracts EXIF coords & compares to reported coords.

Runs AI image verification (OpenAI first, fallback to Hugging Face if no API key or fail).

Combines results: is_verified=True only if image shows civic issue and location plausible.

Saves details JSON.
Provide example of calling it after form save.

Prompt 7 — Reverse geocode
Ask:

Create reverse_geocode(lat, lon) using geopy.Nominatim (free) to get address. Return address string. Also add plausibility_check(reported_lat, reported_lon, exif_lat, exif_lon) to confirm if within 50 meters.

Prompt 8 — API endpoint for verification
Ask:

Create DRF endpoint /api/reports/<id>/verify/ that runs run_verification(issue_id) and returns JSON {is_verified, score, details}.

Prompt 9 — Admin customization
Ask:

Customize IssueReport admin: show title, is_verified, method, score; filter by status; add actions force_verify, mark_needs_review.

Prompt 10 — Demo seed command
Ask:

Management command create_demo_issues that seeds a few reports with sample images.

Prompt 11 — Tests
Ask:

Add tests for EXIF extraction, haversine, AI verifier (mocked), and full verification pipeline.

Prompt 12 — Deployment checklist
Ask:

Provide checklist for deploying Django with media storage and using AI API keys securely for hackathon demo.

