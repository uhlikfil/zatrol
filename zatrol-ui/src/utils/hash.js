export const hashStr = (string) => {
  let hash = 0
  for (let i = 0; i < string.length; i++) {
    hash = (hash << 5) - hash + string.charCodeAt(i)
    hash |= 0 // Convert to 32bit integer
  }
  return hash + 2147483648 // always positive
}
