import {drawContactMap} from "./canvas/draw.js";
import data from "./utils/sample-data.js";

window.onload = () => {
  drawContactMap(document.getElementById('canvas'), data);
};