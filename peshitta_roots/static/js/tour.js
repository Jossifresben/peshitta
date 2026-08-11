/**
 * Peshitta Constellations — Guided Tour
 * Zero-dependency step-by-step walkthrough with spotlight overlay.
 *
 * Usage:
 *   PeshittaTour.start(stepsArray, { onFinish: fn })
 *
 * Each step: { target: '#selector' | null, title: '', body: '', position: 'bottom' }
 * position: 'top' | 'bottom' | 'left' | 'right' | 'center'
 * If target is null or not found, tooltip shows centered (welcome/farewell screens).
 */
var PeshittaTour = (function() {
    'use strict';

    var overlay, spotlight, tooltip, stepDots, currentStep, steps, opts;

    function create() {
        // Overlay backdrop
        overlay = document.createElement('div');
        overlay.className = 'tour-overlay';

        // Spotlight hole (positioned over the target element)
        spotlight = document.createElement('div');
        spotlight.className = 'tour-spotlight';

        // Tooltip
        tooltip = document.createElement('div');
        tooltip.className = 'tour-tooltip';
        tooltip.innerHTML =
            '<div class="tour-tooltip-title"></div>' +
            '<div class="tour-tooltip-body"></div>' +
            '<div class="tour-tooltip-footer">' +
                '<div class="tour-dots"></div>' +
                '<div class="tour-buttons">' +
                    '<button class="tour-btn tour-btn-skip"></button>' +
                    '<button class="tour-btn tour-btn-next"></button>' +
                '</div>' +
            '</div>';

        document.body.appendChild(overlay);
        document.body.appendChild(spotlight);
        document.body.appendChild(tooltip);

        stepDots = tooltip.querySelector('.tour-dots');

        // Events
        overlay.addEventListener('click', function(e) {
            e.stopPropagation();
        });
        tooltip.querySelector('.tour-btn-skip').addEventListener('click', finish);
        tooltip.querySelector('.tour-btn-next').addEventListener('click', next);
        document.addEventListener('keydown', onKey);
    }

    function destroy() {
        if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
        if (spotlight && spotlight.parentNode) spotlight.parentNode.removeChild(spotlight);
        if (tooltip && tooltip.parentNode) tooltip.parentNode.removeChild(tooltip);
        document.removeEventListener('keydown', onKey);
        overlay = spotlight = tooltip = stepDots = null;
    }

    function onKey(e) {
        if (e.key === 'Escape') finish();
        if (e.key === 'ArrowRight' || e.key === 'Enter') next();
        if (e.key === 'ArrowLeft') prev();
    }

    function start(stepsArr, options) {
        steps = stepsArr;
        opts = options || {};
        currentStep = 0;
        create();
        show();
    }

    function next() {
        if (currentStep < steps.length - 1) {
            currentStep++;
            show();
        } else {
            finish();
        }
    }

    function prev() {
        if (currentStep > 0) {
            currentStep--;
            show();
        }
    }

    function finish() {
        destroy();
        localStorage.setItem('tourCompleted', 'true');
        if (opts.onFinish) opts.onFinish();
    }

    function show() {
        var step = steps[currentStep];
        var el = step.target ? document.querySelector(step.target) : null;

        // Title & body
        tooltip.querySelector('.tour-tooltip-title').textContent = step.title || '';
        tooltip.querySelector('.tour-tooltip-body').innerHTML = step.body || '';

        // Dots
        var dotsHtml = '';
        for (var i = 0; i < steps.length; i++) {
            dotsHtml += '<span class="tour-dot' + (i === currentStep ? ' active' : '') + '"></span>';
        }
        stepDots.innerHTML = dotsHtml;

        // Buttons
        var skipBtn = tooltip.querySelector('.tour-btn-skip');
        var nextBtn = tooltip.querySelector('.tour-btn-next');
        var isLast = currentStep === steps.length - 1;
        skipBtn.textContent = opts.skipLabel || 'Skip';
        nextBtn.textContent = isLast ? (opts.finishLabel || 'Done') : (opts.nextLabel || 'Next');
        skipBtn.style.display = isLast ? 'none' : '';

        if (el) {
            // Scroll element into view
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Small delay for scroll to finish
            setTimeout(function() {
                positionSpotlight(el);
                positionTooltip(el, step.position || 'bottom');
            }, 350);
        } else {
            // Center mode (no target). Uses position:fixed + explicit left/top
            // rather than transform-based centering, so a mobile CSS rule that
            // pins left/right can't fight the transform and push it off-screen.
            spotlight.style.display = 'none';
            tooltip.className = 'tour-tooltip tour-tooltip-center';
            tooltip.style.transform = 'none';
            tooltip.style.position = 'fixed';
            tooltip.style.right = 'auto';
            tooltip.style.bottom = 'auto';

            var cw = window.innerWidth < 600 ? window.innerWidth - 24 : 340;
            tooltip.style.width = cw + 'px';
            tooltip.style.left = Math.max(12, (window.innerWidth - cw) / 2) + 'px';

            var ch = tooltip.offsetHeight;
            tooltip.style.top = Math.max(12, (window.innerHeight - ch) / 2) + 'px';
        }

        // Animate in
        overlay.classList.add('active');
        tooltip.classList.add('active');
    }

    function positionSpotlight(el) {
        var rect = el.getBoundingClientRect();
        var pad = 8;
        spotlight.style.display = 'block';
        spotlight.style.top = (rect.top + window.scrollY - pad) + 'px';
        spotlight.style.left = (rect.left + window.scrollX - pad) + 'px';
        spotlight.style.width = (rect.width + pad * 2) + 'px';
        spotlight.style.height = (rect.height + pad * 2) + 'px';
    }

    function positionTooltip(el, pos) {
        var rect = el.getBoundingClientRect();
        var pad = 16;
        var ttWidth = window.innerWidth < 600 ? window.innerWidth - 24 : 340;

        tooltip.className = 'tour-tooltip active tour-pos-' + pos;
        tooltip.style.transform = 'none';
        tooltip.style.right = 'auto';
        tooltip.style.bottom = 'auto';
        // Reset anything center mode may have set (it uses position:fixed and
        // an explicit width; anchored steps are absolute and CSS-sized).
        tooltip.style.position = 'absolute';
        tooltip.style.width = '';

        // Measure rendered tooltip height (content already populated in show()
        // before positionTooltip runs, so offsetHeight is current).
        var ttHeight = tooltip.offsetHeight;

        var top, left;
        switch (pos) {
            case 'top':
                top = rect.top + window.scrollY - ttHeight - pad;
                left = rect.left + window.scrollX + rect.width / 2 - ttWidth / 2;
                break;
            case 'bottom':
                top = rect.bottom + window.scrollY + pad;
                left = rect.left + window.scrollX + rect.width / 2 - ttWidth / 2;
                break;
            case 'left':
                top = rect.top + window.scrollY + rect.height / 2 - ttHeight / 2;
                left = rect.left + window.scrollX - ttWidth - pad;
                break;
            case 'right':
                top = rect.top + window.scrollY + rect.height / 2 - ttHeight / 2;
                left = rect.right + window.scrollX + pad;
                break;
            default:
                top = rect.bottom + window.scrollY + pad;
                left = rect.left + window.scrollX;
        }

        // If the bottom-anchored tooltip would extend off-viewport but there's
        // room above the target, flip to top placement so the user sees the
        // whole tooltip without scrolling.
        var viewportBottom = window.scrollY + window.innerHeight;
        var viewportTop = window.scrollY;
        if (pos === 'bottom' && top + ttHeight + pad > viewportBottom) {
            var aboveTop = rect.top + window.scrollY - ttHeight - pad;
            if (aboveTop > viewportTop + pad) {
                top = aboveTop;
            }
        }

        tooltip.style.top = clampTop(top, ttHeight) + 'px';
        tooltip.style.left = clampLeft(left) + 'px';
    }

    function clampLeft(left) {
        var tw = window.innerWidth < 600 ? window.innerWidth - 24 : 340;
        var maxLeft = window.innerWidth - tw - 12;
        if (left < 12) return 12;
        if (left > maxLeft) return maxLeft;
        return left;
    }

    function clampTop(top, height) {
        // Keep the whole tooltip within the current viewport (relative to the
        // document, since the tooltip is position:absolute). Pad 12px from each
        // viewport edge. If the tooltip is taller than the viewport itself,
        // pin to viewport top so the title/body are at least visible.
        var pad = 12;
        var viewportTop = window.scrollY + pad;
        var viewportBottom = window.scrollY + window.innerHeight - height - pad;
        if (viewportBottom < viewportTop) return viewportTop;
        if (top < viewportTop) return viewportTop;
        if (top > viewportBottom) return viewportBottom;
        return top;
    }

    return { start: start, finish: finish };
})();
