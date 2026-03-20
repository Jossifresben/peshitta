/**
 * Peshitta Root Finder — Global UI behaviors
 * Settings, theme, language, share, Syriac font variant
 */

(function() {
    'use strict';

    // --- Dark Mode ---
    var html = document.documentElement;
    var themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        var themeIcon = themeBtn.querySelector('.material-symbols-outlined');

        function applyTheme(theme) {
            html.setAttribute('data-theme', theme);
            if (themeIcon) themeIcon.textContent = theme === 'dark' ? 'bedtime' : 'sunny';
        }

        var savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            applyTheme(savedTheme);
        }

        themeBtn.addEventListener('click', function() {
            var current = html.getAttribute('data-theme') || 'light';
            var next = current === 'dark' ? 'light' : 'dark';
            localStorage.setItem('theme', next);
            applyTheme(next);
        });

    }

    // --- Language Dropdown ---
    var langToggle = document.getElementById('lang-toggle');
    var langDropdown = document.getElementById('lang-dropdown');
    if (langToggle && langDropdown) {
        langToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            langDropdown.classList.toggle('open');
            var sd = document.getElementById('settings-dropdown');
            if (sd) sd.classList.remove('open');
        });
        document.addEventListener('click', function() {
            langDropdown.classList.remove('open');
        });
        langDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // --- Settings Dropdown ---
    var settingsToggle = document.getElementById('settings-toggle');
    var settingsDropdown = document.getElementById('settings-dropdown');
    if (settingsToggle && settingsDropdown) {
        settingsToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            settingsDropdown.classList.toggle('open');
            if (langDropdown) langDropdown.classList.remove('open');
        });

        settingsDropdown.querySelectorAll('.settings-option').forEach(function(opt) {
            opt.addEventListener('click', function() {
                var url = new URL(window.location.href);
                var scriptVal = this.getAttribute('data-script');
                var transVal = this.getAttribute('data-trans');
                if (scriptVal) {
                    localStorage.setItem('script', scriptVal);
                    url.searchParams.set('script', scriptVal);
                } else if (transVal) {
                    localStorage.setItem('trans', transVal);
                    url.searchParams.set('trans', transVal);
                } else {
                    return;
                }
                window.location.href = url.toString();
            });
        });

        document.addEventListener('click', function() {
            settingsDropdown.classList.remove('open');
        });
        settingsDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // --- Syriac Font Variant ---
    var storedFont = localStorage.getItem('syriac-font') || 'estrangela';
    if (storedFont !== 'estrangela') {
        html.setAttribute('data-syriac-font', storedFont);
    }
    document.querySelectorAll('.syriac-font-option').forEach(function(btn) {
        if (btn.getAttribute('data-syriac-font') === storedFont) {
            btn.classList.add('active');
        }
        btn.addEventListener('click', function() {
            var val = this.getAttribute('data-syriac-font');
            localStorage.setItem('syriac-font', val);
            if (val === 'estrangela') {
                html.removeAttribute('data-syriac-font');
            } else {
                html.setAttribute('data-syriac-font', val);
            }
            document.querySelectorAll('.syriac-font-option').forEach(function(b) {
                b.classList.remove('active');
            });
            this.classList.add('active');
        });
    });

    // --- Sync stored preferences with URL params ---
    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('trans')) {
        localStorage.setItem('trans', urlParams.get('trans'));
    }
    if (urlParams.has('script')) {
        localStorage.setItem('script', urlParams.get('script'));
    }

    // --- Stored Preferences Redirect ---
    var needsRedirect = false;
    if (!urlParams.has('script')) {
        var storedScript = localStorage.getItem('script');
        if (storedScript && storedScript !== 'latin') {
            urlParams.set('script', storedScript);
            needsRedirect = true;
        }
    }
    if (!urlParams.has('trans')) {
        var storedTrans = localStorage.getItem('trans');
        if (storedTrans) {
            urlParams.set('trans', storedTrans);
            needsRedirect = true;
        }
    }
    if (needsRedirect) {
        var newUrl = window.location.pathname + '?' + urlParams.toString() + window.location.hash;
        window.location.replace(newUrl);
    }

    // --- Share / QR Modal ---
    var shareBtn = document.getElementById('share-toggle');
    var shareModal = document.getElementById('share-modal');
    if (shareBtn && shareModal) {
        var shareUrl = document.getElementById('share-url');
        var copyBtn = document.getElementById('share-copy-btn');
        var qrEl = document.getElementById('share-qr');
        var qrGenerated = false;

        shareBtn.addEventListener('click', function() {
            var url = window.location.href;
            if (shareUrl) shareUrl.value = url;
            if (!qrGenerated && qrEl && typeof QRCode !== 'undefined') {
                var isDark = html.getAttribute('data-theme') === 'dark';
                new QRCode(qrEl, {
                    text: url,
                    width: 200,
                    height: 200,
                    colorDark: isDark ? '#e8dfd5' : '#2c1810',
                    colorLight: isDark ? '#2a2018' : '#ffffff',
                    correctLevel: QRCode.CorrectLevel.M
                });
                qrGenerated = true;
            }
            shareModal.classList.add('active');
        });

        shareModal.addEventListener('click', function(e) {
            if (e.target === shareModal) shareModal.classList.remove('active');
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && shareModal.classList.contains('active')) {
                shareModal.classList.remove('active');
            }
        });

        if (copyBtn && shareUrl) {
            copyBtn.addEventListener('click', function() {
                shareUrl.select();
                navigator.clipboard.writeText(shareUrl.value).then(function() {
                    copyBtn.querySelector('.material-symbols-outlined').textContent = 'check';
                    setTimeout(function() {
                        copyBtn.querySelector('.material-symbols-outlined').textContent = 'content_copy';
                    }, 1500);
                });
            });
        }
    }
})();
