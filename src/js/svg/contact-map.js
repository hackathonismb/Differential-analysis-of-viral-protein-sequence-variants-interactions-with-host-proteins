import config from "../utils/config.js";
import getColor from "../utils/colors.js";

const xmlns = "http://www.w3.org/2000/svg";

export default function contactMapSVG(data={x: [], y: [], data: {}}) {
  let svg = document.getElementById('svg');
  while (svg.lastChild) {
    svg.removeChild(svg.lastChild);
  }
  let canvas = document.getElementById('canvas');
  svg.setAttribute('width', canvas.clientWidth + '');
  svg.setAttribute('height', canvas.clientHeight + '');

  let bg = svg.appendChild(document.createElementNS(xmlns, 'rect'));
  bg.setAttributeNS(null, 'x', 0);
  bg.setAttributeNS(null, 'y', 0);
  bg.setAttributeNS(null, 'width', canvas.clientWidth + '');
  bg.setAttributeNS(null, 'height', canvas.clientHeight + '');
  bg.setAttributeNS(null, 'fill', config.backgroundColor);

  let g = svg.appendChild(document.createElementNS(xmlns, 'g'));
  g.setAttributeNS(null,'transform', `translate(${config.margin.left - config.lineWidth / 2}, ${config.margin.top - config.lineWidth / 2})`);
  g.setAttributeNS(null, 'font-family', config.font.split(' ')[1]);
  g.setAttributeNS(null, 'font-size', config.font.split(' ')[0]);
  g.setAttributeNS(null, 'stroke-width', config.lineWidth);

  let w = canvas.innerWidth;
  let h = canvas.innerHeight;
  let rect = g.appendChild(document.createElementNS(xmlns, 'rect'));
  rect.setAttributeNS(null, 'x', 0);
  rect.setAttributeNS(null, 'y', 0);
  rect.setAttributeNS(null, 'width', w);
  rect.setAttributeNS(null, 'height', h);
  rect.setAttributeNS(null, 'stroke', config.lineColor);
  rect.setAttributeNS(null, 'fill', config.backgroundColor);

  let gridWidth = config.gridWidth;
  for (let i = 0; i < data.x.length; i++) {
    let line = g.appendChild(document.createElementNS(xmlns, 'line'));
    line.setAttributeNS(null, 'x1', `${(i + 1) * gridWidth}`);
    line.setAttributeNS(null, 'y1', '0');
    line.setAttributeNS(null, 'x2', `${(i + 1) * gridWidth}`);
    line.setAttributeNS(null, 'y2', `${h}`);
    line.setAttributeNS(null, 'stroke', config.lineColor);
    line.setAttributeNS(null, 'stroke-dasharray', config.lineDash.join(' '));
    let text = g.appendChild(document.createElementNS(xmlns, 'text'));
    text.setAttributeNS(null, 'x', `${(i + 1) * gridWidth}`);
    text.setAttributeNS(null, 'y', `${-config.textMargin}`);
    text.setAttributeNS(null, 'fill', config.textColor);
    text.setAttributeNS(null, 'alignment-baseline', 'middle');
    text.setAttributeNS(null, 'text-anchor', 'start');
    text.setAttributeNS(null,'transform', `rotate(-90, ${(i+1) * gridWidth}, ${-config.textMargin})`);
    text.appendChild(document.createTextNode(data.x[i]));
  }

  for (let i = 0; i < data.y.length; i++) {
    let line = g.appendChild(document.createElementNS(xmlns, 'line'));
    line.setAttributeNS(null, 'y1', `${(i + 1) * gridWidth}`);
    line.setAttributeNS(null, 'x1', '0');
    line.setAttributeNS(null, 'y2', `${(i + 1) * gridWidth}`);
    line.setAttributeNS(null, 'x2', `${w}`);
    line.setAttributeNS(null, 'stroke', config.lineColor);
    line.setAttributeNS(null, 'stroke-dasharray', config.lineDash.join(' '));
    let text = g.appendChild(document.createElementNS(xmlns, 'text'));
    text.setAttributeNS(null, 'y', `${(i + 1) * gridWidth}`);
    text.setAttributeNS(null, 'x', `${-config.textMargin}`);
    text.setAttributeNS(null, 'fill', config.textColor);
    text.setAttributeNS(null, 'alignment-baseline', 'middle');
    text.setAttributeNS(null, 'text-anchor', 'end');
    text.appendChild(document.createTextNode(data.y[i]));
  }

  let selectedTypes = canvas.getContext('2d').selectedTypes;
  for (let i = 0; i < data.x.length; i++) {
    for (let j = 0; j < data.y.length; j++) {
      let o = data.data[`${data.x[i]}-${data.y[j]}`];
      if (selectedTypes.includes(o.type) && o.value) {
        let circle = g.appendChild(document.createElementNS(xmlns, 'circle'));
        circle.setAttributeNS(null, 'cx', (i + 1) * gridWidth + '');
        circle.setAttributeNS(null, 'cy', (j + 1) * gridWidth + '');
        circle.setAttributeNS(null, 'r', config.circleRadius);
        circle.setAttributeNS(null, 'fill', getColor(o.type));
      }
    }
  }
}