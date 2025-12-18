# Cultural Face Perception Experiment

A 2AFC (two-alternative forced choice) web-based experiment using jsPsych 7.3, hosted on GitHub Pages with data saved to Google Sheets.

## Task Description

Participants view face images and judge whether each came from a Western (Google) or Chinese (Baidu) search engine using arrow keys.

## Project Structure

```
cultural-face-experiment/
├── index.html           # Main experiment (jsPsych 7.3)
├── stimuli.json         # Auto-generated image list
├── images/
│   ├── english/         # Western source images (50 images)
│   └── chinese/         # Chinese source images (50 images)
├── generate_urls.py     # Participant URL generator
└── README.md
```

## Configuration

Edit the `CONFIG` object at the top of `index.html`:

```javascript
const CONFIG = {
    N_TRIALS: 5,              // Number of main trials per participant
    N_PRACTICE: 2,            // Number of practice trials (1 per source)
    GOOGLE_SCRIPT_URL: '',    // Fill in after setting up Google Apps Script
    SAMPLE_WITH_REPLACEMENT: true,
    FIXATION_DURATION: 500,   // ms
    FEEDBACK_DURATION: 800    // ms
};
```

## Setup Instructions

### 1. Deploy to GitHub Pages

1. Create a new GitHub repository (e.g., `cultural-face-experiment`)
2. Push this folder to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/USERNAME/cultural-face-experiment.git
   git branch -M main
   git push -u origin main
   ```
3. Go to repository Settings → Pages
4. Under "Source", select "Deploy from a branch"
5. Select "main" branch and "/ (root)" folder
6. Click Save

Your experiment will be available at: `https://USERNAME.github.io/cultural-face-experiment/`

### 2. Set Up Google Sheets Data Collection

#### Create the Google Sheet

1. Go to [Google Sheets](https://sheets.google.com) and create a new spreadsheet
2. Name it "Face Perception Data"
3. Add headers in Row 1:
   ```
   A: participant_id
   B: trial_number
   C: image
   D: source
   E: response
   F: response_decoded
   G: correct
   H: rt
   I: timestamp
   J: completion_code
   K: debrief_response
   ```

#### Create the Apps Script

1. In your Google Sheet, go to **Extensions → Apps Script**
2. Delete any existing code and paste the following:

```javascript
function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const data = JSON.parse(e.postData.contents);

    // Append each trial as a row
    data.trials.forEach(trial => {
      sheet.appendRow([
        trial.participant_id,
        trial.trial_number,
        trial.image,
        trial.source,
        trial.response,
        trial.response_decoded,
        trial.correct,
        trial.rt,
        trial.timestamp,
        data.completion_code,
        data.debrief_response
      ]);
    });

    return ContentService.createTextOutput(JSON.stringify({status: 'success'}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({status: 'error', message: error.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Test function to verify deployment
function doGet(e) {
  return ContentService.createTextOutput('Google Apps Script is working!')
    .setMimeType(ContentService.MimeType.TEXT);
}
```

3. Click **Deploy → New deployment**
4. Click the gear icon → Select **Web app**
5. Configure:
   - Description: "Face Perception Data Collector"
   - Execute as: **Me**
   - Who has access: **Anyone**
6. Click **Deploy**
7. Click **Authorize access** and grant permissions
8. **Copy the Web app URL** (looks like `https://script.google.com/macros/s/.../exec`)

#### Add the URL to Your Experiment

1. Open `index.html`
2. Find the `CONFIG` object and paste your URL:

```javascript
const CONFIG = {
    ...
    GOOGLE_SCRIPT_URL: 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec',
    ...
};
```

3. Commit and push the change

### 3. Generate Participant URLs

Use the included Python script to generate unique participant URLs:

```bash
python generate_urls.py --base-url https://USERNAME.github.io/cultural-face-experiment --n 50
```

Or use the bash one-liner:

```bash
for i in $(seq -f "%03g" 1 50); do
  echo "https://USERNAME.github.io/cultural-face-experiment/?pid=P${i}"
done
```

## Participant Experience

1. Participant clicks their unique link (e.g., `?pid=P001`)
2. Welcome screen displays their participant ID
3. Instructions explain the task
4. 2 practice trials with feedback
5. 5 main trials (randomly sampled) without feedback
6. Debrief question: "What cues did you use?"
7. Completion screen showing:
   - Accuracy
   - Completion code: `FACE-P001-A7X2`

## Data Output

Each trial is logged to Google Sheets with:

| Field | Description |
|-------|-------------|
| participant_id | From URL parameter |
| trial_number | 1-5 |
| image | Filename |
| source | english/chinese |
| response | arrowleft/arrowright |
| response_decoded | western/chinese |
| correct | true/false |
| rt | Response time (ms) |
| timestamp | ISO timestamp |
| completion_code | FACE-{pid}-{4chars} |
| debrief_response | Free text |

## Verifying Completion

Match the completion code format: `FACE-{pid}-{4 random chars}`

For participant P001, valid codes look like: `FACE-P001-A7X2`

## Local Testing

To test locally:

1. Start a local server:
   ```bash
   python -m http.server 8000
   ```
2. Open: `http://localhost:8000/?pid=test001`

## Troubleshooting

**Images not loading?**
- Check that images are in the correct folders
- Ensure `stimuli.json` paths match actual file locations
- Check browser console for 404 errors

**Data not saving to Google Sheets?**
- Verify the Apps Script URL is correct
- Check that the script is deployed as "Anyone" can access
- Check browser console for CORS or fetch errors
- Test the script URL directly in browser (should show "Google Apps Script is working!")

**Completion code not generating?**
- Ensure participant ID is provided in URL
- Check browser console for JavaScript errors
