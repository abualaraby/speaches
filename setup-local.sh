#!/bin/bash

# Speaches Local Setup Script - سكربت إعداد التطبيق محلياً
# Script to easily set up Speaches locally

set -e

echo "🎙️  مرحباً بك في مشروع Speaches / Welcome to Speaches"
echo "📋 سيقوم هذا السكربت بإعداد التطبيق محلياً / This script will set up the application locally"
echo ""

# Check if Python 3.12+ is available
echo "🔍 التحقق من Python / Checking Python..."
python_version=$(python3 --version 2>/dev/null | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
required_version="3.12"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت / Python 3 is not installed"
    echo "   يرجى تثبيت Python 3.12+ / Please install Python 3.12+"
    exit 1
fi

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ إصدار Python أقل من المطلوب / Python version is too old"
    echo "   الإصدار الحالي: $python_version / Current version: $python_version"
    echo "   الإصدار المطلوب: $required_version+ / Required version: $required_version+"
    exit 1
fi

echo "✅ Python $python_version موجود / Python $python_version found"

# Check if UV is available, install if not
echo "🔍 التحقق من UV package manager / Checking UV package manager..."
if ! command -v uv &> /dev/null; then
    echo "📥 تثبيت UV / Installing UV..."
    pip install --user uv
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "✅ UV متوفر / UV available"

# Create virtual environment
echo "🔧 إنشاء البيئة الافتراضية / Creating virtual environment..."
uv venv

# Activate virtual environment and install dependencies
echo "📦 تثبيت المتطلبات / Installing dependencies..."
source .venv/bin/activate
uv sync --all-extras

echo ""
echo "🎉 تم الإعداد بنجاح! / Setup completed successfully!"
echo ""
echo "🚀 لتشغيل التطبيق / To start the application:"
echo "   source .venv/bin/activate"
echo "   uvicorn --factory --host 0.0.0.0 speaches.main:create_app"
echo ""
echo "🌐 ثم افتح المتصفح على / Then open your browser to:"
echo "   http://localhost:8000"
echo ""
echo "📚 للمزيد من التفاصيل، راجع ملف / For more details, see:"
echo "   docs/installation.md"