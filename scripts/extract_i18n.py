import os
import re
import json

def extract_keys():
    keys = set()

    # 1. Extract from index.html (data-i18n and data-i18n-placeholder)
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            # Simple regex for data-i18n="key" and data-i18n-placeholder="key"
            keys.update(re.findall(r'data-i18n="([^"]+)"', content))
            keys.update(re.findall(r'data-i18n-placeholder="([^"]+)"', content))

    # 2. Extract from app.js (i18n.t('key'))
    if os.path.exists('app.js'):
        with open('app.js', 'r', encoding='utf-8') as f:
            content = f.read()
            # Simple regex for i18n.t('key') or i18n.t("key")
            keys.update(re.findall(r"i18n\.t\(['\"]([^'\"]+)['\"]", content))

    # 3. Extract from skills_data.json (categories)
    if os.path.exists('skills_data.json'):
        with open('skills_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                if 'category' in item:
                    keys.add(item['category'])

    # 4. Extract from platforms list in app.js
    if os.path.exists('app.js'):
        with open('app.js', 'r', encoding='utf-8') as f:
            content = f.read()
            # Find the platforms array and extract the 'desc' values
            # This is a bit more complex, using a targeted regex for the platform_desc_* pattern
            keys.update(re.findall(r"desc: ['\"]([^'\"]+)['\"]", content))

    # 5. Standard Categories from app.js (if any hardcoded list)
    standard_categories = ['All', 'Office', 'Automation', 'Finance', 'Communication', 'Utilities', 'Data', 'Education', 'Marketing', 'Sales', 'Lifestyle', 'Legal', 'Search', 'Creative', 'Productivity', 'Research', 'Coding']
    keys.update(standard_categories)

    return sorted(list(keys))

def update_locale_file(keys, lang='en'):
    filepath = f'locales/{lang}.json'
    existing_data = {}
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                pass

    # Update with new keys, keeping existing translations
    new_data = {key: existing_data.get(key, key) for key in keys}

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    print(f"Updated {filepath} with {len(keys)} keys.")

if __name__ == "__main__":
    os.makedirs('locales', exist_ok=True)
    keys = extract_keys()
    update_locale_file(keys, 'en')
    # Also update zh.json with keys if it doesn't exist, but don't overwrite translations
    update_locale_file(keys, 'zh')
