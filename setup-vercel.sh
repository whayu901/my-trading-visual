#!/bin/bash

#==============================================================================
# 🚀 Automated Vercel Deployment Setup
# For: Trading Visual Guide HTML
#==============================================================================

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  📊 Trading Visual Guide - Vercel Deployment Setup        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

#==============================================================================
# Step 1: Check Prerequisites
#==============================================================================
echo "🔍 Checking prerequisites..."

# Check Git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found!"
    echo "📥 Installing Git..."
    if command -v brew &> /dev/null; then
        brew install git
    else
        echo "⚠️  Please install Git manually from: https://git-scm.com/download/mac"
        exit 1
    fi
fi
echo "✅ Git installed: $(git --version)"

# Check if GitHub CLI installed (optional)
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found: $(gh --version | head -n 1)"
    HAS_GH_CLI=true
else
    echo "ℹ️  GitHub CLI not found (optional - you can use web interface)"
    HAS_GH_CLI=false
fi

echo ""

#==============================================================================
# Step 2: Git Configuration
#==============================================================================
echo "⚙️  Configuring Git..."

# Check if Git is already configured
GIT_NAME=$(git config --global user.name 2>/dev/null || echo "")
GIT_EMAIL=$(git config --global user.email 2>/dev/null || echo "")

if [ -z "$GIT_NAME" ]; then
    read -p "Enter your name for Git: " GIT_NAME
    git config --global user.name "$GIT_NAME"
fi

if [ -z "$GIT_EMAIL" ]; then
    read -p "Enter your email for Git: " GIT_EMAIL
    git config --global user.email "$GIT_EMAIL"
fi

echo "✅ Git configured as: $GIT_NAME <$GIT_EMAIL>"
echo ""

#==============================================================================
# Step 3: Project Setup
#==============================================================================
echo "📦 Setting up project structure..."

# Create project directory
PROJECT_DIR="$HOME/Documents/tradingview/snd/trading-guide-app"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Copy HTML file
if [ -f "../trading-visual-guide.html" ]; then
    cp "../trading-visual-guide.html" "index.html"
    echo "✅ Copied: index.html"
else
    echo "❌ Error: trading-visual-guide.html not found!"
    exit 1
fi

# Create vercel.json
cat > vercel.json << 'EOF'
{
  "version": 2,
  "name": "trading-visual-guide",
  "builds": [
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
EOF
echo "✅ Created: vercel.json"

# Create README
cat > README.md << 'EOF'
# 📊 S&R Trading Visual Guide

Interactive visual guide for Support & Resistance trading strategy.

## Features
- Support/Resistance box examples
- Break & Retest strategies
- Risk management calculator
- Multi-timeframe workflow
- Signal reference guide

## Tech Stack
- Pure HTML/CSS
- TradingView dark theme
- Responsive design

## Deployment
Hosted on Vercel with auto-deployment from GitHub.

---
Optimized for XAU & Forex scalping (M1/M5/M15)
EOF
echo "✅ Created: README.md"

# Create .gitignore
cat > .gitignore << 'EOF'
# Mac
.DS_Store

# Logs
*.log

# Editor
.vscode/
.idea/

# Environment
.env
.env.local

# Vercel
.vercel
EOF
echo "✅ Created: .gitignore"

echo ""

#==============================================================================
# Step 4: Initialize Git Repository
#==============================================================================
echo "🌱 Initializing Git repository..."

git init
git add .
git commit -m "Initial commit: S&R trading visual guide"

echo "✅ Git repository initialized"
echo ""

#==============================================================================
# Step 5: GitHub Setup
#==============================================================================
echo "🌐 GitHub Setup..."
echo ""
echo "Choose an option:"
echo "  1) Use GitHub CLI (automated)"
echo "  2) Use GitHub Web (manual)"
echo ""
read -p "Enter choice [1 or 2]: " GITHUB_CHOICE

if [ "$GITHUB_CHOICE" = "1" ] && [ "$HAS_GH_CLI" = true ]; then
    echo ""
    echo "📤 Creating GitHub repository..."

    # Check if logged in to GitHub CLI
    if ! gh auth status &> /dev/null; then
        echo "🔐 Logging into GitHub..."
        gh auth login
    fi

    # Create repo
    read -p "Repository name [trading-guide]: " REPO_NAME
    REPO_NAME=${REPO_NAME:-trading-guide}

    read -p "Make repository private? [Y/n]: " IS_PRIVATE
    IS_PRIVATE=${IS_PRIVATE:-Y}

    if [[ "$IS_PRIVATE" =~ ^[Yy]$ ]]; then
        gh repo create "$REPO_NAME" --private --source=. --push
    else
        gh repo create "$REPO_NAME" --public --source=. --push
    fi

    echo "✅ Repository created and pushed!"
    REPO_URL=$(gh repo view --json url -q .url)
    echo "🔗 Repository URL: $REPO_URL"

else
    echo ""
    echo "📋 Manual GitHub Setup Instructions:"
    echo ""
    echo "1. Go to: https://github.com/new"
    echo "2. Repository name: trading-guide (or your choice)"
    echo "3. Description: S&R Trading Visual Guide"
    echo "4. Choose: Private or Public"
    echo "5. DON'T initialize with README"
    echo "6. Click 'Create repository'"
    echo ""
    read -p "Press Enter when repository is created..."
    echo ""

    read -p "Enter your GitHub username: " GH_USERNAME
    read -p "Enter repository name: " REPO_NAME

    git remote add origin "https://github.com/$GH_USERNAME/$REPO_NAME.git"
    git branch -M main

    echo ""
    echo "📤 Pushing to GitHub..."
    echo "ℹ️  You may need to enter your GitHub credentials"
    echo "ℹ️  Use Personal Access Token as password (not account password)"
    echo "ℹ️  Create token at: https://github.com/settings/tokens"
    echo ""

    git push -u origin main

    echo "✅ Pushed to GitHub!"
    REPO_URL="https://github.com/$GH_USERNAME/$REPO_NAME"
    echo "🔗 Repository URL: $REPO_URL"
fi

echo ""

#==============================================================================
# Step 6: Vercel Deployment Instructions
#==============================================================================
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 NEXT: Deploy to Vercel                                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Follow these steps:"
echo ""
echo "1. Go to: https://vercel.com"
echo "2. Click 'Login' → 'Continue with GitHub'"
echo "3. Authorize Vercel"
echo "4. Click 'Add New...' → 'Project'"
echo "5. Import your repository: ${REPO_NAME:-trading-guide}"
echo "6. Keep all settings default"
echo "7. Click 'Deploy'"
echo "8. Wait 30 seconds..."
echo "9. 🎉 Your guide is LIVE!"
echo ""
echo "Your URL will look like:"
echo "https://trading-guide-xxxxx.vercel.app"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📋 Project location: $PROJECT_DIR"
echo "🔗 GitHub: $REPO_URL"
echo ""
echo "🎉 Setup complete!"
echo ""
echo "💡 Future updates:"
echo "   1. Edit: $PROJECT_DIR/index.html"
echo "   2. Run: cd $PROJECT_DIR && git add . && git commit -m 'Update' && git push"
echo "   3. Vercel auto-deploys in 30 seconds!"
echo ""
echo "════════════════════════════════════════════════════════════"
