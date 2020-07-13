let data = {x: [], y: [], data: {}};

let s = 'abcdefghihklmnopq';
data.x = s.split('');
data.y = s.split('');

for (let c1 of s) {
  for (let c2 of s) {
    data.data[`${c1}-${c2}`] = {
      type: 'interaction',
      value: Math.random() > .8 ? 1 : 0,
    }
  }
}

export default data;