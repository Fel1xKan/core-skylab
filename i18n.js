/**
 * i18n.js - Lightweight Internationalization Manager
 */

class I18n {
    constructor() {
        this.currentLang = localStorage.getItem('app-language') || 'en';
        this.translations = {};
        this.onLanguageChange = null;
    }

    async init() {
        await this.loadTranslations(this.currentLang);
        this.translatePage();
    }

    async loadTranslations(lang) {
        try {
            const response = await fetch(`locales/${lang}.json`);
            if (response.ok) {
                this.translations = await response.json();
                this.currentLang = lang;
                localStorage.setItem('app-language', lang);
                document.documentElement.lang = lang;
            } else {
                console.error(`Failed to load translations for ${lang}`);
            }
        } catch (error) {
            console.error(`Error loading translations: ${error}`);
        }
    }

    t(key, defaultValue) {
        return this.translations[key] || defaultValue || key;
    }

    async setLanguage(lang) {
        if (lang === this.currentLang) return;
        await this.loadTranslations(lang);
        this.translatePage();
        if (typeof this.onLanguageChange === 'function') {
            this.onLanguageChange(lang);
        }
    }

    translatePage() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            const translation = this.t(key);

            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                if (el.placeholder) {
                    el.placeholder = translation;
                } else {
                    el.value = translation;
                }
            } else {
                el.textContent = translation;
            }
        });

        const placeholders = document.querySelectorAll('[data-i18n-placeholder]');
        placeholders.forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = this.t(key);
        });
    }
}

const i18n = new I18n();
window.i18n = i18n;
