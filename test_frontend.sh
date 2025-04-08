#!/bin/bash

# Simple testing script for the DiscoBots.fr frontend
echo "Testing DiscoBots.fr frontend..."

# Check that all required files exist
echo "Checking for required files..."

FILES=(
  "frontend/index.html"
  "frontend/login.html"
  "frontend/register.html"
  "frontend/discord.html"
  "frontend/terms.html"
  "frontend/settings.html"
  "frontend/checkout.html"
  "frontend/checkout-success.html"
  "frontend/checkout-cancel.html"
  "frontend/css/styles.css"
  "frontend/js/main.js"
  "frontend/js/api.js"
  "frontend/js/particles.js"
  "frontend/img/logo.png"
  "frontend/img/favicon.ico"
  "frontend/netlify.toml"
)

MISSING=0
for FILE in "${FILES[@]}"; do
  if [ ! -f "$FILE" ]; then
    echo "❌ Missing: $FILE"
    MISSING=$((MISSING+1))
  else
    echo "✅ Found: $FILE"
  fi
done

if [ $MISSING -eq 0 ]; then
  echo "All required files are present."
else
  echo "$MISSING required files are missing."
fi

# Check for valid HTML in all HTML files
echo ""
echo "Checking HTML files..."
HTML_ERRORS=0
for FILE in frontend/*.html; do
  # Use grep to check for basic HTML structure
  if ! grep -q "<html" "$FILE" || ! grep -q "<head" "$FILE" || ! grep -q "<body" "$FILE"; then
    echo "❌ Invalid HTML in $FILE"
    HTML_ERRORS=$((HTML_ERRORS+1))
  else
    echo "✅ Valid HTML in $FILE"
  fi
done

if [ $HTML_ERRORS -eq 0 ]; then
  echo "All HTML files look valid."
else
  echo "$HTML_ERRORS HTML files have issues."
fi

# Check for JavaScript errors
echo ""
echo "Checking JavaScript files..."
JS_ERRORS=0
for FILE in frontend/js/*.js; do
  # Use grep to check for common syntax errors
  if grep -q "^[^\/]*[^=]=[^=]" "$FILE"; then
    echo "⚠️ Possible assignment used instead of comparison in $FILE"
    JS_ERRORS=$((JS_ERRORS+1))
  else
    echo "✅ No obvious errors in $FILE"
  fi
done

if [ $JS_ERRORS -eq 0 ]; then
  echo "All JavaScript files look valid."
else
  echo "$JS_ERRORS JavaScript files have potential issues."
fi

# Summary
echo ""
echo "Test Summary:"
echo "-------------"
echo "Total files checked: ${#FILES[@]}"
echo "Missing files: $MISSING"
echo "HTML files with issues: $HTML_ERRORS"
echo "JavaScript files with potential issues: $JS_ERRORS"

if [ $MISSING -eq 0 ] && [ $HTML_ERRORS -eq 0 ] && [ $JS_ERRORS -eq 0 ]; then
  echo "✅ All tests passed! The frontend is ready for deployment."
else
  echo "❌ Some tests failed. Please fix the issues before deploying."
fi