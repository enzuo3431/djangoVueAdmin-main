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
  const move = (elapsed) => {
    const now = elapsed
    const start = window.scrollY
    const change = to - start
    const increment = 20
    const duration = typeof duration === 'undefined' ? 500 : duration

    document.documentElement.scrollTop = change

    if (now < duration) {
      requestAnimFrame(move)
    } else {
      if (callback && typeof callback === 'function') {
        callback()
      }
    }
  }
  requestAnimFrame(move)
}
