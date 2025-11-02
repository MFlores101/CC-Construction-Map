# Deployment Guide - Vercel

This guide explains how to deploy this project to Vercel with environment variables for API keys.

## Prerequisites

1. A Vercel account (free tier works)
2. Your API keys:
   - Google Maps API Key
   - OpenAI API Key (for local Python script)

## Setting Up Environment Variables in Vercel

### Step 1: Add Environment Variables in Vercel Dashboard

1. **Go to your Vercel project dashboard**
2. **Navigate to Settings → Environment Variables**
3. **Add the following variable:**

   - **Name:** `GOOGLE_MAPS_API_KEY`
   - **Value:** Your Google Maps API key
   - **Environment:** Production, Preview, Development (check all)

4. **Click "Save"**

### Step 2: Using Vercel CLI (Alternative)

```bash
# Install Vercel CLI if you haven't
npm i -g vercel

# Login to Vercel
vercel login

# Set environment variable
vercel env add GOOGLE_MAPS_API_KEY

# Pull environment variables for local testing
vercel env pull .env.local
```

## How It Works

1. **Build Script**: The `build.js` script runs during Vercel deployment
2. **Environment Variable**: Reads `GOOGLE_MAPS_API_KEY` from Vercel's environment
3. **Key Injection**: Replaces `YOUR_GOOGLE_MAPS_API_KEY` placeholder in `index.html`
4. **Deployment**: Vercel serves the updated `index.html` with your actual key

## Deploying to Vercel

### Method 1: GitHub Integration (Recommended)

1. Push your code to GitHub
2. Import the repository in Vercel
3. **Add environment variable** in Vercel dashboard (Settings → Environment Variables)
4. Deploy! Vercel will run `npm run build` automatically

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy (will prompt for environment variables if not set)
vercel

# For production deployment
vercel --prod
```

## Local Development

For local development, you can:

**Option A: Use the Python server (no build needed)**
```bash
python3 server.py
# Manually replace YOUR_GOOGLE_MAPS_API_KEY in index.html
```

**Option B: Test the build locally**
```bash
# Set environment variable
export GOOGLE_MAPS_API_KEY="your-key-here"

# Run build script
npm run build

# Run local server
python3 server.py
```

**Option C: Create `.env.local`** (for Vercel CLI)
```bash
vercel env pull .env.local
# Then run: npm run build
```

## Important Notes

1. **Google Maps API Key Security:**
   - Restrict your API key in Google Cloud Console
   - Add your Vercel domain to allowed HTTP referrers:
     - `https://your-project.vercel.app/*`
     - `https://*.vercel.app/*` (for preview deployments)
   - **Never commit your actual API key to Git**

2. **OpenAI API Key:**
   - The Python script (`extract_construction.py`) runs locally, not on Vercel
   - Run it on your machine to generate `construction_data.json`
   - Commit `construction_data.json` to Git (or use a separate service)
   - For the script, use: `export OPENAI_API_KEY="your-key"` locally

3. **Build Process:**
   - The build script modifies `index.html` during deployment
   - The modified file is only in Vercel's build output, not your repo
   - Your Git repo stays clean with placeholders

## Troubleshooting

**Build fails:**
- Make sure `GOOGLE_MAPS_API_KEY` is set in Vercel dashboard
- Check that Node.js is available (Vercel provides it automatically)

**Maps not loading:**
- Verify the API key is correctly injected (check page source on Vercel)
- Check Google Cloud Console API key restrictions
- Ensure Maps JavaScript API is enabled in Google Cloud Console

