# 🚀 Git Setup Guide for Beginners

Follow these steps EXACTLY to push your project to GitHub.

## ⚠️ Before You Start

1. **Create a GitHub account** at https://github.com if you don't have one
2. **Install Git** on your computer:
   - Download from: https://git-scm.com/downloads
   - After installing, restart your terminal/command prompt

## 📋 Step-by-Step Commands

### STEP 1: Configure Git (First Time Only)

Open your terminal/command prompt and run these commands:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Replace:**
- `"Your Name"` with your actual name
- `"your.email@example.com"` with your email

### STEP 2: Navigate to Your Project

```bash
cd student-academic-system
```

### STEP 3: Initialize Git Repository

```bash
git init
```

You should see: `Initialized empty Git repository`

### STEP 4: Add All Files

```bash
git add .
```

This adds all files to staging (the dot means "everything")

### STEP 5: Make Your First Commit

```bash
git commit -m "Initial commit: Student Academic Performance System"
```

You should see a summary of files added.

### STEP 6: Create Repository on GitHub

1. Go to https://github.com
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in:
   - **Repository name:** `student-academic-system`
   - **Description:** "AI-powered student performance prediction and career guidance system"
   - **Public** or **Private** (your choice)
   - **DO NOT** check "Initialize with README" (we already have one)
4. Click **"Create repository"**

### STEP 7: Connect to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/student-academic-system.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME`** with your actual GitHub username!

**Example:**
If your username is `john123`, the command would be:
```bash
git remote add origin https://github.com/john123/student-academic-system.git
```

### STEP 8: Enter GitHub Credentials

When prompted:
- **Username:** Your GitHub username
- **Password:** Your GitHub Personal Access Token (NOT your password!)

#### How to Create Personal Access Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Student Project"
4. Select scopes: Check **"repo"** (full control)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing

## ✅ Verify Success

After pushing, go to your GitHub repository URL:
```
https://github.com/YOUR_USERNAME/student-academic-system
```

You should see all your files there!

## 🔄 Making Changes Later

When you make changes to your code:

```bash
# 1. Add changed files
git add .

# 2. Commit with a message
git commit -m "Description of what you changed"

# 3. Push to GitHub
git push
```

## 🆘 Common Issues

### Issue: "git: command not found"
**Solution:** Install Git from https://git-scm.com/downloads

### Issue: "Permission denied"
**Solution:** Use Personal Access Token instead of password

### Issue: "Repository not found"
**Solution:** Check your username in the URL is correct

### Issue: "Failed to push"
**Solution:** Run `git pull origin main` first, then `git push`

## 📝 Quick Reference

```bash
# Check status
git status

# See commit history
git log

# See remote URL
git remote -v

# Pull latest changes
git pull

# Push changes
git push
```

## 🎉 You're Done!

Your project is now on GitHub! Share the link with others:
```
https://github.com/YOUR_USERNAME/student-academic-system
```

---

**Need help?** Open an issue on GitHub or ask in the community!
