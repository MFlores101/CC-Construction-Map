#!/usr/bin/env node
/**
 * Build script for Vercel deployment
 * Replaces API key placeholders with environment variables
 */

const fs = require('fs');
const path = require('path');

const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY || 'YOUR_GOOGLE_MAPS_API_KEY';

// Read index.html
const indexPath = path.join(__dirname, 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

// Replace Google Maps API key
html = html.replace(/YOUR_GOOGLE_MAPS_API_KEY/g, GOOGLE_MAPS_API_KEY);

// Write back
fs.writeFileSync(indexPath, html, 'utf8');

console.log('✅ Build complete - API keys injected');

