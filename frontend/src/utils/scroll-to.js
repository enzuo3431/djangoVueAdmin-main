Math.easeInOutQuad = function(t, b, c, d) {
  t /= d / 2
  if (t < 1) {
    return c / 2 * t * t + b
  } else {
    return -c / 2 * ((--t) * (t - 2) - 1) + b
  }
}

// requestAnimationFrame for Smart Animating http://goo.gl/sx5sts
var requestAnimFrame = (function() {
  return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || function(callback) { window.setTimeout(callback, 1000 / 60) }
})()

export function scrollTo(to, duration, callback) {
  const start = window.scrollY || window.pageYOffset || 0
  const change = to - start
  const totalDuration = typeof duration === 'undefined' ? 500 : duration
  const startTime = performance.now()

  const move = (timestamp) => {
    const elapsed = timestamp - startTime
    const position = Math.easeInOutQuad(
      Math.min(elapsed, totalDuration),
      start,
      change,
      totalDuration
    )

    document.documentElement.scrollTop = position
    document.body.scrollTop = position

    if (elapsed < totalDuration) {
      requestAnimFrame(move)
      return
    }
    if (callback && typeof callback === 'function') {
      callback()
    }
  }

  requestAnimFrame(move)
}
