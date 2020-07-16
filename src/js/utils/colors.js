function colors() {
  const pool = {
    '1': 'rgba(255,102,102,.4)',
    '2': 'rgba(255,102,102,.8)',
    '3': 'rgba(255,42,42,.9)',
    '4': 'rgba(255,0,0,.9)',
  };
  return function (type, highlight=false) {
    if (!pool[type]) {
      pool[type] = [
        Math.floor(Math.random() * 256),
        Math.floor(Math.random() * 256),
        Math.floor(Math.random() * 256),
      ]
    }
    if (typeof pool[type] === 'string') {
      return pool[type];
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

