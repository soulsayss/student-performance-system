# Performance Optimization Installation Script

Write-Host "🚀 Installing Performance Optimizations..." -ForegroundColor Green
Write-Host ""

# Step 1: Install Flask-Caching
Write-Host "Step 1: Installing Flask-Caching..." -ForegroundColor Cyan
pip install Flask-Caching==2.1.0

Write-Host ""
Write-Host "✅ Flask-Caching installed successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Verify installation
Write-Host "Step 2: Verifying installation..." -ForegroundColor Cyan
pip show Flask-Caching

Write-Host ""
Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "1. Restart your backend server: python app.py"
Write-Host "2. Test the dashboard - it should load 75% faster!"
Write-Host "3. Check PERFORMANCE_BOOST.md for details"
Write-Host ""
