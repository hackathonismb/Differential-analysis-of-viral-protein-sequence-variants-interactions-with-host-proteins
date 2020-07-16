import sampleData from "./sample-data.js";
import {labels, values} from "./real-data.js";
import drawContactMap from "../canvas/contact-map.js";

export default function load() {
  let d = document.getElementById('data');
  let selected = d.options[d.selectedIndex].value;
  let canvas = document.getElementById('canvas');
  switch (selected) {
    case 'sample-data':
      drawContactMap(canvas, sampleData, 'info-panel', 'type-options');
      document.getElementById('type-selector').classList.remove('hidden');
      break;
    case 'common-values':
      drawContactMap(canvas, values, 'info-panel', '');
      document.getElementById('type-selector').classList.add('hidden');
      break;
    case 'common-labels':
      drawContactMap(canvas, labels, 'info-panel', 'type-options');
      document.getElementById('type-selector').classList.remove('hidden');
      break;
    default:
      alert("Hey, you shouldn't see this alert.");
  }

  d.addEventListener('change', load);
}