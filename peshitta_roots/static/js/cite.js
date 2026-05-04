(function() {
    'use strict';

    var citeData = null;
    var activeStyle = 'bibtex';
    var lastView = 'app';
    var lastLabel = null;

    window.openCiteModal = function(view, label) {
        lastView = view || 'app';
        lastLabel = label || null;
        var modal = document.getElementById('cite-modal');
        if (!modal) return;
        var output = document.getElementById('cite-output');
        if (output) output.textContent = 'Loading...';
        modal.classList.add('active');

        // Reset to BibTeX tab
        activeStyle = 'bibtex';
        document.querySelectorAll('.cite-style-tab').forEach(function(btn) {
            btn.classList.toggle('active', btn.getAttribute('data-style') === 'bibtex');
        });

        var url = location.origin + location.pathname + location.search;
        var qs = '?view=' + encodeURIComponent(lastView)
            + (lastLabel ? '&label=' + encodeURIComponent(lastLabel) : '')
            + '&url=' + encodeURIComponent(url);

        fetch('/api/citation' + qs)
            .then(function(r) { return r.json(); })
            .then(function(data) {
                citeData = data;
                renderActiveStyle();
            })
            .catch(function() {
                if (output) output.textContent = 'Error loading citation.';
            });
    };

    window.closeCiteModal = function() {
        var modal = document.getElementById('cite-modal');
        if (modal) modal.classList.remove('active');
    };

    window.switchCiteStyle = function(style) {
        activeStyle = style;
        document.querySelectorAll('.cite-style-tab').forEach(function(btn) {
            btn.classList.toggle('active', btn.getAttribute('data-style') === style);
        });
        renderActiveStyle();
    };

    window.copyCitation = function() {
        var output = document.getElementById('cite-output');
        if (!output) return;
        var text = output.textContent;
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(function() {
                flashCopyButton();
            });
        } else {
            var ta = document.createElement('textarea');
            ta.value = text;
            document.body.appendChild(ta);
            ta.select();
            try { document.execCommand('copy'); flashCopyButton(); } catch (e) {}
            document.body.removeChild(ta);
        }
    };

    function renderActiveStyle() {
        var output = document.getElementById('cite-output');
        if (!output || !citeData || !citeData.styles) return;
        output.textContent = citeData.styles[activeStyle] || '';
    }

    function flashCopyButton() {
        var btn = document.querySelector('.cite-copy-btn');
        if (!btn) return;
        var orig = btn.innerHTML;
        btn.innerHTML = '<span class="material-symbols-outlined">check</span> Copied';
        setTimeout(function() { btn.innerHTML = orig; }, 1500);
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeCiteModal();
    });
})();
