export function formatDateTime(value) {
  if (!value) return '-'
  const input = String(value)
  // Normalize microseconds to milliseconds for Date parsing.
  const normalized = input.replace(
    /(\.\d{3})\d+(?=(Z|[+-]\d{2}:?\d{2})?$)/,
    '$1'
  )
  const date = new Date(normalized)
  if (Number.isNaN(date.getTime())) {
    return input
  }
  const pad = (num) => (num < 10 ? `0${num}` : `${num}`)
  const year = date.getFullYear()
  const month = pad(date.getMonth() + 1)
  const day = pad(date.getDate())
  const hours = pad(date.getHours())
  const minutes = pad(date.getMinutes())
  const seconds = pad(date.getSeconds())
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}
