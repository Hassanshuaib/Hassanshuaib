let audioCtx = null

// نغمة تنبيه بسيطة عبر Web Audio API بدون الحاجة لملف صوتي خارجي
export function playNewOrderBeep() {
  try {
    audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)()
    const now = audioCtx.currentTime

    ;[880, 1046.5].forEach((freq, i) => {
      const osc = audioCtx.createOscillator()
      const gain = audioCtx.createGain()
      osc.type = 'sine'
      osc.frequency.value = freq
      gain.gain.setValueAtTime(0.0001, now + i * 0.18)
      gain.gain.exponentialRampToValueAtTime(0.35, now + i * 0.18 + 0.02)
      gain.gain.exponentialRampToValueAtTime(0.0001, now + i * 0.18 + 0.22)
      osc.connect(gain)
      gain.connect(audioCtx.destination)
      osc.start(now + i * 0.18)
      osc.stop(now + i * 0.18 + 0.25)
    })
  } catch {
    // المتصفح لا يدعم Web Audio أو لم يُسمح بالتشغيل بعد بدون تفاعل المستخدم
  }
}
