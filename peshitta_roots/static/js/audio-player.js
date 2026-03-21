(function() {
    'use strict';
    if (typeof audioConfig === 'undefined') return;

    var audio = new Audio(audioConfig.src);
    audio.preload = 'auto';
    var verses = audioConfig.verses;
    var duration = audioConfig.duration;
    var mode = 'idle'; // 'idle', 'verse', 'chapter'
    var activeVerse = null;
    var sortedVerses = Object.keys(verses).map(Number).sort(function(a, b) { return a - b; });

    // DOM elements
    var playBtn = document.getElementById('chapter-play-btn');
    var progressWrap = document.getElementById('audio-progress-wrap');
    var progressBar = document.getElementById('audio-progress-bar');
    var timeDisplay = document.getElementById('audio-time');
    var speedSelect = document.getElementById('audio-speed');

    // Restore speed preference
    var savedSpeed = localStorage.getItem('peshitta_audio_speed');
    if (savedSpeed) {
        audio.playbackRate = parseFloat(savedSpeed);
        if (speedSelect) speedSelect.value = savedSpeed;
    }

    function formatTime(s) {
        var m = Math.floor(s / 60);
        var sec = Math.floor(s % 60);
        return m + ':' + (sec < 10 ? '0' : '') + sec;
    }

    function findVerseAtTime(t) {
        for (var i = sortedVerses.length - 1; i >= 0; i--) {
            var v = sortedVerses[i];
            if (t >= verses[v].start) return v;
        }
        return sortedVerses[0];
    }

    function highlightVerse(num) {
        if (activeVerse === num) return;
        clearHighlight();
        activeVerse = num;
        var el = document.getElementById('verse-' + num);
        if (el) {
            el.classList.add('verse-playing');
            // Auto-scroll if off screen
            var rect = el.getBoundingClientRect();
            if (rect.top < 80 || rect.bottom > window.innerHeight - 20) {
                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
        // Update per-verse button icon
        document.querySelectorAll('.audio-verse-play').forEach(function(btn) {
            var icon = btn.querySelector('.material-symbols-outlined');
            if (parseInt(btn.getAttribute('data-verse')) === num && !audio.paused) {
                icon.textContent = 'pause';
            } else {
                icon.textContent = 'volume_up';
            }
        });
    }

    function clearHighlight() {
        activeVerse = null;
        document.querySelectorAll('.verse-playing').forEach(function(el) {
            el.classList.remove('verse-playing');
        });
        document.querySelectorAll('.audio-verse-play .material-symbols-outlined').forEach(function(icon) {
            icon.textContent = 'volume_up';
        });
    }

    function updatePlayBtn() {
        var icon = playBtn.querySelector('.material-symbols-outlined');
        icon.textContent = audio.paused ? 'play_arrow' : 'pause';
    }

    // Timeupdate handler
    audio.addEventListener('timeupdate', function() {
        var t = audio.currentTime;

        // Update progress bar
        if (duration > 0) {
            progressBar.style.width = (t / duration * 100) + '%';
        }
        timeDisplay.textContent = formatTime(t) + ' / ' + formatTime(duration);

        // Determine active verse
        var currentV = findVerseAtTime(t);

        if (mode === 'verse') {
            // In verse mode, stop at verse end
            var vData = verses[currentV];
            if (currentV !== activeVerse && activeVerse !== null) {
                // We've passed beyond the target verse
                audio.pause();
                mode = 'idle';
                clearHighlight();
                updatePlayBtn();
                return;
            }
            if (vData && t >= vData.end - 0.05) {
                audio.pause();
                mode = 'idle';
                updatePlayBtn();
                return;
            }
            highlightVerse(currentV);
        } else if (mode === 'chapter') {
            highlightVerse(currentV);
        }
    });

    audio.addEventListener('ended', function() {
        mode = 'idle';
        clearHighlight();
        updatePlayBtn();
        progressBar.style.width = '100%';
    });

    // Chapter play/pause
    if (playBtn) {
        playBtn.addEventListener('click', function() {
            if (audio.paused) {
                mode = 'chapter';
                audio.play();
            } else {
                audio.pause();
                if (mode === 'chapter') mode = 'idle';
            }
            updatePlayBtn();
        });
    }

    // Per-verse play buttons (delegated)
    document.getElementById('reader-body').addEventListener('click', function(e) {
        var btn = e.target.closest('.audio-verse-play');
        if (!btn) return;
        e.stopPropagation();

        var verseNum = parseInt(btn.getAttribute('data-verse'));
        var vData = verses[verseNum];
        if (!vData) return;

        if (mode === 'verse' && activeVerse === verseNum && !audio.paused) {
            // Toggle pause on same verse
            audio.pause();
            mode = 'idle';
            clearHighlight();
            updatePlayBtn();
            return;
        }

        mode = 'verse';
        audio.currentTime = vData.start;
        audio.play();
        highlightVerse(verseNum);
        updatePlayBtn();
    });

    // Progress bar seek
    if (progressWrap) {
        progressWrap.addEventListener('click', function(e) {
            var rect = progressWrap.getBoundingClientRect();
            var pct = (e.clientX - rect.left) / rect.width;
            pct = Math.max(0, Math.min(1, pct));
            audio.currentTime = pct * duration;
            if (mode === 'idle' && !audio.paused) {
                mode = 'chapter';
            }
        });
    }

    // Speed control
    if (speedSelect) {
        speedSelect.addEventListener('change', function() {
            var rate = parseFloat(this.value);
            audio.playbackRate = rate;
            localStorage.setItem('peshitta_audio_speed', this.value);
        });
    }
})();
