#!/bin/bash

echo "🔍 Deployment Verification Script"
echo "=================================="
echo ""

# Check if wsgi.py exists
if [ -f "wsgi.py" ]; then
    echo "✅ wsgi.py exists"
else
    echo "❌ wsgi.py NOT FOUND"
    exit 1
fi

# Check if app.py still exists (should not)
if [ -f "app.py" ]; then
    echo "⚠️  WARNING: app.py still exists - please delete it"
else
    echo "✅ app.py removed (correct)"
fi

# Check render.yaml
if grep -q "gunicorn wsgi:app" render.yaml; then
    echo "✅ render.yaml uses wsgi:app"
else
    echo "❌ render.yaml still uses app:app"
    exit 1
fi

# Check Procfile
if grep -q "gunicorn wsgi:app" Procfile; then
    echo "✅ Procfile uses wsgi:app"
else
    echo "❌ Procfile still uses app:app"
    exit 1
fi

# Test Python import
echo ""
echo "Testing Python import..."
python3 -c "import wsgi; print('✅ wsgi.py imports successfully'); print('   App name:', wsgi.app.name)" 2>&1

# Test gunicorn config
echo ""
echo "Testing gunicorn config..."
if python3 -m gunicorn --check-config wsgi:app 2>&1 | grep -q "error"; then
    echo "❌ Gunicorn config test failed"
    exit 1
else
    echo "✅ Gunicorn can load wsgi:app"
fi

echo ""
echo "=================================="
echo "✅ ALL CHECKS PASSED!"
echo "Ready for deployment to Render"
echo ""
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m 'fix: rename app.py to wsgi.py'"
echo "3. git push origin main"
echo "4. Render will auto-deploy"
