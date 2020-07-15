function colors() {
  const pool = {};
  return function (type, highlight=false) {
    if (!pool[type]) {
      pool[type] = [
        Math.floor(Math.random() * 256),
        Math.floor(Math.random() * 256),
        Math.floor(Math.random() * 256),
      ]
    }
    if (highlight) {
      return `rgba(${pool[type][0]},${pool[type][1]},${pool[type][2]},.9)`;
    } else {
      return `rgba(${pool[type][0]},${pool[type][1]},${pool[type][2]},.5)`;
    }
  }
}

const getColor = colors();

export default getColor;

