let data = {x: [], y: [], data: {}};

let s = 'abcdefghihklmnopq';
data.x = s.split('');
data.y = s.split('');

for (let c1 of s) {
  for (let c2 of s) {
    data.data[`${c1}-${c2}`] = {
      x: c1,
      y: c2,
      type: ['A', 'B', 'C', 'D'][Math.floor(Math.random() * 4)],
      value: Math.random() > .8 ? 1 : 0,
    }
  }
}

export default data;

const commonLabels = `0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
0,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,6M0J,nan,nan,nan
1,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,both,nan,nan,nan,nan,nan,nan
2,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,both,nan,nan,nan,nan,nan,nan
3,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,both,both,nan,nan,nan
4,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,both,nan,nan,both,both,both,nan,nan,nan
5,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,both,nan,nan,nan,nan,nan,nan
6,nan,nan,nan,2AJF,nan,nan,nan,nan,6M0J,both,both,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan
7,nan,nan,nan,nan,nan,nan,nan,nan,both,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan
8,nan,nan,nan,nan,nan,nan,nan,nan,both,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan
9,nan,6M0J,6M0J,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,both,nan,nan,nan,nan,nan,nan,nan
10,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,both,both,both,nan,nan,nan,nan,nan
11,nan,nan,6M0J,nan,2AJF,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan
12,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,2AJF,2AJF,2AJF,nan,6M0J,nan,nan,nan
13,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,6M0J,nan,nan,nan,nan,nan,nan,nan,nan,nan
14,nan,nan,nan,6M0J,both,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,2AJF,nan,nan,nan
15,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,both,both,nan,nan,nan,nan,nan,nan,nan,nan,nan
16,6M0J,nan,nan,nan,nan,both,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan
17,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,both,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan
18,nan,nan,nan,nan,nan,6M0J,both,nan,nan,nan,both,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan
19,nan,nan,nan,nan,nan,nan,6M0J,nan,nan,both,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan,nan`;

const commonValues = `0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
0,,,,,,,,,,,,,,,,,,1.0,,,
1,,,,,,,,,,,,,,,1.0,,,,,,
2,,,,,,,,,,,,,,,1.0,,,,,,
3,,,,,,,,,,,,,,,,,1.0,1.0,,,
4,,,,,,,,,,,,,1.0,,,1.0,1.0,1.0,,,
5,,,,,,,,,,,,,,,1.0,,,,,,
6,,,,1.0,,,,,1.0,1.0,1.0,,,,,,,,,,
7,,,,,,,,,1.0,,,,,,,,,,,,
8,,,,,,,,,1.0,,,,,,,,,,,,
9,,1.0,1.0,,,,,,,,,,,1.0,,,,,,,
10,,,,,,,,,,,,,,1.0,1.0,1.0,,,,,
11,,,4.0,,1.0,,,,,,,,,,,,,,,,
12,,,,,,,,,,,,,,1.0,1.0,1.0,,2.0,,,
13,,,,,,,,,,,,1.0,,,,,,,,,
14,,,,1.0,1.0,,,,,,,,,,,,,1.0,,,
15,,,,,,,,,,,1.0,1.0,,,,,,,,,
16,3.0,,,,,1.0,,,,,,,,,,,,,,,
17,,,,,,,,,,,1.0,,,,,,,,,,
18,,,,,,1.0,1.0,,,,1.0,,,,,,,,,,
19,,,,,,,1.0,,,1.0,,,,,,,,,,,`;